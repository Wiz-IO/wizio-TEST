# WizIO 2022 Georgi Angelov

from __future__ import print_function
from os.path import join
from SCons.Script import (AlwaysBuild, Builder, COMMAND_LINE_TARGETS, Default, DefaultEnvironment)
from colorama import Fore

env = DefaultEnvironment()
print( '<<<<<<<<<<<< ' + env.BoardConfig().get("name").upper() + " 2022 Georgi Angelov >>>>>>>>>>>>" )

dev_pioasm(env)

elf = env.BuildProgram()
src = env.ElfToBin( join("$BUILD_DIR", "${PROGNAME}"), elf )
prg = env.Alias( "buildprog", src, [ env.VerboseAction("", "DONE") ] )
AlwaysBuild( prg )

upload = env.Alias("upload", prg, [ 
    env.VerboseAction("$UPLOADCMD", "Uploading..."),
    env.VerboseAction("", ""),
])
AlwaysBuild( upload )    

debug_tool = env.GetProjectOption("debug_tool")
if None == debug_tool:
    Default( prg )
else:   
    Default( prg )

