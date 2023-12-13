import ctypes
import platform
import os
parent = os.path.dirname(__file__)

# RusticComponents BuildTool v1.0 (By: Simon Kalmi Claesson)
# This is a python script to execute built dlls

# SETTINGS (Example Scripts)
libpath_win = f"{parent}/../target/x86_64-pc-windows-gnu/debug/RusticComponents.dll"
libpath_lnx = f"{parent}/../target/x86_64-unknown-linux-gnu/debug/libRusticComponents.so"
libpath_mac = f"{parent}/../target/x86_64-apple-darwin/debug/libRusticComponents.dylib"

_platform = platform.system()

class dynLib():
    def __init__(self,libpath):
        self.libpath = libpath
        self.lib = ctypes.CDLL(libpath)

    def get(self):
        return self.lib
    
    def runMethod(self,methodCall=str):
        eval(f"self.lib.{methodCall}")

    def ingest(self):
        for name, func in self._get_library_functions():
            setattr(self, name, self._create_method(func))

    def _get_library_functions(self):
        functions = []
        for name, func in self.lib.__dict__.items():
            if callable(func):
                functions.append((name, func))
        return functions

    def _create_method(self, func):
        def method(*args, **kwargs):
            return func(*args, **kwargs)
        return method

if __name__ == "__main__":
    # Load the appropriate shared library based on the platform
    try:
        if _platform == "Linux":
            library = dynLib(libpath_lnx)
        elif _platform == "Darwin":
            library = dynLib(libpath_mac)
        elif _platform == "Windows":
            library = dynLib(libpath_win)
    except FileNotFoundError as e:
        print(f"{e}\n\nModule not found! (Platform: {_platform})")
        exit()
    except Exception as e:
        print(f"{e}\n\nError loading module! (Platform: {_platform})")
        exit()

    # Call the main function from the shared library
    try:
        library.runMethod("main()")
    except Exception as e:
        print(f"{e}\n\nError calling main() function! (Platform: {_platform})")
        exit()