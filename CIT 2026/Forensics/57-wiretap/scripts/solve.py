#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "matplotlib>=3.9.0",
#   "Pillow>=11.2.0",
#   "scipy>=1.15.0",
# ]
# ///

import hashlib
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.io import wavfile
from scipy.signal import butter, hilbert, resample_poly, sosfiltfilt

EXPECTED_SHA1 = "fb8ef1616ef3e993e81d7f23f9d56b76d51175be"
START_SEC = 9.5
RESAMPLED_RATE = 7350
BAUD = 300
MANUAL_SHA1 = "a08ab8740169cee83a7dc2b345b9e9b34a408422"
GLYPH_MAP = {
    (
        ".####",
        "#....",
        "#....",
        "#....",
        "#....",
        "#....",
        ".####",
    ): "C",
    (
        "###",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        "###",
    ): "I",
    (
        "#####",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
        "..#..",
    ): "T",
    (
        "..##",
        ".#..",
        ".#..",
        "#...",
        ".#..",
        ".#..",
        "..##",
    ): "{",
    (
        "....",
        "....",
        ".###",
        "#..#",
        ".###",
        "...#",
        ".##.",
    ): "g",
    (
        ".###.",
        "#...#",
        "....#",
        "..##.",
        "....#",
        "#...#",
        ".###.",
    ): "3",
    (
        ".#..",
        ".#..",
        "###.",
        ".#..",
        ".#..",
        ".#..",
        "..##",
    ): "t",
    (
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        ".....",
        "#####",
    ): "_",
    (
        ".###.",
        "#..##",
        "#.#.#",
        "#.#.#",
        "#.#.#",
        "##..#",
        ".###.",
    ): "0",
    (
        "..##",
        ".#..",
        "###.",
        ".#..",
        ".#..",
        ".#..",
        ".#..",
    ): "f",
    (
        "#....",
        "#....",
        "#.##.",
        "##..#",
        "#...#",
        "#...#",
        "#...#",
    ): "h",
    (
        ".....",
        ".....",
        "####.",
        "#...#",
        "#...#",
        "####.",
        "#....",
    ): "p",
    (
        ".....",
        ".....",
        "#.##.",
        "##..#",
        "#...#",
        "#...#",
        "#...#",
    ): "n",
    (
        ".##.",
        "#.#.",
        "..#.",
        "..#.",
        "..#.",
        "..#.",
        ".###",
    ): "1",
    (
        ".....",
        ".....",
        "##.##",
        "#.#.#",
        "#.#.#",
        "#...#",
        "#...#",
    ): "m",
    (
        ".....",
        ".....",
        ".###.",
        "#...#",
        "#####",
        "#....",
        ".###.",
    ): "e",
    (
        ".....",
        ".....",
        "#.##.",
        "##..#",
        "#....",
        "#....",
        "#....",
    ): "r",
    (
        "##..",
        "..#.",
        "..#.",
        "...#",
        "..#.",
        "..#.",
        "##..",
    ): "}",
}


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def demodulate_channel(
    samples: np.ndarray,
    sample_rate: int,
    center_freq: float,
    low_cutoff: float,
    high_cutoff: float,
) -> np.ndarray:
    bandpass = butter(
        6,
        [low_cutoff, high_cutoff],
        btype="bandpass",
        fs=sample_rate,
        output="sos",
    )
    filtered = sosfiltfilt(bandpass, samples)

    analytic = hilbert(filtered)
    phase = np.exp(
        -1j * 2 * np.pi * center_freq * np.arange(len(filtered)) / sample_rate,
    )
    baseband = analytic * phase

    lowpass = butter(4, 180, btype="lowpass", fs=sample_rate, output="sos")
    i = sosfiltfilt(lowpass, np.real(baseband))
    q = sosfiltfilt(lowpass, np.imag(baseband))
    iq = i + 1j * q

    unwrapped = np.unwrap(np.angle(iq))
    return np.diff(unwrapped) * sample_rate / (2 * np.pi)


def decode_bits(
    freq_discriminator: np.ndarray,
    sample_rate: int,
    baud: int,
) -> list[int]:
    samples_per_bit = sample_rate / baud
    bit_count = int(len(freq_discriminator) / samples_per_bit) - 1
    bits: list[int] = []

    for index in range(bit_count):
        start = int(round(index * samples_per_bit + 0.2 * samples_per_bit))
        end = int(round((index + 1) * samples_per_bit - 0.2 * samples_per_bit))
        if end <= start:
            continue
        average = float(np.mean(freq_discriminator[start:end]))
        bits.append(1 if average > 0 else 0)

    return bits


def decode_async_bytes(bits: list[int]) -> bytes:
    output = bytearray()
    index = 1

    while index < len(bits) - 10:
        if bits[index - 1] == 1 and bits[index] == 0:
            value = sum(bits[index + 1 + shift] << shift for shift in range(8))
            if bits[index + 9] == 1:
                output.append(value)
                index += 10
                continue
        index += 1

    return bytes(output)


