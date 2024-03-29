# [Imports]
import os,importlib.util,base64,subprocess,json,platform,sys,re,platform
from datetime import datetime
from scandir import scandir

# [Importa function]
def fromPath(path):
    path = path.replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
parentDir = os.path.dirname(__file__)

# [Dynamic Imports]
gh = fromPath(f"{parentDir}{os.sep}gamehubAPI.py")
_fs = fromPath(f"{parentDir}{os.sep}libs{os.sep}libfilesys.py")
fs = _fs.filesys
def decrypt_string():pass
rsa = fromPath(f"{parentDir}{os.sep}libs{os.sep}libRSA.py")
decrypt_string = rsa.decrypt_string
exec(base64.b64decode("aW1wb3J0IGdldHBhc3MKaW1wb3J0IHNvY2tldAppbXBvcnQgZGF0ZXRpbWUKaW1wb3J0IGhhc2hsaWIKCmRlZiBlbnRyb3B5R2VuZXJhdG9yKCkgLT4gc3RyOgogICAgdXNlciA9IGdldHBhc3MuZ2V0dXNlcigpCiAgICBob3N0ID0gc29ja2V0LmdldGhvc3RuYW1lKCkKICAgIGlwX2FkZHJlc3MgPSBzb2NrZXQuZ2V0aG9zdGJ5bmFtZShob3N0KQogICAgZGF0ZSA9IGRhdGV0aW1lLmRhdGUudG9kYXkoKS5zdHJmdGltZSgnJXktJW0tJWQnKQogICAgZW50cm9weV9zdHIgPSBmJ3t1c2VyfS17aG9zdH0te2lwX2FkZHJlc3N9LXtkYXRlfScKICAgIGVudHJvcHkgPSBoYXNobGliLnNoYTI1NihlbnRyb3B5X3N0ci5lbmNvZGUoKSkuaGV4ZGlnZXN0KCkKICAgIHJldHVybiBlbnRyb3B5CgpkZWYgZ2V0U2FmZUNvbmZpZ0tleSgpIC0+IHN0cjoKICAgIHJldHVybiAiLS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tXG5NSUlFdlFJQkFEQU5CZ2txaGtpRzl3MEJBUUVGQUFTQ0JLY3dnZ1NqQWdFQUFvSUJBUURlT1dORGxwOHZmVnNrXG5CaG4xWThKUnZoVFRJS2pDR3NyS1NGbmR6d21hU0hLSjNhQWVzVWE2SGpBTzV6MGpjOUpyQVp2SGZ3eUFHZDQzXG5TOHhkL2x1SkFtcU5HcHNZZitvZU5tZ2ZLdTNTaDh2Yjd6dGxXcndsMUdEVG1KaXZsdjVGYnAyeGdldFZyczJFXG55NStTNThRZlpTZlVJVGNqYVFMbHhaOVZ5S084dk1pdDJsYkUvWkFaazJwYU00ZzJkeHQwV2MxRm5zRnY3TXdwXG5sekttRitteWpVRHNhbGo2TGxsbUxJM05kN2pSQkNaZis2dmVlWURSWE1xVjJ3UnhGd3pPbm5VODFTUmJrS3B2XG5pODgyU09hMnVaYzI5d3RWWjVtTjJQTUQ1cEFnSElsNXJWdU16WGhVWjA4bVhMY2I1cWRnc01zRmRsWTdkT0psXG4zUjNvSnFCeEFnTUJBQUVDZ2dFQVU4bURlY3BpdnI4ZkRCZ1kxWU1GazFoOTlaVE16RkxadnlkRWF2TlRCWTduXG5VTC8xVFYwOTg1TEtQL1JFQXdmNmdFb2MrRDBZODN2Tll6LzdFRDJGT2NWbGMwcGl5L3YrdytGenBMekU2cW8wXG4zUG40aFNDTzdCeUZYWUtkbnlicFBEaVcwSVRSdkg2cUVyWEx0dElZQ2xaVGpCSHgvakhyMjhLRmJ3eTFYOFdDXG5YRTZpeDZVMTUyNysrb2RvbmtoU29EYVlvWHBLVmkyMnNka1ZUaUtuY2RWZUVBUHl4dTRTVUQ5K01mZi9heDd1XG5rTHpQMWJ1c3VpeGpUc0szYTRJbW5EQituTWh0b1B6RjZwUWVtUDVOWENNRFh2VHhRcHJ3VkJyUWZSZ3lOekg2XG5QMWpkTGlYSTkwcEpJL3lDeXpITmt4Rmo2aXNKUHlnSmpvbTVXRmE4dVFLQmdRRG5uT2JkdmE3NGx1R0tRQzliXG5SbXhpc0tpUS9LUFpRMkhOcE9ubFNidHNnSnd3SjlIYXJlMDJsT1ZwYjBEQmQ4TVVreENEWjJ4dSs4TFR1ZmNTXG4ycTVRTTJsZGNpN0Z3Rk5Nd2lYM2JzeVFveGIzQmluQVRwelF6dlh0ckUydmpFMjc4T1I2WnFib0FtWVQ1UFd5XG5qZFVhZWFCYngyeFVzTmFBTk10czZYK1ZLd0tCZ1FEMW4ybjJFcTY5TEdmcmtKMlpEMGRISmk4cVFmSkV1aHFaXG5FM0ZJdWo3aVRpelM5eXlJTnJ6b0VteTVaUGV4VFdDMmQvTnJhQ2gvcDJJcmRMNkZWNUdZbHowRlFSNDdpR3ZrXG4vT3dUOEl0SzdMS2x6bUNDU3RzL1JxZkx3dUZOVXZqSnY5NWNiTGJUKzF3ckxIVXV0QVdtSVlic2tFbi9IWDN5XG41WTBGS1FFSzB3S0JnSEZlcE1iZlJSa2JTWlRSYkJ6Q2NPVXgwYUQrZVBrcytWK2VuSHFHUjc2SmlXb3M0NVNsXG4wOW9Hc2ZDVTYxNkh6NjV2ZWdMSUNoU2RHVFZuN3ArRStSUDZ4bFZlUWJTOE9rbjFNbjVWOXIzSmhzRXRmQnhNXG5ub2U2OWpmN1FoOXVqdEl5ekxONU1iT1pFUHdsODNvTjRNVFB5Z1dDck8wYmpqTTlKR0hRUFluM0FvR0FlbEovXG50THF0Snl6OFBBWnpWZ3lUMU0waFpBd2ZtVGFObEhwb1NtM21iMUc3WlAwUHdtNXdPYXNqVmxrQU9kNXRNYklmXG5HZmh2WXRON1FtVUxsT0I5Yzk2dDF2WU5GbHprVHMvZXlqZGJSMThGd1NrOFN1YjR0VlI4c0M5SGdQaTNTZEl4XG43UmwvRzZic3lkdUVLRlFqRkE5U1lIR2pTRmZwcDVQR1hUR0VnVjBDZ1lFQXVSbERiUmZNT0VFVkx4bEx3VmttXG40K0pjRTNGck9NVjh6RlZRSEQ4NXlKeDhuRGxGNlU3TE5FMmZTUzRRbkdtNVA4OUVBYjV2UGMrZkJma21ZSVBRXG5RVDY5TXJuOFhpZmxKa1I4elVtVFJlditqeVB2WFZ3dlRISDYwb3F0VnZJeGF1cFoveWJNSnVzazN6bTZWMmdWXG4vYkUvVXRhM0YwN2hkYVdQMjlzampqQT1cbi0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS1cbiI=").decode("utf-8"))
libhasher = fromPath(f"{parentDir}{os.sep}libs{os.sep}libhasher.py")
hashFile = libhasher.hashFile
hashString = libhasher.hashString

