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
parser.add_argument('-loc', dest="dataLocation", help="")
parser.add_argument('-datafile', dest="dataFile", help="")
parser.add_argument('-scoreboard', dest="scoreboard", help="")
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
sc = fromPath(f"{parent}\\..\\gamehubAPI.py")
scoreboard = sc.scoreboardConnector()
exitFile = os.path.join(parent,"exit.state")

# [Listener]
print(f"\033[33m[SaveService] \033[90mStarted listener in {args.dataFile}\033[0m")
print("\033[33m[SaveService] \033[90mWaiting for tmp file...\033[0m") 
while fs.doesExist(exitFile) == False: _ = ""
print("\033[33m[SaveService] \033[90mContinuing!\033[0m")
while True:
    if fs.doesExist(exitFile) == True:
        fs.deleteFile(exitFile)
        break
    if fs.doesExist(args.dataFile) == True:
        scoreDataJson = fs.readFromFile(args.dataFile)
        scoreData = json.loads(scoreDataJson)
        newScore = scoreData["data"]["score"]
        user = scoreData["user"]
        oldScore = scoreboard.get(args.scoreboard)[user]["score"]
        if int(newScore) > int(oldScore):
            scoreboard.append(args.scoreboard,{user:scoreData["data"]})
            print(f"\033[33m[SaveService] \033[90mWrote new score '{newScore}' for user '{user}'\033[0m")