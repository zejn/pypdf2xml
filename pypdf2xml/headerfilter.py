#!/usr/bin/python
# coding: utf-8
"""

A filter that detects and removes repeating content at same position, which is
usually header and footer.

"""

from StringIO import StringIO
import lxml.etree

from pypdf2xml import parse_page_xml

__all__ = ['remove_header_and_footer']

def detect_repetition(pages):
    counter = {}
    filter_pages = pages[1:]
    numpages = len(filter_pages)
    for pagenum, texts in filter_pages:
        for t in texts:
            ht = (t[0], tuple(t[1]))
            appearances = counter.setdefault(ht, [])
            appearances.append(pagenum)

    counter_items = [(k, v) for k,v in counter.iteritems() if len(v) == numpages]
    header_footer = {}
    for item0 in counter_items:
        top = item0[0][0]
        for item in item0[0][1]:
            left, text = item
            header_footer[(top, left, text)] = 1
    return header_footer

def filter_lines(fileobj, header):

    pdfxml = fileobj.read()
    root = lxml.etree.fromstring(pdfxml)

    fontspecs = {}
    rows = []

    pages = []
    for pagenum, page in enumerate(root):
        assert page.tag == 'page'
        pagelines = {}
        for v in page:
            if v.tag == 'text':
                # there has to be a better way here to get the contents
                text = v.text
                left = int(v.attrib.get('left'))
                top  = int(v.attrib.get('top'))
                # fix some off-by-one placement issues, which make some text span over two lines where it should be in one
                if (top-1, left, text) in header or (top, left, text) in header or (top+1, left, text) in header:
                    v.getparent().remove(v)
                    continue
    return lxml.etree.tostring(root)


def remove_header_and_footer(fileobj):
    xml = StringIO(fileobj.read())
    xml.seek(0)

    parsed = parse_page_xml(xml)
    header_footer = detect_repetition(parsed)

    xml.seek(0)
    newxml = filter_lines(xml, header_footer)
    return newxml

