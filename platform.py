# LICENSE

import os, sys, time, pathlib, json
from os.path import join, dirname, exists
from platformio.managers.platform import PlatformBase

class WiziotestPlatform(PlatformBase):
    def is_embedded(self):
        print('[---] is_embedded()')
        return True

    def get_boards(self, id_=None):
        print('[---] get_boards()')
        res = PlatformBase.get_boards(self, id_)
        return res

    def get_package_type(self, name):
        print('[---] get_package_type()', name)
        return self.packages[name].get("type")

    def on_installed(self):
        print('[---] on_installed( + )')   

        p = join( dirname( __file__ ), 'builder', 'frameworks', 'install.py' ).replace('\\\\', '/')
        print('[---] on_installed( %s )' % p)
        if exists( p ):
            print('[---] on_installed( EXIST )')
            __import__(p).dev_install()
        else:
            print('[---] on_installed( NOT EXIST )')
        print('[---] on_installed( - )') 
