#!/usr/bin/python

# Parse an OCRopus output XML.
# davep 09-Feb-2013

import sys
import os
import xml.etree.ElementTree as ET

import rects

def load_xml( xmlfilename ) :
    tree = ET.parse(xmlfilename)
    root = tree.getroot()
    return root

# pretend to be a UW-III boxfile so I can convert an upper_left/lower_right to
# a rects.Strip
class Zone( object ): 
    corner_one = {"row":0,"col":0}
    corner_two = {"row":0,"col":0}

    def __init__( self, upper_left, lower_right ) : 
        # incoming fields are x,y order 
        self.corner_one["row"] = upper_left[1]
        self.corner_one["col"] = upper_