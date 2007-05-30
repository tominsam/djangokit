from distutils.core import setup as setup_core
import py2app,sys,os
from glob import glob
import django
from AppKit import NSBundle

# Yes, ok, this is nasty, and I'm sure there's a faaar more elegant way
# of doing it. But I don't really understand distutils right now. This
# _works_, and it wouldn't if I got sidetracked by every little thing
# I didn't understand. Patches welcome.. :-)

def setup(**args):

    appname = args['appname']
    del args['appname']
    
    if 'prettyname' in args:
        prettyname = args['prettyname']
        del args['prettyname']
    else:
        prettyname = appname
    
    if 'settings' in args:
        more_settings = args['settings']
        del args['settings']
    else:
        more_settings = {}
    
    NSBundle.mainBundle().infoDictionary()[u'DjangoKit'] = {
      'appname':appname,
      'prettyname':prettyname,
    };
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangokit.settings'
    from django.core.management import syncdb
    from django.conf import settings
    settings.DATABASE_NAME # reading a property inflated the settings object
    settings.DATABASE_NAME = "database.sqlite"
    syncdb()
    
    plist = dict(
        NSMainNibFile="MainMenu",
        CFBundleName = prettyname,
        CFBundleIdentifier="org.jerakeen.DjangoKitApps.%s"%appname, # TODO - could be better
        CFBundleShortVersionString = args['version'],
        CFBundleVersion = args['version'],
        NSHumanReadableCopyright="Copyright 2007 %s"%args['author'],
        DjangoKit={
          'appname':appname,
          'prettyname':prettyname,
          'settings':more_settings,
        },
    )
    
    py2app_options = dict(
        plist=plist,
        packages = [appname, 'djangokit', 'django'],
    )

    if 'iconfile' in args:
        py2app_options['iconfile'] = args['iconfile']
        del args['iconfile']

    base = __import__('djangokit').__path__[0]
    nibfile = "%s/MainMenu.nib"%base
    setup_core( **dict( args,
        app=[ "%s/app.py"%base ],
        # TODO - this requires a local 'media' folder. Don't.
        data_files = ['media', nibfile, 'database.sqlite', appname],
        options=dict(py2app=py2app_options),
    ))
