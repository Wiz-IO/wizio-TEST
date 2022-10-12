# LICENSE: WizIO 2022 Georgi Angelov

from install import dev_install
from pico_common import DEBUG, ERROR, dev_init_template, dev_init_compiler, dev_init_variables, dev_init_modules

def dev_init(env):
    DEBUG('Debug test')   

    dev_install(env.framework_dir)
    dev_init_compiler(env)    
    dev_init_template(env)
    dev_init_variables(env)
    dev_init_modules(env)

    ERROR('The beer got hot !')
