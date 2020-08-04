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
        del img
        img = img2

    return img

def draw_boxes( boxfilename, outdir=None) : 

    box_list = zonebox.load_boxes(boxfilename)

    print box_list

    # get the document id from the box file
#    imgfilename = "IMAGEBIN/{0}BIN.TIF".format( box_list[0].document_id )
    imgfilename = "IMAGEBIN/{0}BIN.png".format( box_list[0].document_id )

    # write the output image to this file and perhaps to another directory
    if not outdir is None : 
        outfilename = outdir + "/" + get_basename(imgfilename) + "_zoneboxes.png"
    else :
        outfilename = get_basename(img