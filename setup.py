#!/usr/bin/python
from distutils.core import setup
from glob import glob
from os.path import splitext, basename, join as pjoin, walk

def get_files(path):
    files = [ ]
    for t in glob(pjoin(path, '*.py')):
        if not t.endswith('__init__.py'):
            files.append('.'.join( [path, splitext(basename(t))[0]]) )
    return files

setup (
  name = "DjangoKit",
  version = "0.2",
  author = "Tom Insam",
  author_email = "tom@jerakeen.org",
  url = "http://jerakeen.org/code/djangokit",
  description = "package django applications as Mac apps",

  packages = ['djangokit'],
  package_data = {
    '':['MainMenu.nib/*.nib'],
  },
  license = "GPL",
)