# [SubFunctions]
# Filesys scantree function
def _scantree(path=str()):
    try:
        for entry in scandir(path):
            if entry.is_dir(follow_symlinks=False):
                yield from filesys.scantree(entry.path)
            else:
                yield entry
    except:
        pass
def _filterBackupServiceFiles(filesList):
    matchingFiles = []
    for file in filesList:
        # Match the file name using regular expressions
        match = re.match(r"^(.+)_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(?:_\d+)?\.json$", file)
        if match:
            matchingFiles.append(file)
    return matchingFiles
def _latestFile(filesList):
    if filesList == None: return None
    currentTime = datetime.now()
    latestFile = None
    latestDatetime = None
    for file in filesList:
        try:
            fileDatetime = datetime.strptime(file, "%Y-%m-%d_%H-%M-%S")
            if fileDatetime > latestDatetime:
                latestFile = file
                latestDatetime = fileDatetime
        # If the file has an invalid format, ignore it
        except ValueError:
            pass
    return latestFile

# Function to handle userData
def gamehub_userData(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        scoreboard=str(),user=None,dictData=None,
        saveUser=False,getUser=False,updateUser=False,getAllUsers=False, doesExist=False,mRemove=False,
        doCheckExistance=None, autoHandlePingRemoval=True, autoFindGlobalManagerFile=True
    ):
    # Create scoreboardConnector
    scoreboard = gh.scoreboardConnector(encryptionType=encType, storageType=manager, key=apiKey, kryptographyKey=encKey, managersFile=managerFile, ignoreManagerFormat=ignoreManFormat, doCheckExistance=doCheckExistance, autoHandlePingRemoval=autoHandlePingRemoval, autoFindGlobalManagerFile=autoFindGlobalManagerFile)
    # Actions
    if saveUser == True:
        if user != None and dictData != None:
            _dict = {user: dictData}
            jsonData = json.dumps(_dict)
            return scoreboard.create(scoreboard=scoreboard,jsonDict=jsonData)
    elif mRemove == True: # 3 requests
        # get data from scoreboard
        _json = scoreboard.get(scoreboard=scoreboard)
        try: _dict = json.loads(_json)
        except: return _json
        # remove user
        _dict.pop(user)
        # create scoreboard with modified data
        scoreboard.replace(scoreboard=scoreboard,jsonDict=_dict)
    elif getUser == True:
        _json = scoreboard.get(scoreboard=scoreboard)
        try: _dict = json.loads(_json)
        except: return _json
        return _dict[user]
    elif updateUser == True:
        _dict = {user: dictData}
        jsonData = json.dumps(_dict)
        return scoreboard.append(scoreboard=scoreboard,jsonDict=jsonData)
    elif doesExist == True:
        return scoreboard.doesExist(scoreboard=scoreboard)
    elif getAllUsers == True:
        return scoreboard.get(scoreboard=scoreboard)

# Function to save data for singleSave to be able to load it
def gamehub_singleSavePrep(
        tempFolder=str(),fileName=str(),encrypt=True,
        scoreboard=str(),user=str(),data=dict()
    ):
    if encrypt == True:
        securityLevel = 2
        encType = "aes"
        encKey = entropyGenerator()
    else:
        securityLevel = 0
        encType = None
        encKey = None
    # Prep settings data
    _data = {
        "scoreboard": scoreboard,
        "user": user,
        "data": data
    }
    _json = json.dumps(_data)
    # Save settings data
    gh.saveDict(securityLevel=securityLevel,encType=encType,encKey=encKey,tempFolder=tempFolder,fileName=fileName,jsonStr=_json)
    encKey = None
