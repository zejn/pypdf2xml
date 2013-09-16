#!/usr/bin/python
# coding: utf-8
"""

A filter that detects and removes repeating content at same position, which is
usually header and footer.

"""

import numpy
import lxml.etree
import re
from PIL import Image
import scipy.ndimage

__all__ = []

def gauss(img):
    dim = 5
    kernel = numpy.ones((dim, dim))/(dim*dim)
    return scipy.ndimage.convolve(img, kernel, mode='constant')


def layout_detect(fileobj):
    pdfxml = fileobj.read()
    root = lxml.etree.fromstring(pdfxml)

    fontspecs = {}
    rows = []

    pages = []
    for pagenum, page in enumerate(root):
        assert page.tag == 'page'
        print page.attrib
        pg = numpy.zeros((
            int(float(page.attrib.get('height'))),
            int(float(page.attrib.get('width'))),
            ))

        pagelines = {}
        for v in page:
            if v.tag == 'text':
                # there has to be a better way here to get the contents
                #text = re.match('(?s)<text.*?>(.*?)</text>', lxml.etree.tostring(v)).group(1)
                text = v.text
                #print >> sys.stderr, text
                if not text.strip():
                    continue
                left = int(v.attrib.get('left'))
                top  = int(v.attrib.get('top'))
                width = int(v.attrib.get('width'))
                height = int(v.attrib.get('height'))
                
                pg[top:top+height,left:left+width] = 255
                # fix some off-by-one placement issues, which make some text span over two lines where it should be in one
                if pagelines.has_key(top-1): 
                    top = top - 1
                elif pagelines.has_key(top+1):
                    top = top + 1
                line = pagelines.setdefault(top, [])
                line.append((left, text))
        ordered = list(sorted([(k, sorted(v)) for k,v in pagelines.iteritems()]))
        rows.extend(ordered)
        pages.append((pagenum, ordered))
        pg2 = gauss(pg).astype(numpy.uint8)
        limit = 5
        pg2[numpy.where(pg2<=limit)] = 0
        pg2[numpy.where(pg2>limit)] = 255
        im = Image.fromarray(pg2, 'L')
        im.save('%.3d.png' % pagenum)

    return pages

    #pg = numpy.zeros((), numpy.int8)
