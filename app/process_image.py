import numpy as np
from PIL import Image
import os

def create_and_save_grayscale(path_to_image):
    img = Image.open(path_to_image).convert('LA')

    img_name = os.path.basename(path_to_image)
    dot_index = img_name.index('.')
    grayscale_name = img_name[:dot_index] + "_grayscale" + img_name[dot_index:]
    grayscale_loc = os.path.join(os.path.dirname(path_to_image), grayscale_name)
    img.save(grayscale_loc)
    return grayscale_loc
