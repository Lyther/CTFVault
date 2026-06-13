from PIL import Image

img = Image.open("../../Steganography/23-cool-car/files/cool_car.png")
pixels = img.load()
w, h = img.size

lines_odd = []
for y in range(0, 100, 2):
    row = "".join("#" if (pixels[x, y][0] & 1) else " " for x in range(1, w, 2))
    lines_odd.append(row)

for i in range(0, w//2, 200):
    print(f"--- Chunk {i} to {i+200} ---")
    for row in lines_odd:
        if "#" in row[i:i+200]:
            print(row[i:i+200])
