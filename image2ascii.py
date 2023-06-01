#! /bin/python3

import sys
import argparse
import numpy as np
from PIL import Image


def get_image_dimensions(image_path: str):
    with Image.open(image_path) as img:
        width, height = img.size
        return (width, height)


def get_pixel_buffer(image_path: str):
    with Image.open(image_path) as img:
        pixel_array = np.array(img)
        return pixel_array


def scale_image(pixel_array, scale_factor : float):
    img = Image.fromarray(pixel_array)
    target_width = int(img.width * scale_factor)
    target_height = int(img.height * scale_factor * 0.7)
    resized_img = img.resize((target_width, target_height))
    resized_array = np.array(resized_img)
    return resized_array

def get_ansii_color_array(pixel_array)-> str:
    
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


def main() -> None:
	parser = argparse.ArgumentParser(description="Image processing script")
	# Add the image path argument
	parser.add_argument("image_path", help="path to the image file")
	# Add the scale option
	parser.add_argument("-s", "--scale", type=float, help="scale factor to resize the image")
	# Parse the command-line arguments
	args = parser.parse_args()
	scale_factor = args.scale if args.scale else 1.0		
	# Process the image
	pixel_buff = get_pixel_buffer(args.image_path)
	pixel_buff = scale_image(pixel_buff, scale_factor)
	print(convert_to_ascii(pixel_buff))


if __name__ == "__main__":
    main()
