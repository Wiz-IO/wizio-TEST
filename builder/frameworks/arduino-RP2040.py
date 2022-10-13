# LICENSE: WizIO 2022 Georgi Angelov

from install import dev_install
from pico_common import DEBUG, ERROR, dev_init_template, dev_init_compiler, dev_init_variables, dev_init_modules

def dev_init(env):
    DEBUG('Arduino test')   

    dev_install(env)
    dev_init_compiler(env)    

    ERROR('The beer got hot !')