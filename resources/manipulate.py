import os

import random
from PIL import Image


def convert_to_pixel_art(input_path, output_path, pixel_size=10, colors=64):
    """
    Converts an image to pixel art by resizing, reducing colors, and saving the result.

    Parameters:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the pixel art output.
        pixel_size (int): Size of the pixels for the pixel art effect.
        colors (int): Number of colors to use in the final image (e.g., 64).
    """
    # Open the original image
    img = Image.open(input_path)

    # Resize the image down to create the pixelation effect
    img_small = img.resize(
        (img.width // pixel_size, img.height // pixel_size),
        resample=Image.Resampling.NEAREST,
    )

    # Resize it back up to the original size to scale up the pixel blocks
    img_pixelated = img_small.resize(
        (img.width, img.height), resample=Image.Resampling.NEAREST
    )

    # Reduce the number of colors to create a more stylized, "pixel art" look
    img_pixelated = img_pixelated.convert(
        "P", palette=Image.Palette.ADAPTIVE, colors=colors
    )

    # Save the pixelated image
    img_pixelated.save(output_path)
    print(f"Pixel art saved to {output_path}")


def convert_folder_to_pixel_art(input_path, output_path, pixel_size=2, colors=64):
    """
    Converts an image to pixel art by resizing, reducing colors, and saving the result.

    Parameters:
        input_path (str): Path to the input image file.
        output_path (str): Path to save the pixel art output.
        pixel_size (int): Size of the pixels for the pixel art effect.
        colors (int): Number of colors to use in the final image (e.g., 64).
    """
    # Walk through each file in the input directory
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_path)
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_path)

    for root, _, files in os.walk(input_dir):
        # Calculate the relative path for the current folder and prepare the output folder
        os.makedirs(output_dir, exist_ok=True)

        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):

                base_file_name = os.path.basename(file)
                f_base = os.path.splitext(base_file_name)[0]
                f_ext = os.path.splitext(base_file_name)[1]

                input_path = os.path.join(root, file)
                output_path = os.path.join(output_dir, f"{f_base}-pixel{f_ext}")

                convert_to_pixel_art(input_path, output_path, pixel_size, colors)


def pixel_manipulate(
    input_path, output_base_path, manipulation_function, repeat_rate=1
):
    """
    Opens an image, applies pixel-wise manipulation multiple times, and saves each result.

    Parameters:
        input_path (str): Path to the input image file.
        output_base_path (str): Base path for output images. Each result will have a unique name.
        manipulation_function (function): A function that takes a pixel (R, G, B) tuple
                                          and returns a new (R, G, B) tuple.
        repeat_rate (int): Number of times to apply the manipulation and save intermediate results.
    """

    # Ensure the output directory exists
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), output_base_path
    )
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Open the original image
    input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_path)
    img = Image.open(input_path).convert("RGB")

    for i in range(1, repeat_rate + 1):
        # Copy the image for manipulation in this iteration
        img_copy = img.copy()
        pixels = img_copy.load()

        # Iterate over each pixel
        for y in range(img_copy.height):
            for x in range(img_copy.width):
                original_pixel = pixels[x, y]
                pixels[x, y] = manipulation_function(original_pixel)

        # Save the modified image with a unique filename
        output_path = f"{output_dir}/back_iteration_{i}.png"
        img_copy.save(output_path)
        print(f"Saved iteration {i} as {output_path}")


# Example manipulation function: Brightness adjustment
def rand_changes(pixel, factor=0.05):
    r, g, b = pixel
    u = random.uniform(-1, 1)
    return (
        min(int(r + r * u * factor), 255),
        min(int(g + g * u * factor), 255),
        min(int(b + b * u * factor), 255),
    )


if __name__ == "__main__":
    # Example usage

    pixel_manipulate(
        "design_3_ufo_attack.png",
        "back_pixel",
        lambda pixel: rand_changes(pixel, factor=0.08),
        repeat_rate=10,
    )

    # convert_folder_to_pixel_art('back_pixel_tmp', 'back_pixel', 1, 256)
