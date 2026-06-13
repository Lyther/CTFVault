from PIL import Image

img = Image.open("files/cool_car.png")
pixels = img.load()
w, h = img.size

chunk_size = 200  # 100 characters wide

for i in range(0, w, chunk_size):
    print(f"--- Chunk {i} to {i + chunk_size} ---")
    has_content = False
    lines = []
    for y in range(0, 100, 2):
        row = "".join(
            "#" if (pixels[x, y][0] & 1) else " "
            for x in range(i, min(i + chunk_size, w), 2)
        )
        if "#" in row:
            has_content = True
        lines.append(row)
    if has_content:
        for line in lines:
            print(line)
