# LICENSE

import os, sys, time, pathlib, json
from os.path import join
from SCons.Script import DefaultEnvironment

version = '1234'

def dev_install():
    global version    
    print('[---] do install( + )')

    env = DefaultEnvironment()  
    pico = join(env.framework_dir, 'pico-sdk')

    if os.path.exists( pico ):  
        print('[---] do install( EXIST )')
        return pico # Update pico-sdk ?!
    print('[---] do install( NOT EXIST )')

    print('[---] do install( - )')