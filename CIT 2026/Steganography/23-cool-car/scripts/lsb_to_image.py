from PIL import Image

img = Image.open("files/cool_car.png")
pixels = img.load()
w, h = img.size

out_img = Image.new("1", (w, h))
out_pixels = out_img.load()

for y in range(h):
    for x in range(w):
        # 255 for white (bit is 0), 0 for black (bit is 1)
        # Or vice versa. Let's make bit 1 = white, bit 0 = black
        out_pixels[x, y] = 255 if (pixels[x, y][0] & 1) else 0

out_img.save("lsb_red.png")
print("Saved lsb_red.png")
