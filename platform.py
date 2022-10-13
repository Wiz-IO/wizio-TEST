# LICENSE: WizIO 2022 Georgi Angelov

from os.path import join, dirname, exists
from importlib.machinery import SourceFileLoader
from platformio.managers.platform import PlatformBase

FRAMEWORK_NAME = 'framework-wizio-TEST'

class WiziotestPlatform(PlatformBase):
    # .platformio/penv/Lib/site-packages/platformio/platform/base.py

    def is_embedded(self):
        return True

    def get_boards(self, id_=None):
        res = PlatformBase.get_boards(self, id_)
        return res

    def get_package_type(self, name):
        T = self.packages[name].get('type')# framework, toolchain...
        if 'framework' == T:
            self.on_installed()
        return T

    def on_installed(self):  
        p = join( dirname( __file__ ), 'builder', 'frameworks', 'install.py' ).replace('\\', '/')
        if exists( p ):
            f_dir = join( self.config.get('platformio', 'core_dir'), 'packages', FRAMEWORK_NAME ),
            name = 'module_' +  str( abs( hash( p ) ) )
            m = SourceFileLoader(name, p).load_module() 
            m.dev_install( f_dir[0] )
        else:
            print('[ERROR] on_installed( INSTALL NOT EXIST )')
 
 
