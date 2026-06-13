from PIL import Image

img = Image.open("../../Steganography/23-cool-car/files/cool_car.png")
pixels = img.load()
w, h = img.size

lines = []
for y in range(0, 100, 1):
    row = "".join("#" if (pixels[x, y][0] & 1) else " " for x in range(0, 300, 1))
    lines.append(row)
print("\n".join(lines[:20]))
