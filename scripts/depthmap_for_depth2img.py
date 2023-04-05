import torch, gc
import cv2
import requests
import os.path
import contextlib
from PIL import Image
from modules.shared import opts, cmd_opts
from modules import processing, images, shared, devices
import os

from torchvision.transforms import Compose
from repositories.midas.midas.model_loader import load_model

import numpy as np

class SimpleDepthMapGenerator(object):
    def calculate_depth_maps(self,image,img_x,img_y,model_type_index,invert_depth):
        try:
            model = None
            def download_file(filename, url):
                print(f"download {filename} form {url}")
                import sys
                try:
                    with open(filename+'.tmp', "wb") as f:
                        response = requests.get(url, stream=True)
                        total_length = response.headers.get('content-length')

                        if total_length is None: # no content length header
                            f.write(response.content)
                        else:
                            dl = 0
                            total_length = int(total_length)
                            for data in response.iter_content(chunk_size=4096):
                                dl += len(data)
                                f.write(data)
                                done = int(50 * dl / total_length)
                                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                                sys.stdout.flush()
                    os.rename(filename+'.tmp', filename)
                except Exception as e:
                    os.remove(filename+'.tmp')
                    print("\n--------download fail------------\n")
                    raise e

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            # model path and name
            model_dir = "./models/midas"
            # create path to model if not present
            os.makedirs(model_dir, exist_ok=True)
            print("Loading midas model weights ..")
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            models = ["dpt_beit_large_512",
                "dpt_beit_large_384",
                "dpt_beit_base_384",
                "dpt_swin2_large_384",
                "dpt_swin2_base_384",
                "dpt_swin2_tiny_256",
                "dpt_swin_large_384",
                "dpt_next_vit_large_384",
                "dpt_levit_224",
                "dpt_large_384",
                "dpt_hybrid_384",
                "midas_v21_384",
                "midas_v21_small_256",
                # "openvino_midas_v21_small_256"
            ]
            model_path = model_dir + '/' + models[model_type_index] + '.pt'
            if not os.path.exists(model_path):
                if models.index("midas_v21_384") <= model_type_index:
                    download_file(model_path, "https://github.com/isl-org/MiDaS/releases/download/v2_1/"+ models[model_type_index] + ".pt")
                elif models.index("midas_v21_384") > model_type_index > models.index("dpt_large_384"):
                    download_file(model_path, "https://github.com/isl-org/MiDaS/releases/download/v3/"+ models[model_type_index] + ".pt")
                else:
                    download_file(model_path, "https://github.com/isl-org/MiDaS/releases/download/v3_1/"+ models[model_type_index] + ".pt")
            model, transform, net_w, net_h = load_model(device, model_path, models[model_type_index], (img_x, img_y))

            img = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB) / 255.0
            img_input = transform({"image": img})["image"]
            precision_scope = torch.autocast if shared.cmd_opts.precision == "autocast" and device == torch.device("cuda") else contextlib.nullcontext
            # compute
            with torch.no_grad(), precision_scope("cuda"):
                sample = torch.from_numpy(img_input).to(device).unsqueeze(0)
                if device == torch.device("cuda"):
                    sample = sample.to(memory_format=torch.channels_last)
                    if not cmd_opts.no_half:
                        sample = sample.half()
                prediction = model.forward(sample)
                prediction = (
                    torch.nn.functional.interpolate(
                        prediction.unsqueeze(1),
                        size=img.shape[:2],
                        mode="bicubic",
                        align_corners=False,
                    )
                    .squeeze()
                    .cpu()
                    .numpy()
                )
            # output
            depth = prediction
            numbytes=2
            depth_min = depth.min()
            depth_max = depth.max()
            max_val = (2**(8*numbytes))-1

            # check output before normalizing and mapping to 16 bit
            if depth_max - depth_min > np.finfo("float").eps:
                out = max_val * (depth - depth_min) / (depth_max - depth_min)
            else:
                out = np.zeros(depth.shape)
            # single channel, 16 bit image
            img_output = out.astype("uint16")

            # # invert depth map
            if invert_depth:
                img_output = cv2.bitwise_not(img_output)

            # three channel, 8 bits per channel image
            img_output2 = np.zeros_like(image)
            img_output2[:,:,0] = img_output / 256.0
            img_output2[:,:,1] = img_output / 256.0
            img_output2[:,:,2] = img_output / 256.0
            img = Image.fromarray(img_output2)
            return img
        except Exception:
            raise
        finally:
            del model
            gc.collect()
            devices.torch_gc()