# Function to load and upload an existing file
def gamehub_singleSave(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        tempFolder=str(),fileName=str(), encrypt=True,
        doCheckExistance=None, autoHandlePingRemoval=True, autoFindGlobalManagerFile=True
    ):
    if encrypt == True:
        securityLevel = 2
        _encType = "aes"
        _encKey = entropyGenerator()
    else:
        securityLevel = 0
        _encType = None
        _encKey = None
    # Load data
    _dict = gh.loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
    _encKey = None
    # Update data
    _jsonData = json.loads( {_dict["user"] : _dict["data"]} )
    gh.gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], jsonData=_jsonData, append=True, doCheckExistance=doCheckExistance,autoHandlePingRemoval=autoHandlePingRemoval,autoFindGlobalManagerFile=autoFindGlobalManagerFile)
# Function to load and upload an existing file (SCORE)
def gamehub_singleSave_score(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        tempFolder=str(),fileName=str(), encrypt=True,
        doCheckExistance=None, autoHandlePingRemoval=True, autoFindGlobalManagerFile=True
    ):
    if encrypt == True:
        securityLevel = 2
        _encType = "aes"
        _encKey = entropyGenerator()
    else:
        securityLevel = 0
        _encType = None
        _encKey = None
    # Load data
    _dict = gh.loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
    _encKey = None
    user = _dict["user"]
    # Get Current Data
    current = gh.gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], get=True, doCheckExistance=doCheckExistance,autoHandlePingRemoval=autoHandlePingRemoval,autoFindGlobalManagerFile=autoFindGlobalManagerFile)
    # Check
    if current.get(user) == None:
        current[user] = {"score":"-1"}
    if int(current[user]["score"]) < int(_dict["data"]["score"]):
        _jsonData = {_dict["user"] : _dict["data"]}
        gh.gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], jsonData=_jsonData, append=True, doCheckExistance=doCheckExistance,autoHandlePingRemoval=autoHandlePingRemoval,autoFindGlobalManagerFile=autoFindGlobalManagerFile)

# Function to sort a scoreboard
def sortScoreboard(scoreboardDict=dict):
    return dict(sorted(scoreboardDict.items(), key=lambda item: int(item[1]["score"]), reverse=True))
def sortScoreboardJson(scoreboardJson=str):
    sortedDict = sortScoreboard(json.loads(scoreboardJson))
    return json.dumps(sortedDict)

# Function to remove comments from json
def removeComments(json_string):
    '''function to strip comments from a raw json string and returns the stripped string'''
    # Match and remove single-line comments that start with //
    pattern = r"(^|\s)//.*$"
    without_comments = re.sub(pattern, "", json_string, flags=re.MULTILINE)
    return without_comments

# Function to handle apiConfigs
def getAPIConfig(apiConfPath=str()) -> dict:
    secureFileEndings = ["sconf","sconfig","secConf","secConfig","ghsc","gh_sconf","gh_sconfig"]
    # Get content
    content = open(apiConfPath,'r').read()
    # Check if secure
    if (os.path.basename(apiConfPath).split("."))[-1] in secureFileEndings:
        #DecryptContent
        content = decrypt_string(content,getSafeConfigKey())
    # Return content
    content = removeComments(content)
    return json.loads(content)

# ScoreboardConnector
class apiConfigScoreboardConnector(gh.scoreboardConnector):
    def __init__(self,apiConfPath=str(), doCheckExistance=None, autoHandlePingRemoval=True, autoFindGlobalManagerFile=True):
        self.apiData = getAPIConfig(apiConfPath)
        super().__init__(encryptionType=self.apiData["encType"], storageType=self.apiData["storageType"], key=self.apiData["apiKey"], kryptographyKey=self.apiData["encKey"], managersFile=self.apiData["managerFile"], ignoreManagerFormat=self.apiData["ignoreManagerFormat"],doCheckExistance=doCheckExistance,autoHandlePingRemoval=autoHandlePingRemoval,autoFindGlobalManagerFile=autoFindGlobalManagerFile)

# wrapper for gamehubAsAFunction
def apiConfig_gamehub_scoreboardFunc(apiConfPath,scoreboard=str(),jsonData=None, create=False,remove=False,get=False,append=False,replace=False, doesExist=False, managerOverwrite=None, doCheckExistance=None, autoHandlePingRemoval=True, autoFindGlobalManagerFile=True):
    _d = getAPIConfig(apiConfPath)
    if managerOverwrite != None: _d["managerFile"] = managerOverwrite
    if jsonData != None: jsonData = json.loads(jsonData)
    return gh.gamehub_scoreboardFunc(encType=_d["encType"],manager=_d["storageType"],apiKey=_d["apiKey"],encKey=_d["encKey"],managerFile=_d["managerFile"],ignoreManFormat=_d["ignoreManagerFormat"],_scoreboard=scoreboard,jsonData=jsonData,create=create,remove=remove,get=get,append=append,replace=replace,doesExist=doesExist,doCheckExistance=doCheckExistance,autoHandlePingRemoval=autoHandlePingRemoval,autoFindGlobalManagerFile=autoFindGlobalManagerFile)

# Function to prep a file for the saveService
def saveServicePrep(linkedFile=str(),doEncrypt=True, scoreboard=str(),user=str(),data=dict()):
    _path = os.path.dirname(linkedFile)
    _file = os.path.basename(linkedFile)
    gamehub_singleSavePrep(tempFolder=_path,fileName=_file,encrypt=doEncrypt,scoreboard=scoreboard,user=user,data=data)

# EasyPass
def _ep(inp):
    if inp.lower() == "false": inp == False
    elif inp.lower() == "true": inp == True
    elif inp.lower() == "None": inp == None
    elif inp.lower() == "": inp == None
    return inp

