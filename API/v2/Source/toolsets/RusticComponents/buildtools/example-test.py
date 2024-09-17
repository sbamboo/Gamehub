import platform
import os
parent = os.path.dirname(__file__)

from rundll import dynLib

# SETTINGS (Example Scripts)
libpath_win = f"{parent}/../target/x86_64-pc-windows-gnu/debug/RusticComponents.dll"
libpath_lnx = f"{parent}/../target/x86_64-unknown-linux-gnu/debug/libRusticComponents.so"
libpath_mac = f"{parent}/../target/x86_64-apple-darwin/debug/libRusticComponents.dylib"

_platform = platform.system()


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

def safe_call(method):
    # Call the main function from the shared library
    try:
        print(library.runMethod(method))
    except Exception as e:
        print(f"{e}\n\nError calling main() function! (Platform: {_platform})")

safe_call("main()")