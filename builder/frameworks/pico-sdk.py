# LICENSE

from os.path import dirname
from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
env.platform = 'pico-sdk'
env["PLATFORM_DIR"] = env.platform_dir = dirname( env["PLATFORM_MANIFEST"] )
env["FRAMEWORK_DIR"] = env.framework_dir = env.PioPlatform().get_package_dir("framework-wizio-TEST")
md = env.platform + "-" + env.BoardConfig().get("build.core")
__import__(md).dev_init(env)

#print( env.Dump() )
