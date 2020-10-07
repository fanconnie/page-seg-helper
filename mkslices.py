#!python

# Load an image. Break apart into multiple images of 1", 2", 3", 4", 6" strips.
# davep 29-Jan-2013

import sys
import os
import numpy as np
import Image

from basename import get_basename

def make_slices( da