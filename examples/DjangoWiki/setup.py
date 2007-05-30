#!/usr/bin/python
from djangokit import setup

setup(
  appname = "wiki",
  prettyname = "DjangoWiki",
  version = "0.1",
  author = "Paul Bissex",
  settings = {
    'WIKI_SITEBASE':'/',
  }
)
