import os
import glob
import json
import random
from pathlib import Path
from difflib import SequenceMatcher
import shutil
from PIL import Image, ImageDraw, ImageFont
import cv2
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from IPython.display import display
import matplotlib
from matplotlib import pyplot, patches

sroie_folder_path = Path('/Users/alyshawang/Downloads/task1&2_test(361p)')
example_file = Path('X00016469670.jpg')
image = Image.open(
    "/Users/alyshawang/Downloads/task1&2_test(361p)/X00016469670.jpg")
image = image.convert("RGB")
new_image = image.resize((300, 600))
new_image


def read_bbox_and_words(path: Path):
    bbox_and_words_list = []

    with open(path, 'r') as f:
        for line in f.read().splitlines():
            split_lines = line.split(",")

            bbox = np.array(split_lines[0:8], dtype=np.int32)
            text = ",".join(split_lines[8:])

            # From the splited line we save (filename, [bounding box points], text line).
            # The filename will be useful in the future
            bbox_and_words_list.append([path.stem, *bbox, text])

    dataframe = pd.DataFrame(bbox_and_words_list, columns=[
                             'filename', 'x0', 'y0', 'x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'line'], dtype=np.int16)
    dataframe = dataframe.drop(columns=['x1', 'y1', 'x3', 'y3'])

    return dataframe


def read_last_lines(file_path, num_lines=10):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_lines = lines[-num_lines:]
    return ''.join(last_lines)
# Example usage


bbox_file_path = sroie_folder_path / \
    "0325updated.task1train(626p)" / example_file
print("== File content ==")
print(read_last_lines(bbox_file_path))

bbox = read_bbox_and_words(path=bbox_file_path)
print("\n== Dataframe ==\n")
bbox.head(5)
