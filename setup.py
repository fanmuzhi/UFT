import sys
sys.path.append('src')
from cx_Freeze import setup, Executable

includes = ["atexit", "pyaardvark"]
include_files = [('src/aardvark32.so', 'aardvark32.so'),
                 ('src/aardvark64.so', 'aardvark64.so'),
                 ('src/aardvark32.dll', 'aardvark32.dll'),
                 ('src/aardvark64.dll', 'aardvark64.dll'),
                 ]
#bin_includes = ['src/aardvark32.so', 'src/aardvark64.so']

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

exe = Executable(script="src/UFT/__init__.py", base=base)

setup(
    name="UFT Test Executive",
    version="1.0",
    options={"build_exe": {"includes": includes,
                           "include_files": include_files,
                           #"bin_includes": bin_includes,
                           #"path": sys.path + ['src'],
                           }
             },
    executables=[exe],
    )
