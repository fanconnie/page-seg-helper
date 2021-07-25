#!python

# Slice a window of N rows down an image by M rows (the slide) each step.
# Write each strip to an individual image file in a subdirectory.
#
# created for the page segmentation comparisson
#
# davep 5-Feb-2013

import sys
import numpy as np
import Image
import os

import mkslices
from basename import get_basename
import rects
import zonebox
import zone2xml
import gtruthxml

num_rows_in_strip = 600
num_rows_to_slide  = 20
#output_dir = str(num_rows_in_strip)

def write_image( data, outfilename ) : 
    img = Image.fromarray( data, mode="L" )
    img.save( outfilename ) 

def make_all_strips_images( data, basename, output_dir ) :
    # carve up the numpy array into N strips of num_rows each; return an array
    # of said strips

    start_idx = 0
    end_idx = start_idx + num_rows_in_strip

    outfilename_fmt = "{0}_{1:03}_{2:03}_{3:04}.png"

    print "mak