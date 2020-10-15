#!python

# Load an image. Break apart into multiple images of 1", 2", 3", 4", 6" strips.
# davep 29-Jan-2013

import sys
import os
import numpy as np
import Image

from basename import get_basename

def make_slices( data, num_rows_in_slice ) :
    # carve up the numpy array into N strips of num_rows each; return an array
    # of said strips

    start_idx = 0
    end_idx = start_idx + num_rows_in_slice

    print "make_slices shape=",data.shape
    slice_list = []
    total_num_rows = data.shape[0] 
    while start_idx < total_num_rows : 
        s = data[start_idx:end_idx,:]
