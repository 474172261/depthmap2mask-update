# 说明
这个是基于[depthmap2mask](https://github.com/Extraltodeus/depthmap2mask)k做的一部分改进, 因为[Midas](https://github.com/isl-org/MiDaS/releases)一直在更新, 但是原始项目并没有更新过, 所以我基于最新的midas代码, 做了点更改.

我已经将项目代码同步到原始项目了，你也可以直接安装原始的项目，这个项目就当中文的文档优化存在就好了。

## 安装
1. 在webui里添加本git连接并安装, 形如下图: (图中是原始的项目链接地址, 要改用本项目的git链接!)
![image](https://user-images.githubusercontent.com/15731540/204056273-fc27d1cf-48ac-4dc3-b737-95b4b1efd32e.png)

2. 默认会安装[Midas](https://github.com/isl-org/MiDaS/) v3.1

默认情况下, 如果找不到midas的模型, 它会自动下载到`stable-diffusion-webui\models\midas`目录里, 如果网络不稳定, 也可以手动下载它, 终端里会输出它下载的地址.

## 使用
在img2img栏目里, scripts里选择`Depth aware img2img mask`, 然后img2img里放入图片, 选择model, 设置`contrasts cut level`, 80到190范围内比较好突出人物, 点击生成即可看到深度图,


以下内容来自原始项目
## The look

![image](https://user-images.githubusercontent.com/15731540/204043153-09cbffd9-28ac-46be-ad99-fc7f2c8656a3.png)

## What does this extension do?

It creates masks for img2img based on a depth estimation made by [MiDaS](https://github.com/isl-org/MiDaS).

![smallerone](https://user-images.githubusercontent.com/15731540/204043576-5dc02def-29f8-423e-a69e-d392f47d3602.png)![5050](https://user-images.githubusercontent.com/15731540/204043582-ae46d0b8-3c4b-43d5-b669-eaf2659ced14.png)

## Where to find it after installing it?

Go to your img2img tab then select it from the custom scripts list at the bottom.

## Explanations of the different UI elements

- Contrasts cut level

![image](https://user-images.githubusercontent.com/15731540/204043824-6067bd9e-49d6-488b-8f99-47928c31ae46.png)

This slider is **purely optional**.
The depthmap is in levels of gray. Each pixel has a value in between 0 and 255 depending if they are black (0) or white (255). That threshold slider will cut to black every pixel below the selected value and scale from black to white what is above its value.

Or in a more human language, it will give more depth to your depthmaps while removing a lot of information.

Example before/after with the slider's value around 220 and using the MiDaS-Large model:

![00073--1 0- sampler -85-8 1-ac07d41f-20221125174853](https://user-images.githubusercontent.com/15731540/204044001-4e672bbe-4ff8-46ef-ae87-ec3377e7aa37.png)![00074--1 0- sampler -85-8 1-ac07d41f-20221125174934](https://user-images.githubusercontent.com/15731540/204044306-80c77ba3-3b38-4ea6-941c-f6c6006c8b4e.png)

Using the MiDaS small model will give you similar if not more interesting results.

![smallerone](https://user-images.githubusercontent.com/15731540/204043576-5dc02def-29f8-423e-a69e-d392f47d3602.png)![5050](https://user-images.githubusercontent.com/15731540/204043582-ae46d0b8-3c4b-43d5-b669-eaf2659ced14.png)

So that's more of an extra-extra option or a way to make sure that your backgrounds are untouched by using a low value (like 50).

- Match input size/Net width/Net height

![image](https://user-images.githubusercontent.com/15731540/204044819-0618bf27-0692-4a20-922f-73e33822dc6f.png)

Match input size (On by default) will make the depth analysis at the same size as the original image. Better not to touch it unless you are having performance issues.

The sliders below will be the resolution of the analysis if Match input size is turned off.

You can also just use these functionalities to test out different results.

- Misc options

![image](https://user-images.githubusercontent.com/15731540/204045429-778f3084-63ad-421d-ad43-af9a20c49621.png)

- Override options :

    These two options simply overrides the inpainting Masked content method and mask blur. I added these because using "original" for Masked content and Mask Blur at 0 just works better. This saves you the clics needed to switch to the intpaint tab/reupload the image to that tab and select the right options.
    
- MiDaS models :

    I'll let you try what suits your needs the most.
    
- Turn the depthmap into absolute black/white

![image](https://user-images.githubusercontent.com/15731540/204057815-1e7d1d38-2fbb-43a1-bb08-133e574138c2.png)

This option will cut out the background of an image into pure black and make the foreground pure white. Like a clean cut.

### Alpha Cropping

You can also save a version of the input image which has had all the masked content replaced with transparent pixels. This is useful when extracting the subject from the background, so that it can be used in designs.

![Image](https://i.imgur.com/yFX6LyQ.jpeg)

Simply check the "Save alpha mask" option before generating.

## Tips

- Avoid using Euler a or you might get really bad results. Usually DDIM works best.

## Credits/Citation

Thanks to [thygate](https://github.com/thygate) for letting me blatantly copy-paste some of his functions for the depth analysis integration in the webui.

This repository runs with [MiDaS](https://github.com/isl-org/MiDaS).

```
@ARTICLE {Ranftl2022,
    author  = "Ren\'{e} Ranftl and Katrin Lasinger and David Hafner and Konrad Schindler and Vladlen Koltun",
    title   = "Towards Robust Monocular Depth Estimation: Mixing Datasets for Zero-Shot Cross-Dataset Transfer",
    journal = "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    year    = "2022",
    volume  = "44",
    number  = "3"
}
```
```
@article{Ranftl2021,
	author    = {Ren\'{e} Ranftl and Alexey Bochkovskiy and Vladlen Koltun},
	title     = {Vision Transformers for Dense Prediction},
	journal   = {ICCV},
	year      = {2021},
}
```
