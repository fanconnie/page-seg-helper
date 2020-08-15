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
    i