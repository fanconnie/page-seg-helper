
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

def load_all_datfiles( dirname ) : 
    metrics = None

    for root,dirs,files in os.walk(dirname) :
#        print "root=",root
#        print "dirs=",dirs
#        print "files=",files
        for f in files : 
            path=os.path.join(root,f)
            if path.endswith(".dat") : 
#                print "path=",os.path.join(root,f)
                ndata = datfile.load( path )
#                print ndata

                if metrics is None : 
                    metrics = ndata
                    ndata = None
                else :
                    metrics = np.append( metrics, ndata )

    return metrics

def plotit( data, outfilename, **kargs ) :

    # going to make a 1 row x N column plot
    if len(data.shape)==1 : 
        num_rows = 1
    else : 
        num_rows = data.shape[1]

    # davep 02-Oct-2012 ; bump up the size to accommodate multiple rows
    fig = Figure()
    figsize = fig.get_size_inches()
#    fig.set_size_inches( (figsize[0],figsize[1]*num_rows) )

    if "title" in kargs : 
        fig.suptitle(kargs["title"])

    # http://matplotlib.org/faq/howto_faq.html
    # "Move the edge of an axes to make room for tick labels"
    # hspace is "the amount of height reserved for white space between
    # subplots"
    fig.subplots_adjust( hspace=0.40 )

    ax = fig.add_subplot(111)
    ax.grid()
    ax.set_ylim(-0.1,1.1)

    label_iter = iter( ("Strip Metric","FullPage Metric","All Strips' Mean"))
    for i in range(num_rows) : 
        if num_rows==1 :
            column = data 
        else : 
            column = data[ :, i ] 

        fmt = kargs.get("fmt","+")
        if "color" in kargs : 
            fmt += kargs["color"]            
        ax.plot(column,fmt,label=label_iter.next())

    if "axis_title" in kargs : 
        title = kargs["axis_title"][i]
        ax.set_title(title)

    ax.legend(loc="lower left")

    ax.set_xlabel( "Strip Number" )
    ax.set_ylabel( "Match Metric" )

    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(outfilename)
    print "wrote", outfilename

def draw_single_pages() : 
    def make_lines(ndata,fullpage_metric) :
        # make horizontal data sets for metric and mean
        fullpage = np.ones_like(ndata) * fullpage_metric
        m = np.ones_like(ndata) * np.mean(ndata)
        print "mean=",np.mean(ndata)
        return np.column_stack((ndata,fullpage,m))

    base = "300_winder_rast/imagesAndgTruth/"
    # draw a few results from single pages
    outfilename = "winder_full_rast_double_2col300_1.png"
    if not os.path.exists(outfilename): 
        ndata = datfile.load(base+"Double_Column/300dpi/2col300_1/2col300_1.dat")
        plotit( make_lines(ndata,1.0),
                    outfilename, title="Winder RAST DoubleColumn 2col300_1", fmt="-" )

    outfilename = "winder_full_rast_double_pic_2col300_2.png"
    if not os.path.exists(outfilename): 
        ndata = datfile.load(base+"Double_Column_Pictures/300dpi/2colpic300_2/2colpic300_2.dat")
        plotit( make_lines(ndata,.78), outfilename, 
                title="Winder RAST Double Column Picture 2col300_2", 
                fmt="-" )

    outfilename = "winder_full_rast_double_sci_2col300_3.png"
    if not os.path.exists(outfilename): 
        ndata = datfile.load(base+"Double_Column_Pictures_Scientific/300dpi/2colpic300_3/2colpic300_3.dat")
        plotit( make_lines(ndata,.56), outfilename, 
                title="Winder RAST Double Column Scientific Picture 2col300_3", 
                fmt="-" )

def get_winder_class_results(class_dir) :
    # load all .dat files corresponding to each class of image in the Winder
    # data set

    # gather all the datafiles from the fullpage winder
    fullpage_winder = datfile.find_all(class_dir)

    class_data = []
    class_names = []
    for datfilename in fullpage_winder : 
        ndata = datfile.load(datfilename)
        basename = get_basename(datfilename)
        class_data.append( np.mean(ndata) )
        class_names.append( basename.replace( "_"," ") )

    return (class_data,class_names)

def draw_class_results_barchart(dataset,dataset_title) : 
    outfilename = "{0}_class_rast_vs_vor.png".format(dataset)

    if dataset=="uwiii" : 
        imgclass_list = uwiii_imgclass_list
        label_list = uwiii_imgclass_list
    elif dataset=="winder" :
        imgclass_list = winder_imgclass_list
        label_list = winder_imgclass_list_shorthand
    else:
        assert 0, dataset

    fig = Figure()
    ax = fig.add_subplot(111)
    fig.suptitle( "{0} RAST vs Voronoi Class Performance".format(dataset_title) )

    ind = np.arange(len(imgclass_list),dtype="float")
    width = .20

    means_hash = { "rast_fullpage": [], 
                   "vor_fullpage": [] ,
                   "rast_300": [], 
                   "vor_300": [] 
                 }

    for algo in algorithm_list : 
        for imgclass in imgclass_list : 
            for stripsize in ("300","fullpage") : 
                data_list = datfile.loaddb( dataset=dataset, stripsize=stripsize, 
                                algorithm=algo, imgclass=imgclass )
                all_metric = np.concatenate( [ d["metrics"] for d in data_list ] )

                key = "{0}_{1}".format( algo, stripsize )

                means_hash[key].append( np.mean(all_metric) )

                # break the ref
                all_metric = None
        
    print means_hash 

    ax.set_ylim(0,1.0)
    ax.set_ylabel( "Match Metric" )
    ax.set_xlabel( "Image Class" )

    rects = []
#    citer = iter( ("r","g","y","b"))
    # copied the hatch list from http://matplotlib.org/api/axes_api.html
    hiter = iter( ("/" , "\\" , "x" , "o" , "O" , "." , "*") )
    for key in ("rast_fullpage","vor_fullpage","rast_300","vor_300") :     
        print ind
        r = ax.bar( ind, means_hash[key], width, hatch=hiter.next(), color="w" )
#        r = ax.bar( ind, means_hash[key], width, color=citer.next() )
        ind += 0.2
        rects.append( r ) 
        # break the ref
        r = None

#    rects2 = ax.bar( ind, means_hash["vor_fullpage"], width, color='y' )
#    ind += width
#    rects3 = ax.bar( ind, means_hash["rast_300"], width, color='r' )
#    ind += width
#    rects4 = ax.bar( ind, means_hash["vor_300"], width, color='y' )

    # http://stackoverflow.com/questions/13515471/matplotlib-how-to-prevent-x-axis-labels-from-overlapping-each-other
    ax.set_xticks( range(len(imgclass_list)) )
    tlist = ax.set_xticklabels( label_list, ha='left' )
    for t in tlist :
#        t.set_horizontalalignment('center')
#        t.set_bbox(dict(facecolor="white", alpha=0.5))
#        print t.get_position()
        pass

#    ax.set( xticks=range(len(imgclass_list)), xticklabels=label_list )