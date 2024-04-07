from PIL import Image, ImageDraw
import random
import math
from tqdm import trange
import argparse

parser = argparse.ArgumentParser(
                    prog='Ranpack',
                    description='Creates a stylized image from a base image',
                    epilog='Ranpack packs circles randomly')

parser.add_argument("input")
parser.add_argument("output")
parser.add_argument("-n", "--number")
parser.add_argument("-r", "--radius")

args = parser.parse_args()

N = int(args.number) if args.number else 100000
RADIUS = int(args.radius) if args.radius else 30
images = []

print(args)

img = Image.open(args.input)
res = Image.new("RGB", img.size, (0, 0, 0))

GRID_SIZE = int(min(img.size)/RADIUS/2)

circles = [[[] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

x = random.randint(0, img.size[0]-1)
y = random.randint(0, img.size[1]-1)
r = 1

circles[int(x/img.size[0]*GRID_SIZE)][int(y/img.size[1]*GRID_SIZE)].append(((x, y), r))

draw = ImageDraw.Draw(res)

for iter in (t:=trange(N)):
    x = random.randint(0, img.size[0]-1)
    y = random.randint(0, img.size[1]-1)
    r = RADIUS
    checks = 0
    i = min(max(1, int(x/img.size[0]*GRID_SIZE)), GRID_SIZE-2)
    j = min(max(1, int(y/img.size[1]*GRID_SIZE)), GRID_SIZE-2)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            for c in circles[i+dx][j+dy]:
                checks += 1
                r = min(r, math.hypot(c[0][0]-x, c[0][1]-y)-c[1])
                            # if r < 0:
                            #     break
    
    t.set_description(str(checks))
    if r < 0:
        continue
    else:
        circles[int(x/img.size[0]*GRID_SIZE)][int(y/img.size[1]*GRID_SIZE)].append(((x, y), r))
        draw.ellipse((x-r, y-r, x+r, y+r), (img.getpixel((x, y))))

        if iter%1000==0:
            images.append(res.copy())


res.save(args.output)
res.show()

gif = Image.new("RGBA", res.size)
gif.save("res.gif", save_all=True, append_images=images)