#!/usr/bin/python
# coding: utf-8

import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

datafile = lambda x: os.path.join(os.path.dirname(__file__), 'data', x)

class TestSimplePDF(unittest.TestCase):
    def runTest(self):
        
        expected = """
        <pdf2xml>
            <page number="1" width="612" height="792">
                <text top="71" left="56" width="87" height="15">This is a test PDF.</text>
            </page>
        </pdf2xml>
        """

        pdf_fn = datafile('test1.pdf')
        from pypdf2xml import pdf2xml
        from StringIO import StringIO
        xml = pdf2xml(StringIO(open(pdf_fn, 'rb').read()))
        
        got_lines = [i.strip() for i in xml.split('\n') if i.strip()]
        expected_lines = [i.strip() for i in expected.split('\n') if i.strip()]
        self.assertEqual(got_lines, expected_lines)

class TestUnicodesPDF(unittest.TestCase):
    def runTest(self):
        expected = """
        <pdf2xml>
            <page number="1" width="612" height="792">
                <text top="71" left="56" width="341" height="15">This is a unicode test, ŠE ČE ŽE, če že še, đon Đon. Bä ĕř. Öl. Löüãñ.</text>
                <text top="71" left="324" width="7" height="17">ȩ</text>
            </page>
        </pdf2xml>
        """

        pdf_fn = datafile('test2.pdf')
        from pypdf2xml import pdf2xml
        from StringIO import StringIO
        xml = pdf2xml(StringIO(open(pdf_fn, 'rb').read()))
        
        got_lines = [i.strip() for i in xml.split('\n') if i.strip()]
        expected_lines = [i.strip() for i in expected.split('\n') if i.strip()]
        self.assertEqual(got_lines, expected_lines)


if __name__ == "__main__":
    unittest.main()