# LinkFileExist
def _linkFileExist(linkedFile) -> bool:
    name = os.path.basename(linkedFile)
    fending = (os.path.basename(linkedFile).split("."))[-1]
    hname = hashString(message=name, hashType="sha256")
    hpath = linkedFile.replace(name, f"{hname}.ghs" )
    exi = fs.doesExist(linkedFile) or fs.doesExist(hpath)
    return exi

# SaveServiceFunction - This is used either by the service.py or internally
def saveServiceFunction(apiConfPath=str(),linkedFile=str(),exitFile=str(),doEncrypt=True,verbose=True,simpleScore=False):
    '''
    apiConfPath: Path to the api.conf file, containing info on how to access the API.
    exitFile: Path to the exit.empty file, if this one is found the listener will stop.
    linkedFile: Path to the linked file, the service will listen for this file and upload data from it, if it is diffrent then previously seen data.
    doEncrypt: Boolean flag, set to False to disable decrypting on the linked file, note! this has to be disabled in the saver aswell.
    verbose: Boolean flag, set to False to disable the function writing out what it is doing.
    simpleScore: Boolean flag, if set to True the function will handle scores (Only update if newer) Data must be {"score":<intValue>}
    '''
    apiConf = getAPIConfig(apiConfPath)
    previousContent = str()
    # Init scoreboard connector
    conn = gh.scoreboardConnector(encryptionType=_ep(apiConf["encType"]), storageType=_ep(apiConf["storageType"]), key=_ep(apiConf["apiKey"]), kryptographyKey=_ep(apiConf["encKey"]), managersFile=_ep(apiConf["managerFile"]), ignoreManagerFormat=_ep(apiConf["ignoreManagerFormat"]))
    # Prep dict settings
    securityLevel,_encType,_encKey = 0,None,None
    if doEncrypt == True:
        securityLevel,_encType,_encKey = 2,"aes",entropyGenerator()
    # Look for first file, as a startup
    if verbose: print(f"\033[33m[SaveService] \033[90mStarted listener on {linkedFile}\033[0m")
    if verbose: print("\033[33m[SaveService] \033[90mWaiting for tmp file...\033[0m")
    while _linkFileExist(linkedFile) == False: 
        if fs.doesExist(exitFile) == True:
            break
    # Loop through the file and listen for changes
    if verbose: print("\033[33m[SaveService] \033[90mContinuing!\033[0m")
    while True:
        # Check for exit file
        if fs.doesExist(exitFile) == True:
            fs.deleteFile(exitFile)
            if verbose: print("\033[33m[SaveService] \033[90mStopped!\033[0m")
            break
        # Listen for content
        if _linkFileExist(linkedFile) == True:
            # Get current content
            tempFolder = os.path.dirname(linkedFile)
            fileName = os.path.basename(linkedFile)
            content = gh.loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
            user = content["user"]
            scoreboard = content["scoreboard"]
            data = content["data"]
            # If simpleScore prep data
            if simpleScore == True:
                currentData = conn.get(scoreboard)
                currentUser = currentData.get(user)
                if currentUser != None: currentScore = currentUser["score"]
                else: currentScore = 0
                newScore = data["score"]
                if int(newScore) > int(currentScore):
                    if verbose: print(f"\033[33m[SaveService] \033[90mUpdated score for user '{user}' from '{currentScore}' to '{newScore}'\033[0m")
                    conn.append(scoreboard,{user:data})
            # Normal upload
            else:
                conn.append(scoreboard,{user:data})
                if verbose: print(f"\033[33m[SaveService] \033[90mUpdated data for user '{user}'\033[0m")
                
# Functions to work with the saveService (Files should be saved with saveServicePrep() with encryption by default)
def gamehub_saveService_on(pyPath="python3",apiConfPath=str(),linkedFile=str(),exitFile=str(),doEncrypt=True,verbose=True,simpleScore=False):
    # General setup of enviroment
    if os.path.exists(exitFile): os.remove(exitFile)
    # Setup base command
    current_os = platform.system()
    if current_os == 'Windows':
        command = ['cmd.exe', '/c', 'start']
        creation_flags = subprocess.DETACHED_PROCESS
    elif current_os == 'Linux':
        command = ['x-terminal-emulator', '-e']
        creation_flags = subprocess.CREATE_NEW_CONSOLE
    elif current_os == 'Darwin':  # macOS
        command = ['open', '-a', 'Terminal']
        creation_flags = subprocess.CREATE_NEW_CONSOLE
    else: raise NotImplementedError(f'Unsupported operating system: {current_os}')
    # Setup command
    command2 = [pyPath, f"{os.path.dirname(__file__)}{os.sep}internal_services{os.sep}save{os.sep}service.py", "-apiConfpath", apiConfPath, "-linkedFile", linkedFile, "-exitFile", exitFile]
    if current_os == 'Darwin': command2.pop(0)
    for e in command2: command.append(e)
    if doEncrypt == True: command.append("--doEncrypt")
    if verbose == True: command.append("--verbose")
    if simpleScore == True: command.append("--simpleScore")
    # Execute Service
    subprocess.Popen(command, creationflags=creation_flags)
    #subprocess.Popen(command, startupinfo=startupinfo if hidden else None)

def gamehub_saveService_off(exitFile=str()):
    if os.path.exists(exitFile): os.remove(exitFile)
    open(exitFile,'w').write("1")

