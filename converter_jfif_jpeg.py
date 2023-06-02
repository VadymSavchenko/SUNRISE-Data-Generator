import os
from PIL import Image


# Sometimes Bing AI returns .jfif or .png files instead of .jpg
# Use this to convert .jfif and .png files to .jpg
def convert_to_jpg(source_dir, dest_dir):
    # Make the destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    # Get a list of all .jfif and .png files in the source directory
    image_files = [f for f in os.listdir(source_dir) if f.endswith('.jfif') or f.endswith('.png')]

    # Convert each .jfif or .png file to .jpg
    for image_file in image_files:
        img = Image.open(os.path.join(source_dir, image_file))

        # Change the file extension to .jpg
        jpg_file = os.path.splitext(image_file)[0] + '.jpg'

        # Save the image in the new format
        img.save(os.path.join(dest_dir, jpg_file))

        print(f'{image_file} has been converted to {jpg_file} and saved in {dest_dir}.')


if __name__ == '__main__':
    source = r'shop_images\Drill'  # Change this to your source directory
    destination = source + r'\jpg'
    convert_to_jpg(source, destination)
