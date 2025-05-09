"""
Build script to create an executable for the Image Resizer application.

Author: Gianpaolo Albanese
Email: albaneg@yahoo.com
Version: 2
Date: May 8th 2025
Assisted by: Amazon Q for VS Code
"""

import PyInstaller.__main__
import os
import sys

# Determine if we're running the GUI or CLI version
if len(sys.argv) > 1 and sys.argv[1] == "--cli":
    print("Building CLI version...")
    script = "image_resizer.py"
    name = "ImageResizer_CLI"
else:
    print("Building GUI version...")
    script = "image_resizer_gui.py"
    name = "ImageResizer"

# Create the dist directory if it doesn't exist
if not os.path.exists("dist"):
    os.makedirs("dist")

# PyInstaller arguments
args = [
    script,
    "--name=" + name,
    "--onefile",
    "--clean",
    "--windowed" if script == "image_resizer_gui.py" else "",
    "--add-data=README.md;.",
]

# Run PyInstaller
PyInstaller.__main__.run(args)

print(f"\nBuild complete! Executable created at: dist/{name}.exe")