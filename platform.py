from platformio.managers.platform import PlatformBase

class WiziotestPlatform(PlatformBase):
    def is_embedded(self):
        print('[---] is_embedded')
        return True

    def get_boards(self, id_=None):
        print('[---] get_boards')
        res = PlatformBase.get_boards(self, id_)
        return res

    def get_package_type(self, name):
        print('[---] get_package_type', name)
        return self.packages[name].get("type")

    def on_installed(self):
        print('[---] on_installed')    