# LICENSE

import os, sys, time, pathlib, json
from os.path import join, dirname, exists
from importlib.machinery import SourceFileLoader
from platformio.managers.platform import PlatformBase

F_NAME = 'framework-wizio-TEST'

class WiziotestPlatform(PlatformBase):
    def is_embedded(self):
        #print('[---] is_embedded()')
        return True

    def get_boards(self, id_=None):
        #print('[---] get_boards()')
        res = PlatformBase.get_boards(self, id_)

        #self.on_installed()

        return res

    def get_package_type(self, name):
        #print('[---] get_package_type()', name)
        return self.packages[name].get('type')

    def on_installed(self):     
        p = os.path.join( dirname( __file__ ), 'builder', 'frameworks', 'install.py' ).replace('\\', '/')
        if exists( p ):
            f_dir = os.path.join( self.config.get('platformio', 'core_dir'), 'packages', F_NAME ),
            name = 'module_' +  str( abs( hash( p ) ) )
            m = SourceFileLoader(name, p).load_module() 
            m.dev_install( f_dir[0] )
        else:
            print('[---] on_installed( INSTALL NOT EXIST )')
 
 
