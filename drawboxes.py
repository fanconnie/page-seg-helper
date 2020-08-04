#!python

# Read UW-III .BOX file. Draw onto an image.
# davep 24-Jan-2013

import sys
import os
import Image
import ImageDraw
#import numpy as np

import zonebox
from basename import get_basename

def load_image( imgfilename ) : 
    # load the image
    img = Image.open(imgfilename)
    img.load()

    # if not RGB, make RGB so we can draw our outlines in color
    if img.mode != "RGB" : 
        img2 = img.convert("RGB")
        