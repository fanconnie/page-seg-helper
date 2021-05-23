#!python

# Parse a UWIII ground truth Box file. Slice into 1",2",3",4",etc new ground
# truth files.
#
# davep 01-Feb-2013

import sys
import os

import zonebox

class Point(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def __repr__(self) : 
        return "({0},{1})".format(self.x,self.y)

class Strip( object ) :
    def __init__( self, **kwargs ) : 
        # self.value will be "Text", "Non-text", ... (more later)
        self.value = None

        self.rect = [ Point(), Point(), Point(), Point() ]

        if "width" in kwargs and "height" in kwargs :
            # create a strip from a simple width/height
            width = kwargs["width"]
            height = kwargs["height"]
            self.rect[0].x = 0
            self.rect[0].y = 0
            self.rect[1].x = width
            self.rect[1].y = 0
            self.rect[2].x = width
            self.rect[2].y = height
            self.rect[3].x = 0
            self.rect[3].y = height

            self.width = width
            self.height = height
        elif "box" in kwargs : 
            # create a strip from a UW-III ZoneBox class
            box = kwargs["box"]

            self.rect[0].x = box.corner_one["col"]
            self.rect[0].y = box.corner_one["row"]

            self.rect[1].x = box.corner_two["col"] # same as [2]
            self.rect[1].y = box.corner_one["row"] # same as [0]

            self.rect[2].x = box.corner_two["col"]
            self.rect[2].y = box.corner_two["row"]

            self.rect[3].x = box.corner_one["col"]  # same as [0]
            self.rect[3].y = box.corner_two["row"]  # same as [2]

            self.width = self.rect[1].x - self.rect[0].x
            self.height = self.rect[2].y - self.rect[1].y

#        else : 
#            # TODO make this smarter (defaults?)
#            raise Exception( "need width/height or box parameters" )

        # add enough duck so zone2xml can quack me 
        # http://en.wikipedia.org/wiki/Duck_typing
        # upper left 
        self._corner_one = { "row": self.rect[0].y, "col": self.rect[0].x } 
        # lower r