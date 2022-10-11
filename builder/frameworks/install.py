# LICENSE

import os, sys, time, pathlib, json
from os.path import join
from shutil import copyfile, rmtree
from platformio import proc
from pico_common import mk_dir

version = '1234'


def create_patch(pico_dir):
    print('create_patch()')

def dev_install( framework_dir ):
    global version    
    print('[---] do install( + )')

    if not os.path.exists( 'C:/Users/1124/.platformio/packages/framework-wizio-TEST' ):  
        print('[---] do install( NOT EXIST )')
        return 

    pico = join( framework_dir, 'pico-sdk' )
    print('[INSTALL]', pico)

    if os.path.exists( pico ):  
        create_patch( pico ) # if manual install
        return 

    ## CLONE BEGIN ####################
    
    url  = 'https://github.com/raspberrypi/pico-sdk'
    start_time = time.time()
    print('[INSTALL] Clone pico-sdk ( less than a minute, Plese wait )')
    args = [ 'git', 'clone', url, pico ]
    res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin )
    
    if 0 == res['returncode']: 
        print('[INSTALL] Init submodules ...')
        args = ['git', 'submodule', 'init']
        res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd = pico )

        if 0 == res['returncode']: 
            print('[INSTALL] Update submodules ...')
            args = ['git', 'submodule', 'update', pico  ]
            res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd = pico )
           
    if 0 != res['returncode']:  
        rmtree(pico, ignore_errors=False)
        print('[ERROR][INSTALL] %s', res)
        exit(-1)

    ## CLONE END   ####################

    create_patch(pico) 
    print('[INSTALL] PICO-SDK Version: %s' % version )
    print('[INSTALL] DONE ( %s seconds )' % int( time.time() - start_time ) )
    print('[---] do install( - )')