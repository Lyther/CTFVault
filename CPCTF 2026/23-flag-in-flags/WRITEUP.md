# Flag in Flags

The PNG looks like a wallpaper made from repeated flag tiles, so the first useful check is periodicity.

The image repeats vertically every `384` rows. If you subtract one `384`-row strip from the next, almost everything cancels out and the hidden content remains.

Minimal extraction:

```python
from PIL import Image
import numpy as np

img = Image.open("Flaggggg_2348u932f4728nv.png").convert("RGB")
arr = np.array(img, dtype=np.int16)

period = 384
diff = np.abs(arr[:period] - arr[period:2 * period]).astype(np.uint8)
boosted = np.clip(diff.astype(np.uint16) * 32, 0, 255).astype(np.uint8)

Image.fromarray(boosted).save("vertical_diff_boosted.png")
```

The boosted diff reveals green text near the top:

```text
CPCTF{FLAG_M
ANY_FLAGS_FL
AG}
```

So the flag is:

```text
CPCTF{FLAG_MANY_FLAGS_FLAG}
```

`solve.py` automates the strip search and writes the extracted images to `/tmp/flag_in_flags/`.
