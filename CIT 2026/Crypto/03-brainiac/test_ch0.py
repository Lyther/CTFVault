from PIL import Image

img = Image.open("../../Steganography/23-cool-car/files/cool_car.png")
pixels = img.load()
w, h = img.size

lines = []
for y in range(0, 100, 2):
    row = "".join("#" if (pixels[x, y][0] & 1) else " " for x in range(0, 1000, 2))
    lines.append(row)
print("\n".join(lines[:20]))
