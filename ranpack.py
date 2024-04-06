from PIL import Image, ImageDraw
import random
import math
from tqdm import trange

GRID_SIZE = 100

img = Image.open("koala.webp")
res = Image.new("RGB", img.size, (0, 0, 0))

circles = [[[] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

x = random.randint(0, img.size[0]-1)
y = random.randint(0, img.size[1]-1)
r = random.randint(5, 30)

circles[int(x/img.size[0]*GRID_SIZE)][int(y/img.size[1]*GRID_SIZE)].append(((x, y), r))

draw = ImageDraw.Draw(res)

for i in (t:=trange(200000)):
    x = random.randint(0, img.size[0]-1)
    y = random.randint(0, img.size[1]-1)
    r = 10
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

res.save("res.png")

res.show()