# LICENSE

import os, sys, time, pathlib, json
from os.path import join
from shutil import copyfile, rmtree
from platformio import proc

version = '1234'

def INFO(str): 
    print('[INSTALL]', str) 

def DBG(str):
    import inspect
    print( '[DBG] { %s() } %s' % (inspect.stack()[1][3], str))

def ERROR(txt):
    print('❖ ERROR ❖ [INSTALL]', txt)
    exit(-1)

###############################################################################

def create_patch(pico_dir):
    DBG('create_patch()')

def dev_install( framework_dir ):
    global version    

    if not os.path.exists( framework_dir ):  
        print('[---] do install( NOT EXIST )')
        return 

    pico = join( framework_dir, 'pico-sdk' )
    DBG('pico: %s' % pico)

    if os.path.exists( pico ):  
        create_patch( pico ) # if manual install
        return 

    ## CLONE BEGIN ####################

    start_time = time.time()
    INFO('Clone pico-sdk ( less than a minute, Plese wait )')
    args = [ 'git', 'clone', 'https://github.com/raspberrypi/pico-sdk', pico ]
    res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin )
    
    if 0 == res['returncode']: 
        INFO('Init submodules ...')
        args = ['git', 'submodule', 'init']
        res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd = pico )

        if 0 == res['returncode']: 
            INFO('Update submodules ...')
            args = ['git', 'submodule', 'update', pico  ]
            res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd = pico )
           
    if 0 != res['returncode']:  
        rmtree(pico, ignore_errors=False)
        ERROR(res)

    ## CLONE END   ####################

    create_patch(pico) 
    INFO('PICO-SDK Version: %s' % version )
    INFO('DONE ( %s seconds )' % int( time.time() - start_time ) )