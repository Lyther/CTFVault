from pathlib import Path

import numpy as np
from PIL import Image


INPUT = Path(__file__).with_name("Flaggggg_2348u932f4728nv.png")
OUT_DIR = Path("/tmp/flag_in_flags")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    img = Image.open(INPUT).convert("RGB")
    arr = np.array(img, dtype=np.int16)
    h = arr.shape[0]

    best_score = None
    best_shift = None
    for shift in range(1, h // 2 + 1):
        score = np.mean(np.abs(arr[:-shift] - arr[shift:]))
        if best_score is None or score < best_score:
            best_score = score
            best_shift = shift

    assert best_shift is not None
    period = best_shift

    diff = np.abs(arr[:period] - arr[period : 2 * period]).astype(np.uint8)
    boosted = np.clip(diff.astype(np.uint16) * 32, 0, 255).astype(np.uint8)

    diff_path = OUT_DIR / "vertical_diff_boosted.png"
    Image.fromarray(boosted).save(diff_path)

    crop = Image.fromarray(boosted).crop((560, 0, 760, 120)).resize((800, 480), Image.NEAREST)
    crop_path = OUT_DIR / "flag_crop.png"
    crop.save(crop_path)

    print(f"best vertical period: {period}")
    print(f"saved: {diff_path}")
    print(f"saved: {crop_path}")
    print("flag: CPCTF{FLAG_MANY_FLAGS_FLAG}")


if __name__ == "__main__":
    main()
