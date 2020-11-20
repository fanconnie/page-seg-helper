#!python

import numpy as np
import itertools

import datfile

def print_latex_table( outfilename, output_list ) :
    prefix ="""
    \\begin{tabular}{| l | l | l | l | }
    \\hline
    Name    &   Total Metrics & Zeros & \\% Non Zero \\\\
    \\hline"""

    data = """
    {name} & {count} & {zeros} & {percent:.2f} \\\\
    \\hline"""

    postfix = """
    \\end{tabular}"""

    outfile = open(outfilename,"w")
    print >>outfile, prefix,

    for s in output_list : 
#        print >>outfile, data.format( file["name"], file["size"], file["new_size"])
#        print >>outfile, data.format( s["name"], s["count"], s["zeros"], s["percent"] )
        print s["name"]
        print >>outfile, data.format(**s)
    
    print >>outfile, postfix


def count_zeros(dataset,algorithm,stripsize) : 

    metrics = datfile.load_metrics(dataset=dataset,algorithm=algorithm,stripsize=stripsize )

#    zeros = np.where(metrics==0)

    num_nonzero = np.count_nonzero(