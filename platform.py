
from os.path import join, dirname, exists
from platformio.managers.platform import PlatformBase
#from builder.frameworks.install import dev_install

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

        p = dirname( __file__ )
        if exists( join( p, 'builder', 'frameworks', 'install.py' ) ):
            print('[---] on_installed( EXIST )')
            from builder.frameworks.install import dev_install
            dev_install() 
        else:
            print('[---] on_installed( NOT EXIST )')
        print('[---] on_installed( - )') 
