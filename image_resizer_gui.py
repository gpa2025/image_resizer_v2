"""
Image Resizer GUI

A graphical user interface for resizing images in various formats.
Supports JPG, PNG, GIF, BMP, TIFF, and WEBP formats.

Author: Gianpaolo Albanese
Email: albaneg@yahoo.com
Version: 2
Date: May 8th 2025
Assisted by: Amazon Q for VS Code
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
from pathlib import Path
import threading
import queue


class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer v2")
        self.root.geometry("600x550")  # Increased height for about info
        self.root.resizable(True, True)
        
        # Application info
        self.app_info = {
            "name": "Image Resizer",
            "version": "2",
            "author": "Gianpaolo Albanese",
            "email": "albaneg@yahoo.com",
            "date": "May 8th 2025",
            "assisted_by": "Amazon Q for VS Code"
        }
        
        # Set icon if available
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        self.input_folder = ""
        self.output_folder = ""
        self.width = tk.StringVar(value="800")
        self.height = tk.StringVar(value="600")
        self.percentage = tk.StringVar(value="50")
        self.resize_mode = tk.StringVar(value="dimensions")
        self.maintain_aspect_ratio = tk.BooleanVar(value=True)
        self.progress_queue = queue.Queue()
        self.processing = False
        
        self.create_widgets()
        self.update_progress()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input folder selection
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Input Folder:").pack(side=tk.LEFT)
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(input_frame, text="Browse...", command=self.browse_input).pack(side=tk.RIGHT)
        
        # Output folder selection
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="Output Folder:").pack(side=tk.LEFT)
        self.output_entry = ttk.Entry(output_frame)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text="Browse...", command=self.browse_output).pack(side=tk.RIGHT)
        
        # Resize mode selection
        mode_frame = ttk.Frame(main_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(mode_frame, text="Resize Mode:").pack(side=tk.LEFT)
        
        # Radio buttons for resize mode
        dimensions_radio = ttk.Radiobutton(mode_frame, text="Dimensions", 
                                          variable=self.resize_mode, value="dimensions",
                                          command=self.toggle_resize_mode)
        dimensions_radio.pack(side=tk.LEFT, padx=5)
        
        percentage_radio = ttk.Radiobutton(mode_frame, text="Percentage", 
                                          variable=self.resize_mode, value="percentage",
                                          command=self.toggle_resize_mode)
        percentage_radio.pack(side=tk.LEFT, padx=5)
        
        # Size settings - Dimensions
        self.dimensions_frame = ttk.Frame(main_frame)
        self.dimensions_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.dimensions_frame, text="Width:").pack(side=tk.LEFT)
        width_entry = ttk.Entry(self.dimensions_frame, textvariable=self.width, width=6)
        width_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.dimensions_frame, text="Height:").pack(side=tk.LEFT, padx=(10, 0))
        height_entry = ttk.Entry(self.dimensions_frame, textvariable=self.height, width=6)
        height_entry.pack(side=tk.LEFT, padx=5)
        
        # Maintain aspect ratio checkbox
        aspect_check = ttk.Checkbutton(self.dimensions_frame, text="Maintain aspect ratio", 
                                       variable=self.maintain_aspect_ratio)
        aspect_check.pack(side=tk.LEFT, padx=(20, 0))
        
        # Size settings - Percentage
        self.percentage_frame = ttk.Frame(main_frame)
        
        ttk.Label(self.percentage_frame, text="Percentage:").pack(side=tk.LEFT)
        percentage_entry = ttk.Entry(self.percentage_frame, textvariable=self.percentage, width=6)
        percentage_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.percentage_frame, text="%").pack(side=tk.LEFT)
        
        # Progress bar and status
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_bar = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack(fill=tk.X, side=tk.TOP)
        
        self.status_label = ttk.Label(progress_frame, text="Ready")
        self.status_label.pack(fill=tk.X, side=tk.TOP, pady=5)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # About section
        about_frame = ttk.LabelFrame(main_frame, text="About")
        about_frame.pack(fill=tk.X, pady=5)
        
        about_text = f"{self.app_info['name']} v{self.app_info['version']}\n"
        about_text += f"Author: {self.app_info['author']}\n"
        about_text += f"Email: {self.app_info['email']}\n"
        about_text += f"Date: {self.app_info['date']}\n"
        about_text += f"Assisted by: {self.app_info['assisted_by']}"
        
        about_label = ttk.Label(about_frame, text=about_text, justify=tk.LEFT)
        about_label.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="About", command=self.show_about).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Start Resizing", command=self.start_resizing).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def browse_input(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder = folder
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, folder)
            self.log(f"Input folder set to: {folder}")
    
    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, folder)
            self.log(f"Output folder set to: {folder}")
    
    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def update_progress(self):
        """Check for progress updates from the worker thread"""
        try:
            while True:
                message_type, message = self.progress_queue.get_nowait()
                
                if message_type == "progress":
                    current, total = message
                    if total > 0:
                        progress = (current / total) * 100
                        self.progress_bar["value"] = progress
                        self.status_label["text"] = f"Processing: {current}/{total} images ({int(progress)}%)"
                
                elif message_type == "log":
                    self.log(message)
                
                elif message_type == "complete":
                    self.progress_bar["value"] = 100
                    self.status_label["text"] = "Complete!"
                    self.processing = False
                    messagebox.showinfo("Complete", f"Successfully processed {message} images!")
                
                elif message_type == "error":
                    self.status_label["text"] = "Error occurred"
                    self.processing = False
                    messagebox.showerror("Error", message)
                
                self.progress_queue.task_done()
                
        except queue.Empty:
            pass
        finally:
            # Schedule the next update
            self.root.after(100, self.update_progress)
    
    def toggle_resize_mode(self):
        """Toggle between dimensions and percentage resize modes"""
        if self.resize_mode.get() == "dimensions":
            self.dimensions_frame.pack(fill=tk.X, pady=5)
            self.percentage_frame.pack_forget()
        else:
            self.dimensions_frame.pack_forget()
            self.percentage_frame.pack(fill=tk.X, pady=5)
            
    def show_about(self):
        """Show about dialog with application information"""
        about_text = f"{self.app_info['name']} v{self.app_info['version']}\n\n"
        about_text += f"A simple utility to resize JPG images from an input folder\n"
        about_text += f"and save them to an output folder.\n\n"
        about_text += f"Author: {self.app_info['author']}\n"
        about_text += f"Email: {self.app_info['email']}\n"
        about_text += f"Date: {self.app_info['date']}\n\n"
        about_text += f"Assisted by: {self.app_info['assisted_by']}"
        
        messagebox.showinfo("About Image Resizer", about_text)
    
    def start_resizing(self):
        """Start the image resizing process in a separate thread"""
        if self.processing:
            messagebox.showinfo("Processing", "Already processing images. Please wait.")
            return
            
        # Get input values
        input_folder = self.input_entry.get().strip()
        output_folder = self.output_entry.get().strip()
        
        # Validate resize parameters based on mode
        resize_mode = self.resize_mode.get()
        width = None
        height = None
        percentage = None
        
        try:
            if resize_mode == "dimensions":
                width = int(self.width.get())
                height = int(self.height.get())
                if width <= 0 or height <= 0:
                    raise ValueError("Width and height must be positive integers")
            else:  # percentage mode
                percentage = float(self.percentage.get())
                if percentage <= 0:
                    raise ValueError("Percentage must be a positive number")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
            
        # Validate folders
        if not input_folder:
            messagebox.showerror("Error", "Please select an input folder")
            return
            
        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder")
            return
            
        if not os.path.isdir(input_folder):
            messagebox.showerror("Error", f"Input folder does not exist: {input_folder}")
            return
            
        # Create output directory if it doesn't exist
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
                self.log(f"Created output directory: {output_folder}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output directory: {str(e)}")
                return
                
        # Reset progress
        self.progress_bar["value"] = 0
        self.status_label["text"] = "Starting..."
        self.processing = True
        
        # Start processing thread
        threading.Thread(
            target=self.process_images_thread,
            args=(input_folder, output_folder, width, height, 
                  self.maintain_aspect_ratio.get(), percentage),
            daemon=True
        ).start()
    
    def process_images_thread(self, input_folder, output_folder, width, height, maintain_aspect, percentage=None):
        """Process images in a separate thread to keep the UI responsive"""
        try:
            # Get all supported image files in the input directory
            input_path = Path(input_folder)
            supported_extensions = ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*.tif", "*.webp"]
            
            image_files = []
            for ext in supported_extensions:
                image_files.extend(list(input_path.glob(ext)))
                # Also check for uppercase extensions
                image_files.extend(list(input_path.glob(ext.upper())))
            
            if not image_files:
                self.progress_queue.put(("log", f"No supported images found in {input_folder}"))
                self.progress_queue.put(("log", f"Supported formats: JPG, PNG, GIF, BMP, TIFF, WEBP"))
                self.progress_queue.put(("complete", 0))
                return
                
            total_files = len(image_files)
            self.progress_queue.put(("log", f"Found {total_files} images to process"))
            
            # Process each image
            for i, image_file in enumerate(image_files, 1):
                output_path = os.path.join(output_folder, image_file.name)
                
                try:
                    with Image.open(image_file) as img:
                        original_width, original_height = img.size
                        
                        if percentage is not None:
                            # Calculate new dimensions based on percentage
                            scale_factor = percentage / 100.0
                            new_width = int(original_width * scale_factor)
                            new_height = int(original_height * scale_factor)
                            resize_type = f"{percentage}% ({new_width}x{new_height})"
                        else:
                            # Calculate new size if maintaining aspect ratio
                            if maintain_aspect:
                                aspect_ratio = original_width / original_height
                                
                                if original_width > original_height:
                                    new_width = width
                                    new_height = int(width / aspect_ratio)
                                else:
                                    new_height = height
                                    new_width = int(height * aspect_ratio)
                            else:
                                new_width, new_height = width, height
                            
                            resize_type = f"{new_width}x{new_height}"
                        
                        # Resize the image
                        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # Save the resized image
                        resized_img.save(output_path)
                        
                        self.progress_queue.put(("log", f"Resized: {image_file.name} -> {resize_type}"))
                except Exception as e:
                    self.progress_queue.put(("log", f"Error processing {image_file}: {e}"))
                
                # Update progress
                self.progress_queue.put(("progress", (i, total_files)))
            
            self.progress_queue.put(("complete", total_files))
            
        except Exception as e:
            self.progress_queue.put(("error", str(e)))


def main():
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()