# BackupSystem
def gamehub_backupService(mode="schedule",pythonPathOverwrite=None,scoreboard=str,apiConfPath=None,backupStoreMode="off",backupStoreLocation=None,ping=False,backupInterval=None,breakFilePath=None,serviceManagerFile=None,pingMessage=None):
    '''
    mode: 'schedule' or 'unschedule' or 'breakLoopExecute' or 'restoreLatest'
    pythonPathOverwrite: Overwriting python path
    apiConfPath: Path to apiconfig provider file (to set which scoreboard to update)
    scoreboard:  The scoreboard to backup/ping
    backupStoreMode:
        "off":    No backups are saved.
        "on":     All backups are saved.
        "latest": Only latest backup is saved.

    backupStoreLocation: Where to store backups (if enabled by the StoreMode)
    ping: Updates the scoreboard with some ping information, under key: 'GamehubBackupServicePing'
    backupInterval: How often to schedule the service:
        'Once':       Runs service once but dosen't schedule it.
        < 1_minutes:  Asks you if you wan't to run loopExecute (Loops until CTRL+C or similar)
        <int>_<unit>, Example: 1_minutes/24_Hours (Allowed units: minutes, hours, days, weeks, months)
    breakFilePath: A path to a breakfile incase using loopExecute.
    serviceManagerFile: boolean to if should use the service's internal manager file.
    '''
    if mode == None: mode = "schedule"
    if backupStoreMode == None: backupStoreMode = "off"
    if serviceManagerFile == "": serviceManagerFile == None
    # Unix message
    if platform.system() != "Windows":
        print("OBS! This functionality uses libschedule, on unix if a schedule dosen't run you should run unixSetup.py, look at documentation for this in: libs/libschedule/readme.txt!")
        confirm = input("Have you read readme.txt and made neccesairy actions? [y/n] ")
        if confirm.lower() != "y":
            print("PLESE READ readme.txt! (Breaking...)")
            return
    # Variable Define
    if pythonPathOverwrite != None:
        python = pythonPathOverwrite
    else:
        python = sys.executable
    parent = os.path.abspath(os.path.dirname(__file__))
    service = f"{parent}{os.sep}internal_services{os.sep}backup{os.sep}service.py"
    command = f'-apiConfPath "{apiConfPath}" -scoreboard "{scoreboard}"'
    cliWrapper = f"{parent}{os.sep}libs{os.sep}libschedule{os.sep}cliWrapper.py"
    # Add once to pingMessage
    if backupInterval == None: backupInterval == ""
    if str(backupInterval).lower() == "once":
        if pingMessage == None or pingMessage == "":
            pingMessage = "Interval:Once"
        else:
            pingMessage = "Interval:Once; " + pingMessage
    # Add non required variables
    if backupStoreMode != None and backupStoreMode != "off":
        command += f' -backupStoreMode "{backupStoreMode}"'
    if backupStoreLocation != None and backupStoreLocation != "":
        command += f' -backupStoreLocation "{backupStoreLocation}"'
    if ping != None and ping != False:
        command += f' --ping'
    if serviceManagerFile != None:
        command += f' --serviceManagerFile'
    if pingMessage != None and pingMessage != "":
        command += f' -pingMessage "{pingMessage}"'
    # Generate scheduleCommand
    scommand = f'{python} {cliWrapper} -task_name "{scoreboard}" -python_path "{python}" -script_path "{service}" -script_args "{command}" -interval_str "{backupInterval}"'
    if breakFilePath != None and breakFilePath != "":
        scommand += f' -break_file_path "{breakFilePath}"'
    # execute service
    if mode.lower() == "schedule":
        # Once
        if backupInterval.lower() == "once":
            os.system(f"{python} {service} {command}")
        # Interval
        else:
            if backupInterval != "":
                scommand += " --schedule"
                os.system(scommand)
            else:
                print("No backup interval given!")
                return
    # Break loopExecute
    elif mode.lower() == "breakloopexecute":
        if os.path.exists(breakFilePath): os.remove(breakFilePath)
        open(breakFilePath,"w").write("1")
    # Restore latest backup
    elif mode.lower() == "restoreLatest":
        if backupStoreLocation != None:
            currentBackupFiles = _scantree(backupStoreLocation)
            if backupStoreMode == "on":
                currentBackupFiles_filtered = _filterBackupServiceFiles(currentBackupFiles)
                latestFile = _latestFile(currentBackupFiles_filtered)
            elif backupStoreMode == "off":
                pass
                # Get _latest file independing on filename and set as latestFile
            # get json and deserialize to a dictionary
            # now accually send the gamehubAPI request to replace the dictionary
    # Unschedule
    else:
        scommand = f'{python} {cliWrapper} -task_name "{scoreboard}" --unschedule'
        os.system(scommand)

def gamehub_backupService_auto20Days(apiConfPath,scoreboard,ping=False,loc=os.path.join(os.path.abspath(parentDir), f"internal_services{os.sep}backup{os.sep}backups")):
    if os.path.exists(loc) != True: os.mkdir(loc)
    gamehub_backupService(scoreboard=scoreboard,apiConfPath=apiConfPath,backupStoreMode="latest",backupStoreLocation=loc,ping=ping,backupInterval="20_days",serviceManagerFile=True,pingMessage="Auto20")

def gamehub_backupService_quickUnshedule(apiConfPath,scoreboard):
    gamehub_backupService(mode="unschedule",apiConfPath=apiConfPath,scoreboard=scoreboard)
# TODO: Add restoreFromLatestBackup and the ability to autoDetect removal and autoRestore to the gamehub_backupService function

def _imfProtocol(string):
    if "§imf§:" in str(string):
        string = string.replace("§s§"," ")
        string = string.replace("§q§","'")
        string = string.replace("§Q§",'"')
        string = string.replace("§imf§:","")
    if "!imf-swq!" in string:
        string = string.replace("'","!q!")
        string = string.replace('"',"!dq!")
        string = string.replace("!q!",'"')
        string = string.replace("!dq!","'")
        string = string.replace("!imf-swq!","")
    return string

