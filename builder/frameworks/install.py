# LICENSE

import os, sys, time, pathlib, shutil
from os.path import join, exists
from shutil import copyfile, rmtree
from subprocess import Popen, PIPE
from platformio import proc

VER = '0.0.0'
ver = {'PICO_SDK_VERSION_MAJOR':'0', 'PICO_SDK_VERSION_MINOR':'0', 'PICO_SDK_VERSION_REVISION':'0' }

def INFO(str): 
    print('❖', str)

def ERROR(txt):
    print('❖ ERROR ❖ [INSTALL]', txt)
    exit(-1)

def MKDIR(dir):
    if not exists( dir ): 
        if not os.path.isdir( dir ):
            try: 
                os.mkdir(dir)
                return False # done
            except OSError:
                ERROR ("Creation of the directory %s failed" % dir)
        else:
            ERROR ("Dir is not dir %s" % dir)
    return True # exists

###############################################################################

def get_ver(item, key):
    if key in item: 
        x = item.find(' ')
        y = item.find(')')
        if x > -1 and y > -1:
            ver[key] = item[ x + 1 : y]

def get_pico_sdk_version( pico_dir ):
    global VER
    f = open( join( pico_dir, 'pico_sdk_version.cmake' ) )
    text = f.read()
    f.close()    
    text = text.strip().split('\n')
    for item in text:
        if False == item.startswith('set(') or item.find(')') == -1 or item.find('$') > -1: continue
        get_ver(item, 'PICO_SDK_VERSION_MAJOR')
        get_ver(item, 'PICO_SDK_VERSION_MINOR')
        get_ver(item, 'PICO_SDK_VERSION_REVISION')
    VER = '%s.%s.%s' % ( ver['PICO_SDK_VERSION_MAJOR'], ver['PICO_SDK_VERSION_MINOR'], ver['PICO_SDK_VERSION_REVISION'] ) 
    return VER     

def get_git_hash( dir, short=True ):
    res = ''
    args = [ 'git', 'rev-parse', '--short' if short else '', 'HEAD' ] # git rev-parse --short HEAD
    proc = Popen(args, stdout=PIPE, stderr=PIPE, cwd=dir)
    out, err = proc.communicate()
    if proc.returncode == 0:
        res = str(out, 'utf-8').upper().replace('\n','') #b'2e6142b\n'
    return res

def get_from_file(filename): 
    res = ''
    if exists( filename ):  
        f= open( filename, 'r' )
        res = f.read(256)
        f.close()
    return res

###############################################################################

def create_folder_gcc( platformio_dir ):
    gcc_dir = join( platformio_dir, 'gcc' )
    if MKDIR( gcc_dir ): return
    f = open( join( gcc_dir, 'gcc-syscall.c' ), 'w' )
    f.write(
'''
#include <sys/stat.h>
extern int __attribute__((weak)) _fstat(int file, struct stat *st){ st->st_mode = S_IFCHR; return 0; }
extern int __attribute__((weak)) _close(int file) { return -1; }
extern int __attribute__((weak)) _isatty(int file) { return 1; }
extern int __attribute__((weak)) _lseek(int file, int ptr, int dir) { return 0; }
extern int __attribute__((weak)) _read(int handle, char *buffer, int length) { return -1; }
extern int __attribute__((weak)) _write(int handle, char *buffer, int length) { return -1; }
'''        
    )
    f.close()

def create_folder_inc( platformio_dir, pico_dir ):
    global VER
    counter = 2
    pico_src_dir = join( pico_dir, 'src' )
    inc_dir = join( platformio_dir, 'inc' )
    if MKDIR( inc_dir ): return
    for root, dirs, files in os.walk( pico_src_dir ):
        if 'host' in root: continue
        if 'include' not in root: continue       
        name = root[ root.index('include') + 8:] # name after include
        MKDIR( join( inc_dir, name ) )
        for file in files:
            ext = pathlib.Path(file).suffix
            if ext == '.h' or ext == '.S':
                src_file = join(root, file)
                dst_file = join(inc_dir, name, file)
                if False == exists( dst_file ): 
                    copyfile( src_file, dst_file )
                    counter += 1
                else: 
                    ERROR('INCLUDE FILE EXISTS: %s' % dst_file)
    INFO('Updated %d files' % counter)
    HASH = get_git_hash( pico_dir )
    if HASH != '': #  write HASH for updates
        f = open( join(platformio_dir, 'HASH'), 'w' )
        f.write(HASH)
        f.close()

###############################################################################

