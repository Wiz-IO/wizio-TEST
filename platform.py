# LICENSE: WizIO 2022 Georgi Angelov

from os.path import join, dirname, exists
from importlib.machinery import SourceFileLoader
from platformio.managers.platform import PlatformBase

FRAMEWORK = 'framework-wizio-TEST'

class WiziotestPlatform(PlatformBase):
    # .platformio/penv/Lib/site-packages/platformio/platform/base.py

    def is_embedded(self):
        #print('[===] is_embedded()')
        return True

    def get_boards(self, id_=None):
        #print('[===] get_boards()')
        res = PlatformBase.get_boards(self, id_)
        ### self.on_installed() # TODO: REMOVE THIS !!!
        return res

    #def board_config(self, id_):
    #def configure_project_packages(self, env, targets=None):
    #def configure_default_packages(self, options, targets):

    def get_package_type(self, name):
        #print('[===] get_package_type()') # framework, toolchain...
        T = self.packages[name].get('type')
        if 'framework' == T:
            #print('[===]\tPackage is framework')
            self.on_installed()
        return T

    def on_installed(self):  
        #print('[===] on_installed()')  
        p = join( dirname( __file__ ), 'builder', 'frameworks', 'install.py' ).replace('\\', '/')
        if exists( p ):
            f_dir = join( self.config.get('platformio', 'core_dir'), 'packages', FRAMEWORK ),
            name = 'module_' +  str( abs( hash( p ) ) )
            m = SourceFileLoader(name, p).load_module() 
            m.dev_install( f_dir[0] )
        else:
            print('[ERROR] on_installed( INSTALL NOT EXIST )')
 
 
