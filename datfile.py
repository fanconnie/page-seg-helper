
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
        data_list.append( ndata )
        # detach ref
        ndata = None

        path_list.append( datfilename)

    return path_list, data_list

def load_results_tree( results_hash ) : 
    for root in results_hash.keys() :
        print root
        names, data = load_all_data(root)
        results_hash[root] = {"names":names,"data":data}

    return results_hash

def load_all_results() :
    pklname = "winder_results.pkl" 
    if os.path.exists(pklname):
        with open(pklname,"rb") as f : 
            winder_results = pickle.load(f)
        print "loaded",pklname
    else : 
        winder_results = { "winder_fullpage_rast" : None,
                           "winder_fullpage_vor" : None,
                           "300_winder_rast" : None,
                           "600_winder_rast" : None,
                           "300_winder_vor" : None,
                           "600_winder_vor" : None }
        winder_results = load_results_tree( winder_results )
        with open(pklname,"wb") as f : 
            pickle.dump(winder_results,f)
            print "wrote", pklname 

    pklname = "uwiii_results.pkl"
    if os.path.exists(pklname) :
        with open(pklname,"rb") as f : 
            uwiii_results = pickle.load(f)
        print "loaded",pklname
    else : 
        uwiii_results = { #"fullpage_rast" : None,
                          #"fullpage_vor" : None,
                          "300_rast" : None,
                          "600_rast" : None,
                          "300_vor" : None,
                          "600_vor" : None }
        uwiii_results = load_results_tree( uwiii_results )
        with open(pklname,"wb") as f : 
            pickle.dump(uwiii_results,f)

#    uwiii_fullpage_rast = load(os.path.join("uwiii_fullpage","uwiii_fullpage_rast.dat"))
#    uwiii_fullpage_vor = load(os.path.join("uwiii_fullpage","uwiii_fullpage_vor.dat"))


#    print uwiii_fullpage_rast
#    print uwiii_fullpage_vor
    
    return winder_results, uwiii_results

db_fields_list = ( "filename" ,
              "algorithm" ,
              "stripsize" ,
              "dataset" ,
              "imgclass" ,
              "metrics"  )

# empty hash with fields that become the fields in our DB
db_fields = dict( [ (k,None) for k in db_fields_list] )
#db_fields = { "filename" : None,
#              "algorithm" : None,
#              "stripsize" : None,
#              "dataset" : None,
#              "imgclass" : None,
#              "metrics" : None }

valid_stripsizes = ( "300", "600", "fullpage" )

def decode_winder_filename(filename) : 
    # split a winder .dat filename into necessary components

    valid_classnames = (
        "Double_Column",
        "Mixed_Columns",
        "Double_Column_Pictures",
        "Mixed_Columns_Pictures",
        "Double_Column_Pictures_Scientific",
        "Single_Column",
        "Magazine",
        "Single_Column_Pictures"
    )

#    fields = { "filename" : None,
#           "algorithm" : None,
#           "stripsize" : None,
#           "dataset" : None,
#           "imgclass" : None }
    fields = dict(db_fields)
    fields["dataset"] = "winder"

    # e.g., 
    # 600_winder_rast/imagesAndgTruth/Double_Column/300dpi/2col300_1/2col300_1.dat
    # winder_fullpage_rast/Double_Column/300dpi/Double_Column.dat

    fields["filename"] = filename

    # get the imgclass name from the dirname
    dirnames = filename.split(os.sep)

    # the results are in directory trees with two different styles
    if "imagesAndgTruth" in filename : 
        fields["imgclass"] = dirnames[2]
        fields["stripsize"],owner,fields["algorithm"]= dirnames[0].split("_")
    else : 
        fields["imgclass"] = dirnames[1]
        fields["stripsize"] = "fullpage"
        x,x,fields["algorithm"]= dirnames[0].split("_")
        
    assert fields["imgclass"] in valid_classnames, fields["imgclass"]
    assert fields["stripsize"] in valid_stripsizes, fields["stripsize"]

    return fields

def decode_uwiii_filename( filename ) : 
    fields = dict(db_fields)
    fields["dataset"] = "uwiii"

    dirnames = filename.split(os.sep)
    
    fields["filename"] = filename
    fields["stripsize"],fields["algorithm"]= dirnames[0].split("_")

    assert fields["stripsize"] in valid_stripsizes, fields["stripsize"]

    # classname is the first letter of the data directory name
    # e.g., "A001ZONE" is the 'A' dataset
    fields["imgclass"] = dirnames[-1][0]

    return fields

def store_result_data_to_db( cur, results ) : 
    for k in results.keys() : 
        name_list = results[k]["names"]
        data_list = results[k]["data"]
        for name,data in zip(name_list,data_list) : 
#            f = decode_winder_filename( name )
            if "winder" in name : 
                f = decode_winder_filename( name )
            else : 
                f = decode_uwiii_filename( name ) 
#            print f
            cur.execute( "INSERT INTO pageseg VALUES(?,?,?,?,?,?)",
                (f["filename"],f["algorithm"],f["stripsize"],
                 f["dataset"],f["imgclass"],data.tostring()))

def loaddb( **kargs ): 
    # run a db query using function keywords and their values as the col=value
    # in the SQL query
    # e.g, = loaddb( dataset="winder", stripsize="600", imgclass="Magazine" )
    
    # sanity check the args
    for k in kargs.keys() : 
        assert k in db_fields_list, k

    query_elements = [ "{0}=?".format(k) for k in kargs.keys() ]
    query = " and ".join( query_elements )
#    print query
    values = kargs.values()
#    print values

    conn = sqlite3.connect("pageseg.db")
    conn.text_factory = str
    cur = conn.cursor()

    query = "SELECT * FROM pageseg WHERE " + query

#    print query
    cur.execute(query, values)

    data = [ dict(zip(db_fields_list,r)) for r in cur.fetchall() ]

    # convert the metrics field to a numpy array (from the string as it's
    # stored in the DB)
    for d in data : 
        d["metrics"] = np.fromstring(d["metrics"],dtype="float")

    conn.close()

    return data