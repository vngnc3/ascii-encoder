from PIL import Image
from math import floor
from tqdm import tqdm
import os

# ⚠️ Remember to run pip install -r requirements.txt before running

# Predefined Shader Arrays
shaders = {
    '4bpp_StyleA': [' ', '.', ':', '#'],
    '8bpp_StyleA': [' ', '.', ':', '-', '=', '+', '*', '#', '@'],
    'unicode_izzy': [' ', '`', '.', ',', '-', ':', 'o', '^', 'F', 'X', '&', '#', 'W', 'M', '@', '█'],
    # add more styles
}

# Render Settings
shader = "unicode_izzy"
column = 48
lineHeight = 0.5
invert = False
normalize = False
overwrite = True

def create_folders():
    # Check if the input and output folders already exist to avoid unnecessary directory creation
    if not os.path.exists('input'):
        os.makedirs('input')
    if not os.path.exists('output'):
        os.makedirs('output')

def log_to_stdout(log_type, message):
    """
    Log messages to standard output based on the log type.

    Args:
    log_type (str): Type of log, either 'error' or 'warn'.
    message (str): The message to log.
    """
    if log_type == 'error':
        print(f"🚫 ERROR: {message}")
    elif log_type == 'warn':
        print(f"⚠️ WARNING: {message}")
    else:
        print(f"🔷 LOG ({log_type}): {message}")

def image_to_ascii(image_path, num_cols, shader_key, line_height=1, invert=False, normalize=False):
    image = Image.open(image_path)
    orig_width, orig_height = image.size

    # Calculate number of rows based on the aspect ratio and line height
    num_rows = floor(orig_height / orig_width * num_cols * line_height)
    
    # Resize and convert to grayscale
    image = image.resize((num_cols, num_rows))
    image = image.convert('L')
    
    shader = shaders[shader_key]
    levels = len(shader)
    
    pixels = list(image.getdata())
    
    if normalize:
        min_pixel = min(pixels)
        max_pixel = max(pixels)
        pixels = [(x - min_pixel) * 255 // (max_pixel - min_pixel) for x in pixels]
    
    ascii_str = ''
    # total_pixels = len(pixels)
    # progress_bar = tqdm(total=total_pixels, desc="🧠 Converting image to ASCII")
    
    for pixel_value in pixels:
        if invert:
            pixel_value = 255 - pixel_value
        index = int((pixel_value * (levels - 1)) / 255)
        ascii_str += shader[index]
        # progress_bar.update(1)
    # progress_bar.close()
    
    ascii_str_len = len(ascii_str)
    ascii_img = ''
    
    for i in range(0, ascii_str_len, num_cols):
        ascii_img += ':' + ascii_str[i:i+num_cols] + '\n'  # Added colon at the beginning
        
    # Extract filename and write to file
    filename, _ = os.path.splitext(os.path.basename(image_path))
    with open(f'{filename}.txt', 'w', encoding='utf-8') as f:
        f.write(ascii_img) 

def batch_convert_images_to_ascii(num_cols, shader_key, line_height=1, invert=False, normalize=False, overwrite=False):
    # Ensure the input and output directories are present
    create_folders()
    
    # List all images in the input directory
    input_folder = 'input'
    output_folder = 'output'
    image_files = os.listdir(input_folder)
    
    if not image_files:  # Check if the input folder is empty
        log_to_stdout("error", "No images found in the input folder. Please add some image files.")
        return
    
    log_to_stdout("info", f"Processing {len(image_files)} images.")
    # Using tqdm to track progress
    progress = tqdm(total=len(image_files), desc="🧠 Converting images to ASCII")
    for file_name in image_files:
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_folder, file_name)
            base_name, _ = os.path.splitext(file_name)
            ascii_file_name = f'{base_name}_ascii_{num_cols}.txt'
            output_path = os.path.join(output_folder, ascii_file_name)
            
            # Check if the ASCII file already exists in the output folder
            if os.path.exists(output_path):
                if overwrite:
                    log_to_stdout("warn", f"Overwriting existing file {file_name} in the output folder.")
                    # Delete the existing file to ensure a clean write
                    os.remove(output_path)
                else:
                    log_to_stdout("warn", f"Skipping {file_name} as it already exists in the output folder.")
                    progress.update(1)
                    continue
            
            # Generate ASCII art from the image
            image_to_ascii(input_path, num_cols, shader_key, line_height, invert, normalize)
            progress.update(1)
            
            # Move the generated ASCII file to the output folder with a modified name
            os.rename(f'{base_name}.txt', output_path)
    
    progress.close()
    log_to_stdout("info", f"Done processing {len(image_files)} images.")

# Single Usage
# image_to_ascii('image0.jpg', 96, 'unicode_izzy', line_height=0.6, invert=False, normalize=False)

# Batch Usage (default)
batch_convert_images_to_ascii(column, shader, lineHeight, invert, normalize, overwrite)
