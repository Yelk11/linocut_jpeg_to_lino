
#!/usr/bin/env python3

import argparse
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
    parser.add_argument("output", help="Output image path")
    parser.add_argument(
        "-l", "--levels", type=int, default=4,
        help="Number of intensity levels (2-256, default: 4)"
    )
    parser.add_argument(
        "--gray", action="store_true",
        help="Convert the image to grayscale"
    )

    args = parser.parse_args()

    if not 2 <= args.levels <= 256:
        parser.error("Levels must be between 2 and 256.")

    try:
        with Image.open(args.input) as source:
            image = source.copy()

        result = posterize(image, args.levels, args.gray)
        result.save(args.output)

        print(f"Saved posterized image to {args.output}")

    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
# python3 posterize.py cat.jpg color.png --levels 2