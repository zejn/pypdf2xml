# coding: utf-8
from distutils.core import setup

setup(name='pypdf2xml',
      version='0.1',
      description='A reimplementation of pdftoxml in Python, using pdfMiner. Handles unicode characters better.',
      author=u'Gašper Žejn'.encode('utf-8'),
      author_email='zejn@owca.info',
      url='https://github.com/zejn/pypdf2xml',
      scripts=['pdf2xml', 'pdfxml2csv', 'headerfilter'],
      packages=['pypdf2xml'],
      install_requires=['pdfminer>=20110515', 'lxml'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          ]
     )


