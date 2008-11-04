#!/usr/bin/python
from djangokit import setup

setup(
  apps = [ "wiki" ],
  appname = "DjangoWiki",
  version = "0.1",
  author = "Paul Bissex",
  settings = {
    'WIKI_SITEBASE':'/wiki/',
  }
)
