# LICENSE: WizIO 2022 Georgi Angelov

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()
env.platform = 'arduino'                                      # platform separating
md = env.platform + '-' + env.BoardConfig().get('build.core') # chip     separating
__import__(md).dev_init(env)

#print( env.Dump() )
