#!/usr/bin/env python

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
    
