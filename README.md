# Image Resizer

A simple utility to resize images from an input folder and save them to an output folder.
Supports multiple image formats including JPG, PNG, GIF, BMP, TIFF, and WEBP.

**Author:** Gianpaolo Albanese  
**Email:** albaneg@yahoo.com  
**Version:** 2  
**Date:** May 8th 2025  
**Assisted by:** Amazon Q for VS Code

## Features

- Resize multiple images at once
- Supported formats:
  - JPEG/JPG
  - PNG
  - GIF
  - BMP
  - TIFF
  - WEBP
- Two resize options:
  - Specify custom width and height
  - Resize by percentage (preserves aspect ratio)
- Option to maintain aspect ratio when using dimensions (GUI version)
- Simple and intuitive graphical interface
- Also available as a command-line tool

## Installation

### Option 1: Download the Executable

1. Download the executable file (`dist\ImageResizer.exe`)
2. Run the executable directly - no installation required

### Option 2: Run from Source

1. Install Python 3.7 or higher
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the script:
   ```
   python image_resizer_gui.py
   ```

## Usage

### GUI Version

1. Launch the application
2. Click "Browse..." to select the input folder containing your JPG images
3. Click "Browse..." to select the output folder where resized images will be saved
4. Enter the desired width and height in pixels
5. Check "Maintain aspect ratio" if you want to preserve the original proportions
6. Click "Start Resizing"

### Command Line Version

Run the script with the following command:

```
python image_resizer.py <input_folder> <output_folder> [options]
```

#### Options:

- Resize by dimensions:
  ```
  python image_resizer.py ./input_images ./output_images -d 800 600
  ```
  This will resize all JPG images in the `input_images` folder to 800x600 pixels.

- Resize by percentage:
  ```
  python image_resizer.py ./input_images ./output_images -p 50
  ```
  This will resize all JPG images to 50% of their original size, preserving aspect ratio.

For help with all available options:
```
python image_resizer.py --help
```

## Building the Executable

To build the executable yourself:

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the build script:
   ```
   python build_exe.py
   ```
   
   This will create the GUI version by default. For the CLI version:
   ```
   python build_exe.py --cli
   ```

3. Find the executable in the `dist` folder# image_resizer_v2
