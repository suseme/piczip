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
            
    def resizeTaobao(self, infile):
        f, e = os.path.splitext(infile)
        outfile = f + '_taobao' + e
        im = Image.open(infile)
        w, h = im.size
        if w > 750:
            scale = w * 1000 / 750
            width = w * 1000 / scale
            height = h * 1000 / scale
            im.resize((width, height), Image.ANTIALIAS).save(outfile)
