#!python

import numpy as np
import itertools

import datfile

def print_latex_table( outfilename, output_list ) :
    prefix ="""
    \\begin{tabular}{| l | l | l | l | }
    \\hline
    Name    &   Total Metrics & Zeros & \\% Non Zero \\\\
 