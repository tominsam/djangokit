import os
import sys
import re
import shutil
import thread
import random

# helps py2app. TODO - get this dep walked properly.
try:
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    from pysqlite2 import dbapi2 as sqlite

from Foundation import *
from AppKit import *
from WebKit import *
from PyObjCTools import NibClassBuilder, AppHelper

# extract classes from nib
NibClassBuilder.extractClasses( "MainMenu" )

# Load the settings file. In settings.py, we do clever things
# to pull informaition from the Info.plist
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangokit.settings'
import djangokit.settings

from django.conf import settings
import django
settings.DATABASE_ENGINE # accessing a property inflates the settings

# now we change the settings object for the current project.

# TODO - I really want to do this in settings.py
nibinfo = NSBundle.mainBundle().infoDictionary()[u'DjangoKit']
if 'settings' in nibinfo:
    for k in nibinfo['settings']:
        print "%s => %s"%( k, nibinfo['settings'][k] )
        settings.__setattr__(k, nibinfo['settings'][k])

# where do our support files live?
support_folder = os.path.join( os.environ['HOME'], "Library", "Application Support", "DjangoKit", settings.APPNAME )
if not os.path.isdir(support_folder):
    NSLog("creating support folder %s"%support_folder)
    os.makedirs(support_folder)

# TODO - need some way of updating SQL schema
# of course, this is a general django problem.
settings.DATABASE_NAME = os.path.join( support_folder, "database.sqlite" )
if not os.path.isfile( settings.DATABASE_NAME ):
    NSLog("installing default database")
    shutil.copy(
        os.path.join( NSBundle.mainBundle().resourcePath(), "database.sqlite" ),
        settings.DATABASE_NAME
    )

# we can just publish media directly from the bundle
# TODO - uploads need to go somewhere, and they can't go here.
settings.MEDIA_ROOT = os.path.join(NSBundle.mainBundle().resourcePath(), "media" )
settings.MEDIA_URL = '/__media/' # randomize?

# TODO - detect from system locale
# settings.TIME_ZONE = ''
# settings.LANGUAGE_CODE = ''

class DjangoKit(NibClassBuilder.AutoBaseClass):

    def applicationDidFinishLaunching_(self, aNotification):
        self.recentPath = "/"
        
        self.window.setTitle_( settings.APPNAME )
    
        res = NSBundle.mainBundle().resourcePath()

        # generate random port number, in what is almost certainly an
        # unsafe way.
        self.port = random.randrange(9000, 12000)

        def startWebServer():
            print("Starting web server on port %d"%self.port)
            from django.core.servers.basehttp import run, AdminMediaHandler, WSGIServerException
            from django.core.handlers.wsgi import WSGIHandler

            path = django.__path__[0] + '/contrib/admin/media'
            handler = AdminMediaHandler(WSGIHandler(), path)

            # even hackier than everything else
            handler = AdminMediaHandler(handler, settings.MEDIA_ROOT)
            handler.media_url = settings.MEDIA_URL
            
            run( '127.0.0.1', self.port, handler)
        
        thread.start_new_thread( startWebServer, () )
        
        # load the index page in 1 second, when presumably the server will
        # be running.
        # TODO - we should ship a 'loading..' html file, load that instantly,
        # then schedule a main page load. Or, _better_, would be to defer
        # display of the window until the server is started.
        self.webview.mainFrame().performSelector_withObject_afterDelay_(
            'loadRequest:',
            NSURLRequest.requestWithURL_( NSURL.URLWithString_('http://localhost:%d/'%self.port) ),
            1,
        )

    def goHome_(self, sender):
        self.webview.mainFrame().loadRequest_(
            NSURLRequest.requestWithURL_( NSURL.URLWithString_('http://localhost:%d/'%self.port) ),
        )

    def goAdmin_(self, sender):
        self.webview.mainFrame().loadRequest_(
            NSURLRequest.requestWithURL_( NSURL.URLWithString_('http://localhost:%d/admin/'%self.port) ),
        )
    
    def goPath_(self, sender):
        self.customPath.setStringValue_( self.recentPath ) # TODO - use current location
        self.customPath.selectText_( self )
        NSApplication.sharedApplication().beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.pathView,
            self.window,
            self,
            None,
            0
        )

    def cancelGoPath_(self, sender):
        self.pathView.orderOut_(self)
        NSApplication.sharedApplication().endSheet_( self.pathView )

    def doGoPath_(self, sender):
        self.pathView.orderOut_(self)
        NSApplication.sharedApplication().endSheet_( self.pathView )

        path = self.customPath.stringValue()
        NSLog(path)
        path = re.sub('^/', '', path)

        if re.match('\w+:', path):
            NSRunAlertPanel("bad location", "please enter a relative path", "Ok", None, None)
            return

        self.webview.mainFrame().loadRequest_(
            NSURLRequest.requestWithURL_( NSURL.URLWithString_('http://localhost:%d/%s'%(self.port, path) ) ),
        )

    # suppress right-click menu
    def webView_contextMenuItemsForElement_defaultMenuItems_( self, webview, element, items ):
        return []
        
    def webView_decidePolicyForNavigationAction_request_frame_decisionListener_(self, webview, action, request, frame, listener):
        url = request.URL()
        
        path = url.absoluteString()
        NSLog("deciding for '%s'"%path)

        # serve files
        if url.scheme() == 'file':
            NSLog("file")
            listener.use()
            return
            
        if url.host() == 'localhost' and url.port() == self.port:
            NSLog("local")
            listener.use()
            self.recentPath = url.path()
            return
        
        # everything else can be ignored, and opened by the system
        NSLog("external link")
        listener.ignore()
        NSWorkspace.sharedWorkspace().openURL_( url )

if __name__ == "__main__":
    AppHelper.runEventLoop()

