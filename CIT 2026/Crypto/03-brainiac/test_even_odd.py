from PIL import Image

img = Image.open("../../Steganography/23-cool-car/files/cool_car.png")
pixels = img.load()
w, h = img.size

print("--- EVEN PIXELS ---")
lines_even = []
for y in range(0, 100, 2):
    row = "".join("#" if (pixels[x, y][0] & 1) else " " for x in range(0, w, 2))
    lines_even.append(row)
print("\n".join(lines_even[:10]))

print("\n--- ODD PIXELS ---")
lines_odd = []
for y in range(0, 100, 2):
    row = "".join("#" if (pixels[x, y][0] & 1) else " " for x in range(1, w, 2))
    lines_odd.append(row)
print("\n".join(lines_odd[:10]))
