
#!/usr/bin/env python3

import argparse
from pathlib import Path
from PIL import Image


def quantize(value: int, levels: int) -> int:
    """Map an intensity to one of the requested levels."""
    return round(round(value * (levels - 1) / 255)
                 * 255 / (levels - 1))


def posterize(image: Image.Image, levels: int,
              grayscale: bool = False) -> Image.Image:
    """Posterize an image in color or grayscale."""

    if not 2 <= levels <= 256:
        raise ValueError("Levels must be between 2 and 256.")

    if grayscale:
        image = image.convert("L")
    else:
        image = image.convert("RGB")

    # Build a 256-entry lookup table.
    lut = [quantize(i, levels) for i in range(256)]

    if image.mode == "L":
        return image.point(lut)

    # Apply the LUT independently to red, green, and blue.
    channels = image.split()
    result = [channel.point(lut) for channel in channels]

    return Image.merge("RGB", result)



def main():
    parser = argparse.ArgumentParser(
        description="Posterize an image for art or linocut."
    )
    parser.add_argument("input", help="Input image path")

    args = parser.parse_args()
    input_path = Path(args.input)
    output_path = input_path.with_name(f"{input_path.stem}_posterized.png")

    try:
        with Image.open(input_path) as source:
            image = source.copy()

        result = posterize(image, levels=2, grayscale=True)
        result.save(output_path)

        print(f"Saved posterized image to {output_path}")

    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
# python3 posterize.py cat.jpg color.png --levels 2