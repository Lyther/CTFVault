from PIL import Image

img = Image.open("files/cool_car.png")
pixels = img.load()
w, h = img.size

with open("lsb_red.txt", "w") as f:
    for y in range(h):
        row = "".join("#" if (pixels[x, y][0] & 1) else " " for x in range(w))
        f.write(row + "\n")