def render_manual_image(response_text: str, output_path: Path) -> str:
    matches = re.findall(
        r'<svg[^>]*viewBox="0 0 (\d+) 7"[^>]*><path d="([^"]+)"',
        response_text,
    )
    if len(matches) != 3:
        fail("expected three SVG strips in the decoded HTML")

    width = max(int(width) for width, _ in matches)
    height = 7 * len(matches)
    image = Image.new("1", (width, height), 1)

    for index, (_, path_data) in enumerate(matches):
        y_offset = index * 7
        for x, y, run_width in re.findall(r"M(\d+),(\d+)h(\d+)v1h-\d+", path_data):
            start_x = int(x)
            start_y = int(y)
            run = int(run_width)
            for pixel_x in range(start_x, start_x + run):
                image.putpixel((pixel_x, y_offset + start_y), 0)

    scaled = image.resize((width * 8, height * 8), Image.Resampling.NEAREST)
    scaled.save(output_path)

    digest = hashlib.sha1(output_path.read_bytes()).hexdigest()
    if digest != MANUAL_SHA1:
        fail(f"unexpected rendered manual hash: {digest}")

    return digest


def decode_svg_line(path_data: str, width: int) -> str:
    grid = [["."] * width for _ in range(7)]

    for x, y, run_width in re.findall(r"M(\d+),(\d+)h(\d+)v1h-\d+", path_data):
        start_x = int(x)
        start_y = int(y)
        run = int(run_width)
        for pixel_x in range(start_x, start_x + run):
            grid[start_y][pixel_x] = "#"

    spans: list[tuple[int, int]] = []
    in_run = False
    start = 0
    for column in range(width):
        filled = any(grid[row][column] == "#" for row in range(7))
        if filled and not in_run:
            start = column
            in_run = True
        elif not filled and in_run:
            spans.append((start, column))
            in_run = False
    if in_run:
        spans.append((start, width))

    decoded: list[str] = []
    for start, end in spans:
        glyph = tuple("".join(grid[row][start:end]) for row in range(7))
        character = GLYPH_MAP.get(glyph)
        if character is None:
            fail(f"unknown glyph: {glyph}")
        decoded.append(character)

    return "".join(decoded)


def decode_flag_from_response(response_text: str) -> str:
    matches = re.findall(
        r'<svg[^>]*viewBox="0 0 (\d+) 7"[^>]*><path d="([^"]+)"',
        response_text,
    )
    if len(matches) != 3:
        fail("expected three SVG strips in the decoded HTML")

    flag = "".join(
        decode_svg_line(path_data, int(width)) for width, path_data in matches
    )
    if not re.fullmatch(r"CIT\{[A-Za-z0-9_]+\}", flag):
        fail(f"decoded flag has unexpected format: {flag}")
    return flag


def save_spectrogram(
    raw_samples: np.ndarray,
    sample_rate: int,
    output_path: Path,
) -> None:
    plt.figure(figsize=(18, 6))
    plt.specgram(raw_samples, NFFT=2048, Fs=sample_rate, noverlap=1024, cmap="magma")
    plt.ylim(0, 4000)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.colorbar(label="Intensity (dB)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=180)
    plt.close()


def decode_capture(wav_path: Path, artifact_dir: Path) -> tuple[bytes, bytes]:
    sample_rate, samples = wavfile.read(wav_path)
    if samples.ndim > 1:
        samples = samples[:, 0]
    samples = samples.astype(float)

    trimmed = samples[int(START_SEC * sample_rate) :]
    resampled = resample_poly(trimmed, up=1, down=sample_rate // RESAMPLED_RATE)
    actual_rate = RESAMPLED_RATE

    low_channel = demodulate_channel(resampled, actual_rate, 1170.0, 900.0, 1400.0)
    high_channel = demodulate_channel(resampled, actual_rate, 2125.0, 1850.0, 2350.0)

    request_bytes = decode_async_bytes(decode_bits(low_channel, actual_rate, BAUD))
    response_bytes = decode_async_bytes(decode_bits(high_channel, actual_rate, BAUD))

    (artifact_dir / "request.bin").write_bytes(request_bytes)
    (artifact_dir / "response.bin").write_bytes(response_bytes)
    (artifact_dir / "request.txt").write_text(
        request_bytes.decode("latin1"),
        encoding="latin1",
    )
    (artifact_dir / "response.txt").write_text(
        response_bytes.decode("latin1"),
        encoding="latin1",
    )
    save_spectrogram(samples, sample_rate, artifact_dir / "spectrogram.png")

    return request_bytes, response_bytes


def main() -> None:
    default_wav = (
        Path(__file__).resolve().parent.parent / "files" / "beep_beep_boop.wav"
    )
    wav_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_wav

    if not wav_path.is_file():
        fail(f"missing WAV file: {wav_path}")

    sha1 = hashlib.sha1(wav_path.read_bytes()).hexdigest()
    if sha1 != EXPECTED_SHA1:
        fail(f"unexpected sha1: {sha1}")

    artifact_dir = Path(__file__).resolve().parent.parent / "other"
    artifact_dir.mkdir(parents=True, exist_ok=True)

    request_bytes, response_bytes = decode_capture(wav_path, artifact_dir)

    if b"GET /SiliconValley/Heights/4721/diary.html HTTP/1.0" not in request_bytes:
        fail("did not recover the expected HTTP request from the low Bell 103 channel")
    if b"HTTP/1.0 200 OK" not in response_bytes:
        fail(
            "did not recover the expected HTTP response from the high Bell 103 channel",
        )

    response_text = response_bytes.decode("latin1", "ignore")
    if "CyberDave98@aol.com" not in response_text:
        fail("decoded page does not match the expected recovered GeoCities page")

    render_manual_image(response_text, artifact_dir / "manual.png")
    print(decode_flag_from_response(response_text))


if __name__ == "__main__":
    main()
