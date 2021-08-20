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

    print "make_strips shape=",data.shape
    strip_list = []
    total_num_rows = data.shape[0] 
    while start_idx < total_num_rows : 
        # kill any previous reference to something in the strip_list
        s = None 

        s = data[start_idx:end_idx,:] 
        print "start={0} end={1} s={2}".format( start_idx, end_idx, s.shape )
        strip_list.append( s ) 

        outfilename = output_dir + "/" + outfilename_fmt.format( 
                basename, num_rows_in_strip, num_rows_to_slide, start_idx )
        print outfilename
        write_image( s, outfilename )
                
    