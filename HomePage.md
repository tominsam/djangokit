# Introduction #

DjangoKit is a framework that will take a [Django](http://www.djangoproject.com/) application, and turn it into a stand-alone MacOS application with a local database and media files. It's more of a thought experiment than an effort at producing a real application, but there are a couple of simple [examples](http://djangokit.googlecode.com/svn/trunk/examples/) and the souce code is available from subversion.

# Installation #

DjangoKit depends on [Django](http://www.djangoproject.com/) and [PyObjC](http://pyobjc.sourceforge.net/), so first install them, then install DjangoKit the usual way:

```
python setup.py install
```

Currently your app will need a fairly specific folder layout to work, use the layout in the examples as a base. Copy a [setup.py file from the TODO example](http://djangokit.googlecode.com/svn/trunk/examples/todo/setup.py) and modify it to suit your app, then run

```
python setup.py syncdb
python setup.py py2app
```

This should produce a stand-alone .app in the local /dist directory. For development, try

```
python setup.py py2app -A
```

Which will produce a development-only app that symlinks your app into it, so you can continue to edit the source files without having to rebuild the app every time you save. You can even edit the templates while the app is still running and see changes.