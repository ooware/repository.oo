#/*
# *      Copyright (C) 2013 Joost Kop
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import urllib

from resources.lib.utils import *
from resources.lib.dropboxviewer import *

MAX_MEDIA_ITEMS_TO_LOAD_ONCE = 15

class FolderBrowser(DropboxViewer):
        
    def __init__( self, params ):
        super(FolderBrowser, self).__init__(params)

    def buildList(self):
        resp = self.getMetaData(self._current_path, directory=True)
        if resp != None and 'contents' in resp:
            contents = resp['contents']
        else:
            contents = []
        super(FolderBrowser, self).buildList(contents)
    
    def show(self):
        super(FolderBrowser, self).show(cacheToDisc=True)

    def getUrl(self, path, media_items=0, module=None):
        url = super(FolderBrowser, self).getUrl(path, media_items, module)
        return url
    
def run(params): # This is the entrypoint
    browser = FolderBrowser(params)
    browser.buildList()
    browser.show()