# ========================================================[CLI Executor]========================================================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="quickuseAPI")
    # Flags
    ## [QuickuseFunctions]
    parser.add_argument('--userData', dest="qu_userData", action='store_true', help="Userdata handler (EXPERIMENTAL)")
    parser.add_argument('--singleSavePrep', dest="qu_prep", action='store_true', help="Savedata in a format compatable with the singleSave system.")
    parser.add_argument('--singleSave', dest="qu_save", action='store_true', help="Uploads data saved with the prep function (EXPERIMENTAL)")
    parser.add_argument('--singleSave_score', dest="qu_savescore", action='store_true', help="Uploads data saved with the prep function but handles scores and uploads incrementaly (EXPERIMENTAL)")
    parser.add_argument('--apiConfScoreboardFunc', dest="qu_apiconfFunc", action='store_true', help="Wrapper for gamehubAPI's asFunction function but uses the APIconf system.")
    parser.add_argument('--apiConfScoreboardFunc_ovmf', dest="qu_apiconfFunc_ovmf", action='store_true', help="Same as normal but takes a managerFormat argument to overwrite the apiConf one.")
    ## [BackupService]
    parser.add_argument('--backupService', dest="bs_backupService", action='store_true', help="Service for backing up scoreboards.")
    parser.add_argument('--backupServiceAuto20', dest="bs_backupServiceA20", action='store_true', help="Auto 20days scheduler.")
    parser.add_argument('--backupServiceUnshedule', dest="bs_backupServiceUnshedule", action='store_true', help="Auto 20days scheduler.")
    ## [SaveService]
    parser.add_argument('--saveServiceFunction', dest="ss_function", action='store_true', help="The main function that listens for updates and uploads them. (Import to create custom backgroundListener)")
    parser.add_argument('--saveServicePrep', dest="ss_prep", action='store_true', help="Prepare data to be uploaded by the listener. (saves it to temp)")
    parser.add_argument('--saveService_on', dest="ss_on", action='store_true', help="Calls the buildint background listener (see params)")
    parser.add_argument('--saveService_off', dest="ss_off", action='store_true', help="Turns off a background listener (see params)")
    ## [Internal]
    parser.add_argument('--internal_ep', dest="it_ep", action='store_true', help="EasyPass (Takes string and None/Bool casts it)")
    parser.add_argument('--internal_linkFileExist', dest="it_linkFexi", action='store_true', help="Does a link file exist?")
    parser.add_argument('--internal_getAPIConfig', dest="it_getApiConf", action='store_true', help="Gets the apiConf data and handles secure-config")
    ## [Others]
    parser.add_argument('--sortScoreboardJson', dest="ot_sort", action='store_true', help="Sorts a json scoreboard and returns json (Takes string)")
    ## [General]
    parser.add_argument('autoComsume', nargs='*', help="AutoConsume")
    # Arguments
    ## [QuickuseFunctions]
    parser.add_argument('-qu_encType', dest="qu_encType", help="QuickuseFuncs: EncryptionType to use for the APIkey (str)")
    parser.add_argument('-qu_encKey', dest="qu_encKey", help="QuickuseFuncs: EncryptionKey to use for the APIkey encryption (str)")
    parser.add_argument('-qu_manager', dest="qu_manager", help="QuickuseFuncs: Manager/StorageType to save too (str)")
    parser.add_argument('-qu_apiKey', dest="qu_apiKey", help="QuickuseFuncs: API key (str)")
    parser.add_argument('-qu_managerFile', dest="qu_managerFile", help="QuickuseFuncs: ManagerFile to use 'GLOBAL' for builtins (str)")
    parser.add_argument('--qu_ignoreManFormat', dest="qu_ignoreManFormat", action="store_true", help="QuickuseFuncs: ignoreManFormat?")
    parser.add_argument('-qu_scoreboard', dest="qu_scoreboard", help="QuickuseFuncs: Scoreboard to save to (str)")
    parser.add_argument('-qu_user', dest="qu_user", help="QuickuseFuncs: User to save to (str)")
    parser.add_argument('-qu_dictData', dest="qu_dictData", help="QuickuseFuncs: Data to save to user (JSONstr)")
    parser.add_argument('--qu_saveUser', dest="qu_saveUser", action="store_true", help="QuickuseFuncs: saveUser")
    parser.add_argument('--qu_getUser', dest="qu_getUser", action="store_true", help="QuickuseFuncs: getUser")
    parser.add_argument('--qu_updateUser', dest="qu_updateUser", action="store_true", help="QuickuseFuncs: updateUser")
    parser.add_argument('--qu_getAllUsers', dest="qu_getAllUsers", action="store_true", help="QuickuseFuncs: getAllUsers")
    parser.add_argument('--qu_doesExist', dest="qu_doesExist", action="store_true", help="QuickuseFuncs: doesExist")
    parser.add_argument('--qu_mRemove', dest="qu_mRemove", action="store_true", help="QuickuseFuncs: mRemove")
    parser.add_argument('-qu_tempFolder', dest="qu_tempFolder", help="QuickuseFuncs: TemporaryFolder, generation of this is recomended! (str)")
    parser.add_argument('-qu_fileName', dest="qu_fileName", help="QuickuseFuncs: fileName of temp file! (str)")
    parser.add_argument('--qu_encrypt', dest="qu_encrypt", action="store_true", help="QuickuseFuncs: Encrypt?! (bool)")
    parser.add_argument('-qu_apiConfPath', dest="qu_apiConfPath", help="QuickuseFuncs: APIconf path (str)")
    parser.add_argument('--qu_create', dest="qu_create", action="store_true", help="QuickuseFuncs: create method (bool)")
    parser.add_argument('--qu_replace', dest="qu_replace", action="store_true", help="QuickuseFuncs: replace method (bool)")
    parser.add_argument('--qu_remove', dest="qu_remove", action="store_true", help="QuickuseFuncs: remove method (bool)")
    parser.add_argument('--qu_get', dest="qu_get", action="store_true", help="QuickuseFuncs: get method (bool)")
    parser.add_argument('--qu_append', dest="qu_append", action="store_true", help="QuickuseFuncs: append method (bool)")
    parser.add_argument('--qu_doCheckExistance', dest="qu_doCheckExistance", action="store_true", help="QuickuseFuncs: doCheckExistance flag (bool)")
    parser.add_argument('--qu_autoHandlePingRemoval', dest="qu_autoHandlePingRemoval", action="store_true", help="QuickuseFuncs: autoHandlePingRemoval flag (bool)")
    parser.add_argument('--qu_autoFindGlobalManagerFile', dest="qu_autoFindGlobalManagerFile", action="store_true", help="QuickuseFuncs: autoFindGlobalManagerFile flag (bool)")
    ## [BackupService]
    parser.add_argument('-bs_apiConfPath', dest="bs_apiConfPath", help="BackupService: APIconf path (str)")
    parser.add_argument('-bs_scoreboard', dest="bs_scoreboard", help="BackupService: Scoreboard to backup/ping (str)")
    parser.add_argument('-bs_backupMode', dest="bs_backupMode", help="BackupService: StorageMode, Can be 'off', 'on' or 'latest's (str)")
    parser.add_argument('-bs_backupLoc', dest="bs_backupLoc", help="BackupService: Where to store backups (str)")
    parser.add_argument('--bs_ping', dest="bs_ping", help="BackupService: If given pings the scoreboard (bool)",action="store_true")
    parser.add_argument('-bs_pingMessage', dest="bs_pingMessage", help="BackupService: Adds a message to the ping (str)")
    parser.add_argument('-bs_interval', dest="bs_interval", help="BackupService: How often to schedule the service, <int>_<unit>, Example: 1_minutes (bool)")
    parser.add_argument('-bs_mode', dest="bs_mode", help="BackupService: Execution mode, can be: 'schedule', 'unschedule' or 'breakLoopExecute' (str)")
    parser.add_argument('-bs_pythonPathOverwrite', dest="bs_pythonPathOverwrite", help="BackupService: Optional python path overwrite (str)")
    parser.add_argument('-bs_breakFilePath', dest="bs_breakFilePath", help="BackupService: Path to breakfile incase using loopExecute (str)")
    parser.add_argument('--bs_serviceManagerFile', dest="bs_serviceManagerFile", help="BackupService: Uses the backupServices internal manager file (str)",action="store_true")
    ## [SaveService]
    parser.add_argument('-ss_apiConfPath', dest="ss_apiConfPath", help="SaveService: APIconf path (str)")
    parser.add_argument('-ss_linkedFile', dest="ss_linkedFile", help="SaveService: LinkedFile path (str)")
    parser.add_argument('-ss_exitFile', dest="ss_exitFile", help="SaveService: ExitFile path (str)")
    parser.add_argument('--ss_doEncrypt', dest="ss_doEncrypt", action="store_true", help="SaveService: doEncrypt? (bool)")
    parser.add_argument('--ss_verbose', dest="ss_verbose", action="store_true", help="SaveService: verbose? (bool)")
    parser.add_argument('--ss_simpleScore', dest="ss_simpleScore", action="store_true", help="SaveService: simpleScore? (bool)")
    parser.add_argument('-ss_scoreboard', dest="ss_scoreboard", help="SaveService: Scoreboard to save to (str)")
    parser.add_argument('-ss_user', dest="ss_user", help="SaveService: User to save to (str)")
    parser.add_argument('-ss_data', dest="ss_data", help="SaveService: Data to save to user specified (JSON)")
    parser.add_argument('-ss_pyPath', dest="ss_pyPath", help="SaveService: PythonPathOverwrite (str)")
    ## [Internal]
    parser.add_argument('-it_inp', dest="it_inp", help="Internal: Input (str)")
    parser.add_argument('-it_linkedFile', dest="it_linkedFile", help="Internal: Linked file (str)")
    parser.add_argument('-it_apiConfPath', dest="it_apiConfPath", help="Internal: APIconf path (str)")
    ## [General]
    parser.add_argument('-json', dest="ot_json", help="Json to pass (str)")
    parser.add_argument('--autoPath', dest="autopath", help="EXPERIMENTAL, DEBUG PURPOSES", action="store_true")
    # Get Inputs
    args = parser.parse_args(sys.argv)
    if args.autopath: os.chdir(f"{parentDir}{os.sep}..")
    # [QuickuseFunctions]
    if args.qu_userData:
        ans =  gamehub_userData(
            encType=args.qu_encType,manager=args.qu_manager,apiKey=args.qu_apiKey,encKey=args.qu_encKey,managerFile=args.qu_managerFile,ignoreManFormat=args.qu_ignoreManFormat,
            scoreboard=args.qu_scoreboard,user=args.qu_user,dictData=json.loads(args.qu_dictData),
            saveUser=args.qu_saveUser,getUser=args.qu_getUser,updateUser=args.qu_updateUser,getAllUsers=args.qu_getAllUsers, doesExist=args.qu_doesExist,mRemove=args.qu_mRemoves,
            doCheckExistance=args.qu_doCheckExistance,autoHandlePingRemoval=args.qu_autoHandlePingRemoval,autoFindGlobalManagerFile=args.qu_autoFindGlobalManagerFile
        )
        print(ans)
    if args.qu_prep:
        ans =  gamehub_singleSavePrep( tempFolder=args.qu_tempFolder,fileName=args.qu_fileName,encrypt=args.qu_encrypt,scoreboard=args.qu_scoreboard,user=args.qu_user,data=json.loads(args.qu_dictData) )
    if args.qu_save:
        ans =  gamehub_singleSave(
        encType=args.qu_encType,manager=args.qu_manager,apiKey=args.qu_apiKey,encKey=args.qu_encKey,managerFile=args.qu_managerFile,ignoreManFormat=args.qu_ignoreManFormat,
        tempFolder=args.qu_tempFolder,fileName=args.qu_fileName, encrypt=args.qu_encrypt,
        doCheckExistance=args.qu_doCheckExistance,autoHandlePingRemoval=args.qu_autoHandlePingRemoval,autoFindGlobalManagerFile=args.qu_autoFindGlobalManagerFile
        )
        print(ans)
    if args.qu_savescore:
        ans =  gamehub_singleSave_score(
        encType=args.qu_encType,manager=args.qu_manager,apiKey=args.qu_apiKey,encKey=args.qu_encKey,managerFile=args.qu_managerFile,ignoreManFormat=args.qu_ignoreManFormat,
        tempFolder=args.qu_tempFolder,fileName=args.qu_fileName, encrypt=args.qu_encrypt,
        doCheckExistance=args.qu_doCheckExistance,autoHandlePingRemoval=args.qu_autoHandlePingRemoval,autoFindGlobalManagerFile=args.qu_autoFindGlobalManagerFile
        )
        print(ans)
    if args.qu_apiconfFunc:
        ans =  apiConfig_gamehub_scoreboardFunc(apiConfPath=args.qu_apiConfPath,scoreboard=args.qu_scoreboard,jsonData=args.qu_dictData, create=args.qu_create,replace=args.qu_replace,remove=args.qu_remove,get=args.qu_get,append=args.qu_append, doesExist=args.qu_doesExist,
                doCheckExistance=args.qu_doCheckExistance,autoHandlePingRemoval=args.qu_autoHandlePingRemoval,autoFindGlobalManagerFile=args.qu_autoFindGlobalManagerFile
               )
        print(ans)
    if args.qu_apiconfFunc_ovmf:
        # imf protcol for services 
        args.qu_dictData = _imfProtocol(str(args.qu_dictData))
        ans =  apiConfig_gamehub_scoreboardFunc(apiConfPath=args.qu_apiConfPath,scoreboard=args.qu_scoreboard,jsonData=args.qu_dictData, create=args.qu_create,replace=args.qu_replace,remove=args.qu_remove,get=args.qu_get,append=args.qu_append, doesExist=args.qu_doesExist, managerOverwrite=args.qu_managerFile,
                doCheckExistance=args.qu_doCheckExistance,autoHandlePingRemoval=args.qu_autoHandlePingRemoval,autoFindGlobalManagerFile=args.qu_autoFindGlobalManagerFile
               )
        print(ans)
    ## [BackupService]
    if args.bs_backupService:
        ans = gamehub_backupService(apiConfPath=args.bs_apiConfPath,scoreboard=args.bs_scoreboard,backupStoreMode=args.bs_backupMode,backupStoreLocation=args.bs_backupLoc,ping=args.bs_ping,backupInterval=args.bs_interval,mode=args.bs_mode,pythonPathOverwrite=args.bs_pythonPathOverwrite,breakFilePath=args.bs_breakFilePath,serviceManagerFile=args.bs_serviceManagerFile,pingMessage=args.bs_pingMessage)
        print(ans)
    if args.bs_backupServiceA20:
        _ping = False
        if args.bs_ping != None:
            _ping = True
        _backupLoc = os.path.join(os.path.abspath(parentDir), f"internal_services{os.sep}backup{os.sep}backups")
        if args.bs_backupLoc != None:
            _backupLoc = args.bs_backupLoc
        ans = gamehub_backupService_auto20Days(apiConfPath=args.bs_apiConfPath, scoreboard=args.bs_scoreboard,ping=_ping,loc=_backupLoc)
        print(ans)
    if args.bs_backupServiceUnshedule:
        ans = gamehub_backupService_quickUnshedule(apiConfPath=args.bs_apiConfPath, scoreboard=args.bs_scoreboard)
        print(ans)
    ## [SaveService]
    if args.ss_function:
        ans =  saveServiceFunction(apiConfPath=args.ss_apiConfPath,linkedFile=args.ss_linkedFile,exitFile=args.ss_exitFile,doEncrypt=args.ss_doEncrypt,verbose=args.ss_verbose,simpleScore=args.ss_simpleScore)
        print(ans)
    if args.ss_prep:
        _str = str(args.ss_data)
        _str = _str.replace("'",'"')
        _jsonData = json.loads(_str)
        ans =  saveServicePrep(linkedFile=args.ss_linkedFile,doEncrypt=args.ss_doEncrypt,scoreboard=args.ss_scoreboard,user=args.ss_user,data=_jsonData)
        print(ans)
    if args.ss_on:
        pyPath = "python3"
        if args.ss_pyPath: pypath = args.ss_pyPath
        ans =  gamehub_saveService_on(ss_pyPath=pyPath,apiConfPath=args.ss_apiConfPath,linkedFile=args.ss_linkedFile,exitFile=args.ss_exitFile,doEncrypt=args.ss_doEncrypt,verbose=args.ss_verbose,simpleScore=args.ss_simpleScore)
        print(ans)
    if args.ss_off:
        ans =  gamehub_saveService_off(exitFile=args.ss_exitFile)
        print(ans)
    ## [Other]
    if args.ot_sort:
        args.ot_json = _imfProtocol(args.ot_json)
        ans = sortScoreboardJson(args.ot_json)
        print(ans)
    ## [Internal]
    if args.it_ep:
        ans =  _ep(args.it_inp)
        print(ans)
    if args.it_linkFexi:
        ans =  _linkFileExist(args.it_linkedFile)
        print(ans)
    if args.it_getApiConf:
        ans = getAPIConfig(args.it_apiConfPath)
        print(ans)