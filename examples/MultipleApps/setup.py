#!/usr/bin/python
from djangokit import setup

setup(
  appname = "Demonstration of multiple apps",
  apps = [ "app1", "app2" ],
  version = "0.1",
  author = "Tom Insam",
  author_email = "tom@jerakeen.org",
)
