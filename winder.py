
#!/usr/bin/python

# sweep through images in Amy Winder's image set and runseg.py on each
# davep 09-Feb-2013

import sys
import os
import os.path
import glob
import Image
import pickle

import runseg
from basename import get_basename

num_rows=600

#root = "imagesAndgTruth"
#root = "300_winder/imagesAndgTruth"
root = "600_winder/imagesAndgTruth"

#runseg.segmentation_cmd = "./rast-ocropus"
#runseg.segmentation_algorithm = "rast"
runseg.segmentation_cmd = "./voronoi-ocropus"
runseg.segmentation_algorithm = "vor"

def main() : 
    root_dirs = os.listdir(root)

    for rdir in root_dirs : 
        # skip the subversion directories
        if ".svn" in rdir: 
            continue
        if ".DS_Store" in rdir: 
            continue

        print "dir=",rdir

        # only do the 300dpi images for now
        image_dirs = os.listdir( os.path.join( root, rdir, "300dpi" ) )

        print "image_dirs=",image_dirs

        assert "png" in image_dirs 

        image_dirs = [ d for d in image_dirs if ".svn" not in d ]
        print "image_dirs=",image_dirs

        assert ".svn" not in rdir, rdir

        png_path = os.path.join(root,rdir,"300dpi","png")
        print "png_path=",png_path

        img_filelist = glob.glob(os.path.join(png_path,"*.png"))
        print "img_filelist=",img_filelist
        assert len(img_filelist)

        xml_filelist = [] 

        for imgfile in img_filelist :
            fields = os.path.split(imgfile)
            print fields
            xmlfile = os.path.join( fields[0].replace("png","gTruth"), 
                                    fields[1].replace(".png",".xml") )

            print "imgfile=",imgfile,"xml_file=",xmlfile
            img = Image.open(imgfile)
            img.load()
            try : 
                f = open(xmlfile,"r")
                f.close()
            except IOError,e :
                if e.errno==2 :
                    # try our luck with the gTruth/xml dir
                    xmlfile = os.path.join( fields[0].replace("png","gTruth"), 
                                            "xml",
                                            fields[1].replace(".png",".xml") )
                    f = open(xmlfile,"r")
                    f.close()
                else : 
                    raise

            xml_filelist.append( xmlfile )

        print img_filelist
        print xml_filelist

        s = "{0}_winder_{1}".format(numrows,runseg.segmentation_algorithm)
        output_dir = os.path.join(s,rdir,"300dpi")
#        output_dir = os.path.join("300_winder_fullpage_rast",rdir,"300dpi")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_basename = rdir
#        runseg.run_file_list( img_filelist, xml_filelist, output_dir, output_basename )


def foo() :
        for imgdir in image_dirs : 
            print "imgdir=",imgdir
            # did we land in a dir with png files? 
            if "png" not in imgdir : 
                continue

            print root,rdir,imgdir
            imgpath = os.path.join(root,rdir,"300dpi",imgdir)
            print "imgpath=",imgpath

            # subversion metadata keeps messing with me
            assert ".svn" not in rdir, rdir
            assert ".svn" not in imgdir, imgdir
            assert ".svn" not in root, root