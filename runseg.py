
#!python

# Run the segmentation then zone compare on a UW-III image. Capture the output
# metric. 
#
# davep 6-Feb-2013

import sys
import subprocess
import os
import pickle
import glob
import Image
import argparse
import signal

from basename import get_basename 
import drawxml

num_rows = 600
#num_rows = 300
uwiii_imgdir = "IMAGEBIN/"
uwiii_xmldir = "ZONEXML/"

#segmentation_cmd = "./rast-ocropus"
#segmentation_algorithm = "rast"

segmentation_cmd = "./voronoi-ocropus"
segmentation_algorithm = "vor"

def parse_runZoneComp_result( strings ) :
#    print strings
#    print type(strings)

    slist = strings.split("\n")
#    print slist
    for s in slist : 
        if s.startswith( "Segmentation Metric" )  :
            fields = s.split()

            metric = float(fields[3])
            return metric

    # TODO add diagnostics, better error report
    raise Exception( "Metric not found" )


def get_document_id_from_basename( basename ) :
    # split the basename (e.g., ("A00BZONE_300_010_0000_rast") into just the
    # UW-III document ID
    fields = basename.split("_")
    document_id = fields[0]

    return document_id

running_filename = None

def handler( signum, frame ) : 
    print running_filename
    result = subprocess.check_output( "ps waux | grep "+running_filename, shell=True )
    print result

    fields = result.split()
    pid = int(fields[1])

    print "killing pid=",pid 

    os.kill(pid,signal.SIGKILL )

def run_image_with_gtruth( imgfilename, gtruth_xml_filename, output_dir ) :
    basename = get_basename(imgfilename)

    document_id = get_document_id_from_basename( basename )

    out_imgfilename = os.path.join( output_dir, "{0}_{1}.png".format(
                        basename, segmentation_algorithm ))
    xml_filename = os.path.join( output_dir, "{0}_{1}.xml".format( 
                        basename, segmentation_algorithm ) )

    # inputs
#    print "imgfilename=",imgfilename
#    print "gtruth_xml_filename=",gtruth_xml_filename

    # outputs
#    print "xml_filename=",xml_filename
#    print "out_imgfilename=",out_imgfilename
#    sys.exit(0)

    # segment the image
    cmd = "{0} {1} {2}".format( segmentation_cmd, imgfilename, out_imgfilename ) 
#    cmd = "./rast-ocropus {0} {1}".format( imgfilename, out_imgfilename ) 

    signal.signal( signal.SIGALRM, handler )
    # small optimization; if the result already exists, don't run it again
    # (crash recovery)
    print cmd
    if os.path.exists( xml_filename ) :
        print "{0} already exists so assume seg already run".format( xml_filename )
    else : 
        global running_filename 
        running_filename = imgfilename 

        signal.alarm( 5 )
        try : 
            result = subprocess.check_output( cmd.split() )
            signal.alarm(0)
        except subprocess.CalledProcessError : 
            signal.alarm(0)
            return { "output_image_file": out_imgfilename, 
                     "output_xml_file": "failed",
                     "metric" : 0 } 

        # write the XML results 
        with open(xml_filename,"w") as outfile :
            print >>outfile, result
        print "wrote", xml_filename

    # run the compare
    cmd = "./runZoneComp -g {0} -d {1}".format( gtruth_xml_filename, xml_filename )
    print cmd

    try : 
        result = subprocess.check_output( cmd.split() )
    except subprocess.CalledProcessError : 
        return { "output_image_file": out_imgfilename, 
                 "output_xml_file": "failed",
                 "metric" : 0 } 

    # get the segmentation metric from the output
    metric = parse_runZoneComp_result( result ) 
    print "metric={0}".format( metric )

    return { "output_image_file": out_imgfilename, 
             "output_xml_file": xml_filename,
             "metric" : metric } 

def run_all_uwiii( ) :
    # run all UW-III images
    output_dir = "fullpage/"

    result_list = []
    for imgfilename in sys.argv[1:] :
        basename = get_basename(imgfilename)
        document_id = get_document_id_from_basename( basename )

        # zone box files use "ZONE" instead of "BIN"
        # e.g., 
        # A00ABIN_300_010_2990.png -> A00AZONE_300_010_2990.xml 
        gtruth_xml_filename = uwiii_xmldir + "{0}.xml".format( basename.replace("BIN","ZONE") )

#        print basename, document_id, gtruth_xml_filename

        result = run_image_with_gtruth( imgfilename, gtruth_xml_filename )
        result_list.append( result ) 

        # save pickled file so can do interesting things with the results later
        # (especially if we crash)
        output = open( "uwiii.pkl", "wb" )
        pickle.dump(result_list,output)
        output.close()