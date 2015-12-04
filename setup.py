#!/usr/bin/env python3

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [],optimize = 2)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Clan_py3.py', base=base, targetName = 'COC.exe', icon='data\Clan.ico')
]

setup(name='Ceilopty',
      version = '1.0.4',
      description = 'My EXE',
      options = dict(build_exe = buildOptions),
      executables = executables)
