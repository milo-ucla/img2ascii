#! /bin/env python3

import sys
import argparse
import numpy as np
from PIL import Image, ImageFilter


def get_image_dimensions(image_path: str):
    with Image.open(image_path) as img:
        width, height = img.size
        return (width, height)


def get_pixel_array(image_path: str):
    with Image.open(image_path) as img:
        pixel_array = np.array(img)
        return pixel_array


def scale_image(pixel_array, scale_factor: float):
    img = Image.fromarray(pixel_array)
    target_width = int(img.width * scale_factor)
    target_height = int(img.height * scale_factor * 0.4)
    resized_img = img.resize((target_width, target_height))
    resized_array = np.array(resized_img)
    return resized_array


def apply_image_filters(pixel_array, args):
    img = Image.fromarray(pixel_array)
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return np.array(img)


def convert_pixel_to_ansi_color_bg(pixel) -> str:
    """Converts a pixel into an ANSI color escape character.
    Args:
      pixel: A pixel represented as a 3-tuple of integers.
    Returns:
      An ANSI color escape character.
    """
    r, g, b = pixel
    # Create an ANSI color escape character.
    ansi_color = f"\033[48;2;{r};{g};{b}m\033[30m"
    return ansi_color


def convert_pixel_to_ansi_color_fg(pixel) -> str:
    """Converts a pixel into an ANSI color escape character.
    Args:
      pixel: A pixel represented as a 3-tuple of integers.

    Returns:
      An ANSI color escape character.
    """
    r, g, b = pixel
    # Create an ANSI color escape character.
    ansi_color = f"\033[38;2;{r};{g};{b}m"
    return ansi_color


def convert_to_ascii(pixel_array) -> str:
    # Map luminance to ASCII characters
    ascii_chars = "@%#*+=-:. "
    ascii_range = len(ascii_chars)

    # Convert pixel array to grayscale
    img = Image.fromarray(pixel_array)
    img = img.convert("L")
    pixel_array = np.array(img)
    # Normalize pixel values
    pixel_array = pixel_array / 255.0
    # Convert pixel values to ASCII characters based on luminance
    ascii_string = ""
    for row in pixel_array:
        for pixel in row:
            ascii_index = int(pixel * (ascii_range - 1))
            ascii_char = ascii_chars[ascii_index]
            ascii_string += ascii_char
        ascii_string += "\n"

    return ascii_string


def convert_bg_to_ansi(pixel_array) -> list[str]:
    ansi_array: list[str] = []
    for row in pixel_array:
        for pixel in row:
            ansi_array.append(convert_pixel_to_ansi_color_bg(pixel))
        ansi_array.append("")
    return ansi_array


def convert_fg_to_ansi(pixel_array) -> list[str]:
    ansi_array: list[str] = []
    for row in pixel_array:
        for pixel in row:
            ansi_array.append(convert_pixel_to_ansi_color_fg(pixel))
        ansi_array.append("\033[0m")
    return ansi_array


def main() -> None:
    parser = argparse.ArgumentParser(description="Image processing script")
    # Add the image path argument
    parser.add_argument(
        "image_path", help="path to the image file")
    # Add the scale option
    parser.add_argument("-s", "--scale", type=float,
                        help="scale factor to resize the image")
    parser.add_argument("-b", "--background-color", action="store_true",
                        help="add ANSI color to the background", default=False)
    parser.add_argument("-a", "--foreground-color", action="store_true",
                        help="add ANSI color to the characters", default=False)
    parser.add_argument("-o", "--omit-characters", action="store_true",
                        help="replace all ASCII characters with whitespace", default=False)
    parser.add_argument("-d", "--edge-detection", action="store_true",
                    help="use laplace edge detection filter on original image", default=False)
    parser.add_argument("-e", "--edge-enhance", action="store_true",
                        help="enhance edges and countours of the image", default=False)
    # Parse the command-line arguments
    args = parser.parse_args()
    scale_factor = args.scale if args.scale else 1.0
    fg_color = args.foreground_color
    bg_color = args.background_color
    omit_ascii = args.omit_characters
    # Process the image
    pixel_array = get_pixel_array(args.image_path)
    pixel_array = apply_image_filters(pixel_array, args)
    pixel_array = scale_image(pixel_array, scale_factor)
    ascii_text = convert_to_ascii(pixel_array)
    if (omit_ascii):
        ascii_text = ''.join([(' ' if char != '\n' else char)
                             for char in ascii_text])
    if (fg_color):
        ansi_fg = convert_fg_to_ansi(pixel_array)
    else:
        ansi_fg = ["" for _ in ascii_text]

    if (bg_color):
        ansi_bg = convert_bg_to_ansi(pixel_array)
    else:
        ansi_bg = ["" for _ in ascii_text]
    final_ascii_text = ""
    for i in range(len(ascii_text)):
        final_ascii_text += f"{ansi_bg[i]}{ansi_fg[i]}{ascii_text[i]}\033[0m"
    print(final_ascii_text)


if __name__ == "__main__":
    main()
