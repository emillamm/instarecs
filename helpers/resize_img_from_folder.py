#!/usr/bin/env python

"""Resize images in folder

This script resizes all the jpeg images in a folder named
images to a size of 300 x 300 px. 

NOTE: This file does not handle all errors.  
"""

import PIL
from PIL import Image
import os
import glob

size = 300, 300
imgdir = glob.glob("images_org/*")
for fileName in imgdir:
    file, ext = os.path.splitext(fileName)
    im = Image.open(fileName)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save(fileName, "JPEG")
    
