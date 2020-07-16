
#!python

# Load a .dat file which is our output of runseg.py
# Moved into own module so can call from oodles of other python scripts.
#
# davep 13-Feb-2013

import sys
import os
import numpy as np
import csv
import pickle
import sqlite3

from basename import get_basename

dataset_list = ( "winder", "uwiii" )
stripsize_list = ( "300", "600", "fullpage" )
algorithm_list = ( "rast", "vor" )

def load( datfile_name ) :
    
    infile = open(datfile_name,"r")
    reader = csv.reader( infile, delimiter=' ')
    data = [ float(row[2]) for row in reader ] 
    infile.close()

    return np.nan_to_num(np.asarray( data, dtype="float" ))

def find_all( dirname ) : 
    # sweep a path (like 'find') and gather all .dat filenames
    datfile_list = []
    for root,dirs,files in os.walk(dirname) :
#        print "root=",root
#        print "dirs=",dirs
#        print "files=",files
        for f in files : 
            path=os.path.join(root,f)
            if path.endswith(".dat") : 
                datfile_list.append( path ) 

    return datfile_list

def load_all_data(root) : 
    fullpage_winder = find_all(root)

    data_list = []
    path_list = []
    for datfilename in fullpage_winder : 
        ndata = load(datfilename)