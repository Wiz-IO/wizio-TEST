# LICENSE: WizIO 2022 Georgi Angelov

from os.path import join
from SCons.Script import (AlwaysBuild, DefaultEnvironment, Default)

#print('[---] main.py')

env = DefaultEnvironment()

elf = env.BuildProgram()
'''
bin = env.ELF2BIN( join("$BUILD_DIR", "${PROGNAME}"), elf )
prg = env.Alias( "buildprog", bin, [ env.VerboseAction("", "DONE") ] )
AlwaysBuild( prg )

#print( env.Dump() )

debug_tool = env.GetProjectOption("debug_tool")
if None == debug_tool:
    Default( prg ) # TODO
else:   
    Default( prg )

upload = env.Alias("upload", prg, [ 
        env.VerboseAction("$UPLOADCMD", "Uploading..."),
        env.VerboseAction("", ""),
    ]
)
AlwaysBuild( upload )
'''