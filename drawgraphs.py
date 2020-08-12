
#!/usr/bin/python

# Load ocropus output metric dat files. Draw many delightful graphs.
# davep 09-Feb-2013
#
# If I had more forethought, I would have done this as a Makefile :-/
# davep 14-Feb-2013

import os
import sys
import csv
import numpy as np
#import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
import itertools
import Image

from basename import get_basename
import datfile

winder_imgclass_list = ( 
    "Double_Column",
    "Magazine",
    "Single_Column",
    "Double_Column_Pictures",
    "Mixed_Columns",
    "Single_Column_Pictures",
    "Double_Column_Pictures_Scientific",
    "Mixed_Columns_Pictures" )

# shorthand (used in drawing the barcharts; must match the order in
# winder_imgclass_list)
winder_imgclass_list_shorthand = ( "DC", "M", "SC", "DCP", "MC", "SCP", "DCS", "MCP" )

# classes in the UW dataset
uwiii_imgclass_list = ( "A", "C", "D", "E", "H", "I", 
                        "J", "K", "N", "S", "V", "W", )

dataset_list = ( "winder", "uwiii" )
stripsize_list = ( "300", "600", "fullpage" )
algorithm_list = ( "rast", "vor" )

def make_histogram( metrics, outfilename, **kargs ) : 
    
    adjmetrics = np.nan_to_num(metrics)
    nonzero = np.where( adjmetrics != 0 )

#    foo = plt.hist( adjmetrics[nonzero], bins=100, normed=True )
#    plt.show()

    fig = Figure()

    if "title" in kargs : 
        fig.suptitle(kargs["title"])

    ax = fig.add_subplot(111)
    ax.grid()
    ax.hist(np.nan_to_num(metrics),bins=25)
#    ax.hist(np.nan_to_num(metrics),bins=25,normed=True)

    ax.set_xlabel( "Metric" )

    ax.set_xlim(0,1.0)

    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfilename)
    print "wrote", outfilename