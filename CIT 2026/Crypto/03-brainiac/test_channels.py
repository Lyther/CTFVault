from PIL import Image

img = Image.open("../../Steganography/23-cool-car/files/cool_car.png")
pixels = img.load()
w, h = img.size

for channel in range(3):
    print(f"--- Channel {channel} ---")
    lines = []
    for y in range(0, 100, 2):
        row = "".join("#" if (pixels[x, y][channel] & 1) else " " for x in range(0, 200, 2))
        lines.append(row)
    if any("#" in line for line in lines):
        print("\n".join(lines[:10]))
