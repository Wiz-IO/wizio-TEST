# LICENSE: WizIO 2022 Georgi Angelov

#TODO: THE BUILDER IS NOT COMPLETE. !?!

import sys
from os.path import join
from install import dev_install
from pico_common import INFO, DEBUG, ERROR
from SCons.Script import DefaultEnvironment
from platformio import proc

env = DefaultEnvironment()
INFO('CMAKE %s' % env.subst('$PROGNAME') )
dev_install(env)

#TODO: Copy pico_sdk_import.cmake to project

platform = env.PioPlatform()

PICO_SDK_PATH = join(platform.get_package_dir('framework-wizio-TEST'), 'pico-sdk')
PROJECT_DIR = env.subst( join('$PROJECT_DIR', 'src') )
BUILD_DIR = env.subst('$BUILD_DIR')

cmake = platform.get_package_dir("tool-cmake")
env['ENV']['PATH'] += ';' + join(cmake, 'bin')

ninja = platform.get_package_dir("tool-ninja")
env['ENV']['PATH'] += ';' + ninja

cmd = [
    'cmake', #'--help',
    '-DPICO_SDK_PATH=%s' % PICO_SDK_PATH, 
    '-DCMAKE_PROJECT_NAME=%s' % env.subst('$PROGNAME'),
    '-DCMAKE_BUILD_TYPE=Release',
    '-DPICO_TOOLCHAIN_PATH=%s' % join( platform.get_package_dir("toolchain-gccarmnoneeabi"), 'bin'),   
    '-G', 'Ninja',
    '-S', PROJECT_DIR,
    '-B', BUILD_DIR,
]
res = proc.exec_command( cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin )
if 0 == res['returncode']:
    cmd = ['ninja']
    res = proc.exec_command( cmd, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd=BUILD_DIR )
    #print(res)

INFO('DONE ? ( TODO )')
exit(0)