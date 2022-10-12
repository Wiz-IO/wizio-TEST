# LICENSE: WizIO 2022 Georgi Angelov

from os.path import dirname
from SCons.Script import DefaultEnvironment

FRAMEWORK = 'framework-wizio-TEST'

env = DefaultEnvironment()
env.platform = 'pico-sdk'
env['PLATFORM_DIR'] = env.platform_dir = dirname( env['PLATFORM_MANIFEST'] )
env['FRAMEWORK_DIR'] = env.framework_dir = env.PioPlatform().get_package_dir(FRAMEWORK)
md = env.platform + '-' + env.BoardConfig().get('build.core') # chip separating
__import__(md).dev_init(env)

#print( env.Dump() )
