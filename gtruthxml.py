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

# pret