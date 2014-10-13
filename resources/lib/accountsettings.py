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

import xbmcvfs
import shutil
import os
import pickle

from resources.lib.utils import *

class AccountSettings(object):
    '''
    Class which loads and saves all the account settings,
    for easy access to the account settings
    '''
    
    def __init__(self, account_name):
        self.account_name = account_name
        self.access_token = ''
        self.passcode = ''
        self.passcodetimeout = 30
        self.session_id = ''
        self.synchronisation = False
        self.syncfreq = 5.0
        self.syncpath = ''
        self.remotepath = ''
        dataPath = xbmc.translatePath( ADDON.getAddonInfo('profile') )
        self._account_dir = dataPath + '/accounts/' + self.account_name
        #read from location if present
        if xbmcvfs.exists( self._account_dir ):
            self.load()
        
    def load(self):
        settings_file = self._account_dir + '/settings'
        try:
            with open(settings_file, 'r') as file_obj:
                tmp_dict = pickle.load(file_obj)
        except Exception as exc:
            log_error('Failed to load the settings: %s' % (str(exc)) )
        else:
            self.__dict__.update(tmp_dict)
        
    def save(self):
        log_debug('Save account settings: %s' % (self.account_name) )
        #check if the account directory is present, create otherwise
        if not xbmcvfs.exists( self._account_dir ):
            xbmcvfs.mkdirs( self._account_dir )
        #Save...
        settings_file = self._account_dir + '/settings'
        try:
            with open(settings_file, 'w') as file_obj:
                pickle.dump(self.__dict__, file_obj)
        except Exception as exc:
            log_error('Failed saving the settings: %s' % (str(exc)) )
    
    def rename(self, new_name):
        log_debug('Rename account from %s to %s' % (self.account_name, new_name) )
        dataPath = xbmc.translatePath( ADDON.getAddonInfo('profile') )
        new_dir = dataPath + '/accounts/' + new_name
        try:
            #rename folder
            os.rename(self._account_dir, new_dir)
        except Exception as exc:
            log_error('Failed to rename folder: %s' % ( str(exc) ) )
        else:
            self.account_name = new_name
            #Also save it, otherwise the wrong (class)account_name will be loaded next time.
            self.save() 
        
    def remove(self):
        log_debug('Remove account folder: %s' % (self._account_dir) )
        shutil.rmtree(self._account_dir)

