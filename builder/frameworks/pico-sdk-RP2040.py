# LICENSE

import os, pathlib
from os.path import join
from shutil import copyfile
from install import dev_install
from pico_common import DEBUG, ERROR, dev_init_template, dev_init_compiler, dev_init_variables, dev_init_modules

def dev_init(env):
    DEBUG('BEGIN')   

    dev_install(env.platform_dir)
    dev_init_template(env)
    dev_init_compiler(env, env.platform)
    dev_init_variables(env)
    dev_init_modules(env)

    ERROR('The beer got hot !')
