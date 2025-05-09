"""
Image Resizer

This script resizes images from an input folder and saves them to an output folder.
Supports multiple image formats (JPG, PNG, GIF, BMP, TIFF, WEBP) and both fixed dimensions 
and percentage-based resizing.

Author: Gianpaolo Albanese
Email: albaneg@yahoo.com
Version: 2
Date: May 8th 2025
Assisted by: Amazon Q for VS Code
"""

import os
import sys
import argparse
from PIL import Image
from pathlib import Path


def create_directory(directory_path):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")


def resize_image(input_path, output_path, size=None, percentage=None):
    """
    Resize an image and save it to the output path.
    
    Args:
        input_path: Path to the input image
        output_path: Path where the resized image will be saved
        size: Tuple of (width, height) for the new size, or None if using percentage
        percentage: Percentage to resize the image, or None if using fixed dimensions
    """
    try:
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            
            if percentage is not None:
                # Calculate new dimensions based on percentage
                scale_factor = percentage / 100.0
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                new_size = (new_width, new_height)
                resize_type = f"{percentage}% ({new_width}x{new_height})"
            else:
                # Use the provided fixed dimensions
                new_size = size
                resize_type = f"{size[0]}x{size[1]}"
            
            # Resize the image
            resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
            # Save the resized image
            resized_img.save(output_path)
            print(f"Resized: {os.path.basename(input_path)} -> {resize_type}")
    except Exception as e:
        print(f"Error processing {input_path}: {e}")


def process_images(input_folder, output_folder, width=None, height=None, percentage=None):
    """
    Process all JPG images in the input folder and save resized versions to the output folder.
    
    Args:
        input_folder: Path to the folder containing images to resize
        output_folder: Path to the folder where resized images will be saved
        width: Width of the resized images (if using fixed dimensions)
        height: Height of the resized images (if using fixed dimensions)
        percentage: Percentage to resize the images (if using percentage-based resizing)
    """
    # Create output directory if it doesn't exist
    create_directory(output_folder)
    
    # Get all supported image files in the input directory
    input_path = Path(input_folder)
    supported_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.tif", "*.webp"]
    
    image_files = []
    for ext in supported_extensions:
        image_files.extend(list(input_path.glob(ext)))
        # Also check for uppercase extensions
        image_files.extend(list(input_path.glob(ext.upper())))
    
    if not image_files:
        print(f"No supported images found in {input_folder}")
        print(f"Supported formats: JPG, PNG, GIF, BMP, TIFF, WEBP")
        return
    
    print(f"Found {len(image_files)} images to process")
    
    # Process each image
    for image_file in image_files:
        output_path = os.path.join(output_folder, image_file.name)
        
        if percentage is not None:
            resize_image(str(image_file), output_path, percentage=percentage)
        else:
            resize_image(str(image_file), output_path, size=(width, height))
    
    print(f"Finished processing {len(image_files)} images")


def main():
    """Main function to handle command line arguments and start processing."""
    # Create a custom epilog with author information
    epilog = """
Author: Gianpaolo Albanese
Email: albaneg@yahoo.com
Version: 2
Date: May 8th 2025
    """
    
    parser = argparse.ArgumentParser(
        description="Resize images from an input folder to an output folder. Supports JPG, PNG, GIF, BMP, TIFF, and WEBP formats.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("input_folder", help="Path to the folder containing images to resize")
    parser.add_argument("output_folder", help="Path to the folder where resized images will be saved")
    
    # Create a mutually exclusive group for resize options
    resize_group = parser.add_mutually_exclusive_group(required=True)
    resize_group.add_argument("-d", "--dimensions", nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'),
                             help="Resize to specific dimensions (width height)")
    resize_group.add_argument("-p", "--percentage", type=float,
                             help="Resize by percentage (e.g., 50 for 50%%)")
    parser.add_argument("-v", "--version", action="version", 
                       version="Image Resizer v2 by Gianpaolo Albanese")
    
    args = parser.parse_args()
    
    # Validate input folder
    if not os.path.isdir(args.input_folder):
        print(f"Error: Input folder '{args.input_folder}' does not exist")
        return
    
    # Process based on the chosen resize method
    if args.dimensions:
        width, height = args.dimensions
        if width <= 0 or height <= 0:
            print("Error: Width and height must be positive integers")
            return
        process_images(args.input_folder, args.output_folder, width=width, height=height)
    else:
        percentage = args.percentage
        if percentage <= 0:
            print("Error: Percentage must be a positive number")
            return
        process_images(args.input_folder, args.output_folder, percentage=percentage)


if __name__ == "__main__":
    main()