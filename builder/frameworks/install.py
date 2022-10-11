# LICENSE

import os, sys, time, pathlib, json
from os.path import join

version = '1234'

def dev_install():
    global version    
    print('[---] do install( + )')

    if os.path.exists( 'C:/Users/1124/.platformio/packages/framework-wizio-TEST' ):  
        print('[---] do install( EXIST )')
        print( globals() )
        return 
    print('[---] do install( NOT EXIST )')

    print('[---] do install( - )')