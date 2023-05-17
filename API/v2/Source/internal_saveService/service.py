# Gamehub saveserice written by Simon Kalmi Claesson
# 
# Obs! This script should only be used through the gamehub api.
#

# [Imports]
import json,os,platform,sys,importlib.util,argparse

# [Importa function]
def fromPath(path):
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# [Arguments]
parser = argparse.ArgumentParser(prog="GamehubAPI_tempFiler")
parser.add_argument('-apiConfpath', dest="apiConfpath", help="Path to the api.conf file, containing info on how to access the API.")
parser.add_argument('-linkedFile', dest="linkedFile", help="Boolean flag, set to False to disable decrypting on the linked file, note! this has to be disabled in the saver aswell.", action="store_true")
parser.add_argument('-exitFile', dest="exitFile", help="Path to the exit.empty file, if this one is found the listener will stop.")
parser.add_argument('--doEncrypt', dest="doEncrypt", help="Boolean flag, set to False to disable decrypting on the linked file, note! this has to be disabled in the saver aswell.", action="store_true")
parser.add_argument('--verbose', dest="verbose", help="Boolean flag, set to False to disable the function writing out what it is doing.", action="store_true")
parser.add_argument('--simpleScore', dest="simpleScore", help="Boolean flag, if set to True the function will handle scores (Only update if newer) Data must be {'score':<intValue>}", action="store_true")
parser.add_argument('autoComsume', nargs='*', help="AutoConsume")
args = parser.parse_args(sys.argv)

# [Window] - Functions from conUtils by Simon Kalmi Claesson
def setConTitle(title):
    # Get platform
    platformv = platform.system()
    # Linux and macOS using ANSI codes
    if platformv in ["Linux", "Darwin"]:
        sys.stdout.write(f"\x1b]2;{title}\x07")
    # Windows using the title command
    elif platformv == "Windows":
        os.system(f'title {title}') # Apply console size with windows.cmd.title
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"
def setConSize(width,height):
    # Get platform
    platformv = platform.system()
    # Linux using resize
    if platformv == "Linux":
        #return "\033[31mError: Platform Linux not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    # Darwin using resize
    elif platformv == "Darwin":
        #return "\033[31mError: Platform Darwin not supported yet!\033[0m"
        os.system(f"resize -s {height} {width}")
    # mode for windows
    elif platformv == "Windows":
        #return "\033[31mError: Platform Windows not supported yet!\033[0m"
        os.system(f'mode con: cols={width} lines={height}') # Apply console size with windows.cmd.mode
    # Error message if platform isn't supported
    else:
        return f"\033[31mError: Platform {platformv} not supported yet!\033[0m"
setConTitle("Gamehub SaveService")
setConSize(60, 15)
# [Setup]
parent = os.path.dirname(__file__)
_fs = fromPath(f"{parent}\\..\\libs\\libfilesys.py")
fs = _fs.filesys
qu = fromPath(f"{parent}\\..\\quickuseAPI.py")

# [Listener]
qu.saveServiceFunction(apiConfPath=args.apiConfPath,linkedFile=args.linkedFile,exitFile=args.exitFile,doEncrypt=args.doEncrypt,verbose=args.verbose,simpleScore=args.simpleScore)