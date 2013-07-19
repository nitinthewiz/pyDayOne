import sys
from cx_Freeze import setup, Executable

build_exe_options = {"include_files": ["pyDayOne.ico"],
                     "build_exe": "./bin",
                     "optimize": 2,
                     "icon": 'pyDayOne.ico',
                     "include_msvcr": True,
                     "compressed": True}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "pyDayOne",
        version = "0.1",
        description = "Day One in Python",
        options = {"build_exe": build_exe_options},
        executables = [Executable("pyDayOne.py", base=base)])

