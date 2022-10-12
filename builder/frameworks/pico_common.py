# LICENSE: WizIO 2022 Georgi Angelov

import os, click
from os.path import join
from shutil import copyfile

TXT_BC = '( binary type config )'
TXT_UC = '( user config )'
TXT_DV = '( default value )'

def INFO(str): 
    print(' ✔', str) 

def DEBUG(str):
    import inspect
    click.echo(click.style( ( '██ [%s] : %s' % (inspect.stack()[1][3], str) ), fg='blue'))

def ERROR(txt):
    click.echo(click.style('✘ [ERROR] : %s'%txt, fg='red'))
    exit(-1)

def dev_init_template(env):
    src_dir = join( env.subst('$PROJECT_DIR'), 'src' )
    tmp_dir = join( env.platform_dir, 'templates', env.sdk )
    for root, void, files in os.walk( src_dir ):
        for file in files:
            if not file.endswith('.c') and not file.endswith('.cpp') and not file.endswith('.cc'): continue
            code = open( join(root, file), 'r').read().replace('\n','').replace('\r','').strip()   
            code = ' '.join( code.split() )        
            if ' main(' in code: return             
    copyfile( join(tmp_dir, 'main.c'), join(src_dir, 'project_main.c') )

def dev_init_compiler(env, sdk_name = 'pico-sdk', application_name = 'APPLICATION'):
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
    env.sdk      = env.GetProjectOption('custom_sdk', sdk_name)               # folder name: < pico-sdk >
    env.SDK_DIR  = env['SDK_DIR']  = join(env.framework_dir, env.sdk, 'src')  # folder path sdk src < ...platformio\packages\framework-NAME\pico-sdk\src >    
    env.INC_DIR  = env['INC_DIR']  = join(env.framework_dir, env.sdk, 'platformio', 'inc')
    env.BOOT_DIR = env['BOOT_DIR'] = join(env.framework_dir, env.sdk, 'platformio', 'boot')
    if env.sdk.startswith('pico-sdk'):
        env.sdk_linker_dir         = join(env.SDK_DIR, 'rp2_common', 'pico_standard_link') # SDK depend
        env.sdk_boot_stage2_dir    = join(env.SDK_DIR, 'rp2_common', 'boot_stage2')        # SDK depend
    else:
        ERROR("NOT SUPPORTED SDK < %s >" % env.sdk)        

    env.cortex          = ['-march=armv6-m', '-mcpu=cortex-m0plus', '-mthumb']   
    env.heap            = env.GetProjectOption('custom_heap', '2048')
    INFO('HEAP          : %s' % (env.heap))
    env.stack           = env.GetProjectOption('custom_stack', '2048')
    INFO('STACK         : %s' % (env.stack))
    env.optimization    = env.GetProjectOption('custom_optimization', '-Os')    # userware
    INFO('OPTIMIZATION  : %s' % (env.optimization))       
 
    INFO('INIT COMPILER : TODO !!!')
    # TODO 
    
def dev_init_variables(env):
    INFO('INIT VARIABLES: TODO !!!')
    # TODO

def dev_init_modules(env):
    INFO('INIT MODULES  : TODO !!!')
    # TODO
