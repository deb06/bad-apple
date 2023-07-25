import os
from PIL import Image

cwd = os.getcwd()
video = f"{cwd}\\bad_apple.mp4"

frame_dir = f"{cwd}\\frame"
if not os.path.isdir(frame_dir):
    os.mkdir(frame_dir)

os.system(f"ffmpeg -i {video} -vf scale=160:120,fps=30 {frame_dir}\\frame_%04d.png")

txt_dir = f"{cwd}\\txt"
if not os.path.isdir(txt_dir):
    os.mkdir(txt_dir)


def create_ascii(fr, out):
    img = Image.open(fr)

    width, height = img.size
    aspect_ratio = height/width
    new_width = 160
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    img = img.convert('L')
    chars = ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "."]
    width, height = img.size
    pixels = img.getdata()
    print(pixels)
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
 
    with open(f"{out}.txt", "w") as f:
        f.write(ascii_image)

for i in os.listdir(frame_dir):
    name = i.replace(".png", "")
    create_ascii(f"{frame_dir}\\{i}",f"{txt_dir}\\{name}")

for i in os.listdir(txt_dir):
    with open(f"{txt_dir}\\{i}", 'r') as f:
        print(f.read())


    