__author__ = 'vin@misday.com'

import os
from PIL import Image

class Imaging:
    def __init__(self):
        pass

    def resize(self, infile, scale=2):
        print infile
        try:
            f, e = os.path.splitext(infile)
            outfile = f + '_compressed' + e
            im = Image.open(infile)
            w, h = im.size
            im.resize((w/scale, h/scale), Image.ANTIALIAS).save(outfile)
        except:
            print 'failed'