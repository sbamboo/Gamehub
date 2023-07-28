import os
import sys
import argparse
import subprocess
import json
from datetime import datetime

python = sys.executable
parent = os.path.abspath(os.path.dirname(__file__))
quickuseAPI = f"{parent}{os.sep}..{os.sep}..{os.sep}quickuseAPI.py"
managerFile = f"{parent}{os.sep}managers.jsonc"
verFile = f"{parent}{os.sep}..{os.sep}..{os.sep}API.json"

# Arguments
parser = argparse.ArgumentParser(prog="GamehubAPI: BackupService")
parser.add_argument('-apiConfPath',dest='apiConfPath')
parser.add_argument('-scoreboard',dest='scoreboard')
parser.add_argument('-backupStoreMode',dest='backupStoreMode')
parser.add_argument('-backupStoreLocation',dest='backupStoreLocation')
parser.add_argument('--ping',dest='ping',action="store_true")
parser.add_argument('--doCheckExistance',dest='doCheckExistance',action="store_true")
parser.add_argument('--serviceManagerFile',dest='serviceManagerFile',action="store_true",help="ONLY USE WHEN RUNNING service.py DIRECTLY")
args = parser.parse_args()

# Functions
def switchQuotes(string) -> str:
    string = string.replace("'","\uFFFC")
    string = string.replace('"',"'")
    string = string.replace("\uFFFC",'"')
    return string

# Get content of scoreboard
command = f"{python} {quickuseAPI} --qu_get -qu_apiConfPath {args.apiConfPath} -qu_scoreboard {args.scoreboard} --apiConfScoreboardFunc_ovmf"
if args.serviceManagerFile == True: command += f" -qu_managerFile {managerFile}"
output = subprocess.check_output(command, shell=True, text=True)
output = switchQuotes(output)

if "<Response" in output:
    output = '{"GamehubBackupServicePing":{"LatestReponse":"' + output + '"}}'
    args.ping == False

# GenerateTimestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Backup data if asked to
if args.backupStoreMode != "off" and args.backupStoreMode != None:
    if os.path.exists(args.backupStoreLocation):
        scoreboard = args.scoreboard
        loc = f"{os.path.abspath(args.backupStoreLocation)}{os.sep}"
        if args.backupStoreMode == "latest":
            filename_we = f"{loc}{scoreboard}_latest.json"
            if os.path.exists(filename_we): os.remove(filename_we)
            open(filename_we,'w').write(output)
        else:
            filename = f"{timestamp}_{scoreboard}"
            filename_we = f"{loc}{filename}.json"
            i = 1
            while os.path.exists(filename_we) == True:
                filename_we = f"{loc}{filename}_{i}.json"
                i += 1
            open(filename_we,'w').write(output)
        
# Ping if enabled
if args.ping == True:
    # Get scoreboardData
    scoreboardData = json.loads(output)
    # GatherVid
    if os.path.exists(verFile):
        try:
            _json = open(verFile,'r').read()
            verData = json.loads(_json)
            vid = verData["Version"]["Vid"]
        except: vid = "Nan"
    # Generate ping:
    newPing = {
        "GamehubVid": str(vid),
        "Timestamp": str(timestamp),
        "StoreMode": str(args.backupStoreMode)
    }
    # Make sure scoreboard has a ping field
    if scoreboardData.get("GamehubBackupServicePing") == None:
        scoreboardData["GamehubBackupServicePing"] = {}
    # Set old ping to previous
    latest = scoreboardData["GamehubBackupServicePing"].get("Latest")
    if latest != None:
        scoreboardData["GamehubBackupServicePing"]["Previous"] = latest
    # Add new ping
    scoreboardData["GamehubBackupServicePing"]["Latest"] = newPing
    # Replace data
    _json = json.dumps(scoreboardData)
    _json = _json.replace(" ","§s§")
    _json = _json.replace("'","§q§")
    _json = _json.replace('"',"§Q§")
    command = f'{python} {quickuseAPI} --qu_replace -qu_apiConfPath {args.apiConfPath} -qu_scoreboard {args.scoreboard} --apiConfScoreboardFunc_ovmf -qu_dictData "§imf§:{_json}"'
    if args.serviceManagerFile == True: command += f" -qu_managerFile {managerFile}"
    os.system(command)