# TODO check dst folder
def create_config_autogen( pico_dir ):
    filename = join( pico_dir, 'src', 'rp2_common', 'pico_platform', 'include', 'pico', 'config_autogen.h' )
    if not exists( filename ): 
        f = open( filename, 'w' ) 
        f.write('// config autogen: PlatformIO')
        f.close()

# TODO check dst folder
def create_version( pico_dir ):
    global VER
    filename = join( pico_dir, 'src', 'rp2_common', 'pico_platform', 'include', 'pico', 'version.h')
    if not exists( filename ): 
        f = open( filename, 'w' ) 
        f.write(
'''
/*
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 * 
 * PlatformIO - WizIO
 * https://github.com/
 */

// ---------------------------------------
// THIS FILE IS AUTOGENERATED; DO NOT EDIT
// ---------------------------------------

#ifndef _PICO_VERSION_H
#define _PICO_VERSION_H

#define PICO_SDK_VERSION_MAJOR      %s
#define PICO_SDK_VERSION_MINOR      %s
#define PICO_SDK_VERSION_REVISION   %s
#define PICO_SDK_VERSION_STRING     "%s < PlatformIO >"

#endif
''' % ( ver['PICO_SDK_VERSION_MAJOR'], ver['PICO_SDK_VERSION_MINOR'], ver['PICO_SDK_VERSION_REVISION'],  VER ) )
        f.close()

###############################################################################

def check_updates( platformio_dir, pico_dir ):
    def RMPIO( platformio_dir ):
        INFO('Updating current config for PICO-SDK %s' % VER)
        shutil.rmtree(platformio_dir, ignore_errors=False)
        time.sleep(1)

    gcc_dir = join(platformio_dir, 'gcc')
    inc_dir = join(platformio_dir, 'inc')
    h_file  = join(platformio_dir, 'HASH')    

    if not exists( pico_dir ):
        #print("[] pico-sdk not exists")
        return -1 # clone      
    elif not exists( platformio_dir ):
        #print("[] platformio_dir not exists")
        return -2 # create     
    elif not exists( gcc_dir ):
        #print("[] gcc_dir not exists")
        RMPIO( platformio_dir )
        return -3
    elif not exists( inc_dir ):
        #print("[] inc_dir not exists")
        RMPIO( platformio_dir )
        return -4
    elif not exists( h_file ):
        #print("[] h_file not exists")
        RMPIO( platformio_dir )                
        return -5

    p_hash = get_git_hash( pico_dir )
    i_hash = get_from_file( h_file  )  
    print("PICO-SDK: %s ( %s )" % (VER, p_hash)) # ✔ 
    if p_hash != i_hash:
        RMPIO( platformio_dir )
        return 0 # wrong hashes
    return 1 # ok

def create_patch( pico_dir ):
    platformio_dir = join( pico_dir, 'platformio' )

    get_pico_sdk_version( pico_dir )

    if 1 == check_updates( platformio_dir, pico_dir ): return

    MKDIR( platformio_dir )  

    create_config_autogen( pico_dir )   
    create_version( pico_dir )    

    create_folder_gcc( platformio_dir ) 
    create_folder_inc( platformio_dir, pico_dir )  

def dev_install( framework_dir ):
    global VER    

    if not exists( framework_dir ): 
        print("[] Framework not exists") 
        return 

    pico_dir = join( framework_dir, 'pico-sdk' )

    if exists( pico_dir ):  
        create_patch( pico_dir ) # if manual install/update
        return 

    ## CLONE BEGIN ##

    start_time = time.time()
    INFO('Clone pico-sdk ( Less than a minute (>100MB), Plese wait )')
    args = [ 'git', 'clone', 'https://github.com/raspberrypi/pico-sdk', pico_dir, '--quiet' ]
    res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin )
    
    if 0 == res['returncode']: 
        INFO('Init submodules ...')
        args = ['git', 'submodule', 'init' , '--quiet' ]
        res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd = pico_dir )

        if 0 == res['returncode']: 
            INFO('Updating submodules ...')
            args = ['git', 'submodule', 'update', '--quiet', pico_dir ]
            res = proc.exec_command( args, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin, cwd = pico_dir )
           
    if 0 != res['returncode']:  
        rmtree(pico_dir, ignore_errors=False)
        ERROR('Result:%d ... Please, try later' % res)

    ## CLONE END   ##

    create_patch( pico_dir ) 

    INFO('PICO-SDK Version: %s' % VER )
    INFO('DONE ( %s sec )' % int( time.time() - start_time ) ) # DONE ( 24 sec )