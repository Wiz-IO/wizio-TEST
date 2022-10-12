# LICENSE

import os, pathlib, click
from os.path import join
from shutil import copyfile

def INFO(str): 
    print(' ✔', str) 

def DEBUG(str):
    import inspect
    click.echo(click.style( ( '██ [%s] : %s' % (inspect.stack()[1][3], str) ), fg='blue'))

def ERROR(txt):
    click.echo(click.style('✘ [ERROR] : %s'%txt, fg='red'))
    exit(-1)

def dev_init_template(env):
    # TODO
    INFO('Init Templates')

def dev_init_compiler(env, sdk_name, application_name = 'APPLICATION'):
    INFO('Init Compiler')
    env.Replace( 
        BUILD_DIR = env.subst('$BUILD_DIR').replace('\\\\', '/'),           # TODO check replace
        AR='arm-none-eabi-ar',
        AS='arm-none-eabi-as',
        CC='arm-none-eabi-gcc',
        GDB='arm-none-eabi-gdb',
        CXX='arm-none-eabi-g++',
        OBJCOPY='arm-none-eabi-objcopy',
        RANLIB='arm-none-eabi-ranlib',
        SIZETOOL='arm-none-eabi-size',
        ARFLAGS=['rc'],
        SIZEPROGREGEXP=r'^(?:\.text|\.data|\.boot2|\.rodata)\s+(\d+).*',    # TODO check
        SIZEDATAREGEXP=r'^(?:\.data|\.bss|\.ram_vector_table)\s+(\d+).*',   # TODO check
        SIZECHECKCMD='$SIZETOOL -A -d $SOURCES',
        SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',           # TODO check BOARD_MCU
        PROGSUFFIX='.elf',
        PROGNAME = application_name 
    )
    # TODO

def dev_init_variables(env):
    INFO('Init Variables')
    # TODO

def dev_init_modules(env):
    INFO('Init Modules')
    # TODO
