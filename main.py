import os
from PIL import Image
from just_playback import Playback

# Setup
cwd = os.getcwd()
video = f"{cwd}\\" + input("File:")

if not os.path.exists(video):
    print("This video does not exist!")
    exit()
elif not ".mp4" in video:
    print("This is not a video file!")
    exit()

fps = input("Fps:")
if int(fps) > 60:
    print("Framerate is too high!\n Max: 60")
    exit()

def clear_dir(dir):
    for i in os.listdir(dir):
        os.remove(f"{dir}\\{i}")

frame_dir = f"{cwd}\\frame"
if not os.path.isdir(frame_dir):
    os.mkdir(frame_dir)
else:
    clear_dir(frame_dir)

txt_dir = f"{cwd}\\txt"
if not os.path.isdir(txt_dir):
    os.mkdir(txt_dir)
else:
    clear_dir(txt_dir)

# Processing Video
os.system(f"ffmpeg -i {video} -vf scale=160:120,fps={int(fps)} {frame_dir}\\%05d.png")

audio = video.replace("mp4","wav")

if os.path.isfile(audio):
    os.remove(audio)

os.system(f"ffmpeg -i {video} -map 0:a {audio}")

# Creating ASCII
def create_ascii(fr, out):
    img = Image.open(fr)
    width, height = img.size
    aspect_ratio = height/width
    new_width = 160
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    img = img.convert('L')
    chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ".", " "]
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

# Playing Video
playback = Playback()
playback.load_file(audio)
playback.play()

frames = os.listdir(txt_dir)
frame_count = len(frames)

while(playback.curr_pos < playback.duration):
    percentage = playback.curr_pos / float(playback.duration)
    percentage = float(percentage)
    frame = int(percentage * frame_count)

    with open(f"{txt_dir}\\{frames[frame]}",mode="r") as f:
        print(f.read())


# Cleaning
clear_dir(frame_dir)
os.removedirs(frame_dir)

clear_dir(txt_dir)
os.removedirs(frame_dir)

os.remove(audio)  