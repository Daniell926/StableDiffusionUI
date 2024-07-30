import os
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, StableDiffusionControlNetPipeline, ControlNetModel
import datetime
import numpy as np
from PIL import Image

#SDV5_MODEL_PATH = os.getenv("SDV5_MODEL_PATH")
#SAVE_PATH = os.environ("USERPROFILE")

current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct paths relative to the src directory

SD_MODEL_PATH = os.path.abspath(os.path.join(current_dir, "..", "models", "Stable-Diffusion", "stable-diffusion-v1-5"))
CN_MODEL_PATH = os.path.abspath(os.path.join(current_dir, "..", "models", "ControlNet", "sd-controlnet-canny"))

print(SD_MODEL_PATH)
print(CN_MODEL_PATH)
SAVE_PATH = os.path.join(os.getcwd(), "output")


device_type = "cuda" if torch.cuda.is_available() else "cpu"
low_vram = True


def name_file(path):
    current_dt = datetime.datetime.now()
    formatted_dt = current_dt.strftime("%Y-%m-%d_%H-%M")
    filename = f"{formatted_dt}.png"
    path += f"\{filename}"
    counter = 1

    while os.path.exists(path):
        file, ext = os.path.splitext(path)
        path = file + "(" + str(counter) + ")" + ext
        counter += 1

    return path

def numpy_to_pil(np_array):
    return Image.fromarray(np.uint8(np_array))

def init_cuda_pipe(using_CN: bool, low_vram: bool):

    if using_CN and low_vram:
        controlnet = ControlNetModel.from_pretrained(CN_MODEL_PATH)
        pipe = StableDiffusionControlNetPipeline.from_pretrained(SD_MODEL_PATH, torch_dtype=torch.float16, revision='fp16')
        pipe.enable_attention_slicing()

    elif low_vram:
        pipe = StableDiffusionPipeline.from_pretrained(SD_MODEL_PATH, torch_dtype=torch.float16, revision='fp16')
        pipe.enable_attention_slicing()

    elif using_CN:
        controlnet = ControlNetModel.from_pretrained(CN_MODEL_PATH)
        pipe = StableDiffusionControlNetPipeline.from_pretrained(SD_MODEL_PATH,controlnet=controlnet,safety_checker=None)

    else:
        pipe = StableDiffusionPipeline.from_pretrained(SD_MODEL_PATH)

    return pipe

def render_prompt(
        prompt, negative_prompt, num_steps, g_scale, height=512, width=512, img=None
):
    
    using_cn = (img is not None)
    if using_cn:
        img = numpy_to_pil(img)
    
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    
    if device_type == "cuda":

        pipe = init_cuda_pipe(using_cn, low_vram)
        pipe.to("cuda")

    elif device_type == "cpu":

        if using_cn:
            controlnet = ControlNetModel.from_pretrained(CN_MODEL_PATH)
            pipe = StableDiffusionControlNetPipeline.from_pretrained(SD_MODEL_PATH,controlnet=controlnet,safety_checker=None)
        
        else:
            pipe = StableDiffusionPipeline.from_pretrained(SD_MODEL_PATH)

    else:
        print("no gpu or cpu")
    
    print(f"\n\nGenerating with prompt: {prompt[:10]}...\nNegative prompt: {negative_prompt[:10]}...\nSteps: {num_steps}\nGuidance Scale: {g_scale}\nImg: {img}\nW: {width}\nHeight: {height}\n\n")
    
    with autocast(device_type):
        gen_image = pipe(
            prompt              =   prompt,
            negative_prompt     =   negative_prompt,
            num_inference_steps =   num_steps,
            guidance_scale      =   g_scale,
            height              =   height,
            width               =   width,
            image               =   img
            ).images[0]

    output_path = name_file(SAVE_PATH)
    gen_image.save(output_path)
    print(f"saved at: {output_path}")
    return output_path




