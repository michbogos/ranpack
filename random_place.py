from PIL import Image, ImageDraw
import random
import math

circles = []

img = Image.open("koala.webp")
res = Image.new("RGB", img.size, (0, 0, 0))

draw = ImageDraw.Draw(res)

def generate(iterations, func):
    for i in range(iterations):
        r = random.randint(max(1, int(30-func(i))), max(1, int(100-func(i))))
        x = random.randint(0, img.size[0]-1)
        y = random.randint(0, img.size[1]-1)
        draw.ellipse((x, y, x+2*r, y+2*r), (img.getpixel((x, y))))

generate(100000, lambda x: x**0.4)

res.save("res.png")

res.show()