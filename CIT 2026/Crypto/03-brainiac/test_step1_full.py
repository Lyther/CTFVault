from PIL import Image

img = Image.open("../../Steganography/23-cool-car/files/cool_car.png")
pixels = img.load()
w, h = img.size

lines = []
for y in range(0, 100, 1):
    row = "".join("#" if (pixels[x, y][0] & 1) else " " for x in range(0, w, 1))
    lines.append(row)

for i in range(0, w, 200):
    print(f"--- Chunk {i} to {i+200} ---")
    for row in lines:
        if "#" in row[i:i+200]:
            print(row[i:i+200])
