from PIL import Image
from math import floor
import os

# Predefined Shader Arrays
shaders = {
    '4bpp_StyleA': [' ', '.', ':', '#'],
    '8bpp_StyleA': [' ', '.', ':', '-', '=', '+', '*', '#', '@'],
    'unicode_izzy': [' ', '`', '.', ',', '-', ':', 'o', '^', 'F', 'X', '&', 'M', 'W', '#', '@', '█'],
    # add more styles
}

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
    
    for pixel_value in pixels:
        if invert:
            pixel_value = 255 - pixel_value
        index = int((pixel_value * (levels - 1)) / 255)
        ascii_str += shader[index]
        
    ascii_str_len = len(ascii_str)
    ascii_img = ''
    
    for i in range(0, ascii_str_len, num_cols):
        ascii_img += ':' + ascii_str[i:i+num_cols] + '\n'  # Added colon at the beginning
        
    # Extract filename and write to file
    filename, _ = os.path.splitext(os.path.basename(image_path))
    with open(f'{filename}.txt', 'w', encoding='utf-8') as f:
        f.write(ascii_img)

# Usage
# izzy for JICAF is rendered as white on black A3 size, specs: 0.6 line height, 92 columns.
image_to_ascii('image0.jpg', 92, 'unicode_izzy', line_height=0.6, invert=False, normalize=False)