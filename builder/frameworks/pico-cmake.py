# LICENSE: WizIO 2022 Georgi Angelov

import os
from install import dev_install
from pico_common import INFO, DEBUG, ERROR, dev_init_compiler
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
env.platform = 'pico-cmake' # platform separating

platform = env.PioPlatform()
print('platform', platform)

cmake = os.path.join(platform.get_package_dir("tool-cmake"), "bin")
print('cmake', cmake)

ninja = platform.get_package_dir("tool-ninja")
print('ninja', ninja)


DEBUG('CMAKE test')   

dev_install(env)
dev_init_compiler(env)    

ERROR('The beer got hot !')
