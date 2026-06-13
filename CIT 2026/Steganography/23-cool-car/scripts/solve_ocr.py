from PIL import Image

img = Image.open("files/cool_car.png")
pixels = img.load()
w, h = img.size

# Instead of printing everything, let's extract connected components or just print the chunks separated.
# The user wants to OCR with their eyes.
# I will generate a text file with the chunks.

chunk_size = 150

with open("output_ocr.txt", "w") as f:
    for i in range(0, w, chunk_size):
        f.write(f"--- Chunk {i} to {i + chunk_size} ---\n")
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
            f.writelines(line + "\n" for line in lines)
