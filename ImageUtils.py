"""
This module contains various image utilities.
"""
from PIL import Image, ImageChops

import os


def convert_heic_directory(path: str) ->list[str]:
    '''
    Convert all .HEIC image(s) in specified folder to jpg.
    Output files will be in the same folder as the original HEIC images.

    Parameters:
    path: path to a folder

    Return:
    List of path of converted file(s).

    Raises:
    FileNotFoundError if input path is invalid.
    '''
    import glob
    changed = False
    # First see if we need to switch folder
    cwd = os.getcwd()

    if not (path == cwd) and not (path == '.'):
        os.chdir(path)
        changed = True

    file_list = []

    for file in os.listdir():
        if file.upper().endswith('HEIC'):
            file_name = convert_heic(file)
            file_list.append(file_name)

    if changed == True:
        os.chdir(cwd)

    return file_list

def convert_heic(imagepath: str) -> str:
    '''
    Convert single .HEIC image to jpg.

    Parameters:
    imagepath: path to a single HEIC image

    Return:
    Path of converted file.

    Raises:
    FileNotFoundError if input path is invalid.
    '''

    from pillow_heif import register_heif_opener
    register_heif_opener()
    cwd = os.getcwd()

    if not os.path.splitext(imagepath)[1][1:].upper() == 'HEIC':
        print(f'{imagepath} does not have the HEIC extension')
        return

    #print(f'convert: {imagepath}')

    try:
        image = Image.open(imagepath)
    except FileNotFoundError as e:
        print(f'Whoops: {e}')
        return None

    rgb = image.convert("RGB")
    image.close()
    outpath = f'{os.path.join(cwd, imagepath)}.jpg'
    rgb.save(f'{outpath}')
    return outpath

def compare_images(img1_path: str, img2_path: str, output = False) ->dict[str, str, str]:
    """
    Compare two images and optionally produce an image of the differences.

    Parameters
        img1_path: Path to the first image.
        img2_path: Path to the second image.
        output: True to create image file of the diffs.  False by default.
    
    Return: 
        pixel_match: percent of matching pixles
        color_match: average of the Euclidian difference in the pixel RGB.
        file_name: name of optional image file created.

    Raises:
        FileNotFoundError if input path is invalid.
        OSError if output image cannot be created.
    """
    import numpy as np
    # Open the images
    try:
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')
    except FileNotFoundError as e:
        print(f'WTF: {e}')
        return None
    
    # Resize the images to the same size (if necessary)
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)

    # Convert images to numpy arrays
    arr1 = np.array(img1)
    arr2 = np.array(img2)

    # Compare pixels and calculate the percentage of matches
    matching_pixels = np.sum(np.all(arr1 == arr2, axis=-1))  # Compare RGB values

    match_percentage = (matching_pixels / (img1.size[0] * img1.size[1])) * 100
    
    # Calculate the difference between the two images in RGB space
    color_diff = np.linalg.norm(arr1 - arr2, axis=-1)  # Euclidean distance for each pixel RGB
    
    # Calculate the average color difference
    avg_color_diff = np.mean(color_diff)
    
    output_filename = None
    if output == True:
        # Create an image file (of the same input type) of the differences.
        # Invert the image first to avoid all black for the matching pixels.
        diff = ImageChops.invert(ImageChops.difference(img1, img2))
        filename1 = os.path.splitext(os.path.basename(img1_path))[0]
        filename2 = os.path.splitext(os.path.basename(img2_path))[0]
        extension = os.path.splitext(os.path.basename(img2_path))[1]
        output_filename = f'{filename1}_{filename2}{extension}'
        try:
            diff.save(output_filename)
        except OSError as e:
            print(f'Error: {e}')
            return None

    ret = {'pixel_match': match_percentage, 'color_match': avg_color_diff, 'output_file': output_filename}
    return ret


    
    
    

