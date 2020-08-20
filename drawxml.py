#!/usr/bin/python

# Parse an OCRopus zone output XML.
# Draw zones onto an image.
# davep 21-Jan-2013

import sys
import os
import Image
import ImageDraw

import gtruthxml
from basename import get_basename

def load_image( imgfilename ) : 
    img = Image.open(imgfilename)
    img.load()
    if img.mode != "RGB" :
        img2 = img.convert("RGB")
        img = img2
        del img2

    return img

def draw_zones( xmlfilename, imgfilename, outfilename=None )