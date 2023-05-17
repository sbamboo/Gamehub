from gamehubAPI import saveDict,loadDict,scoreboardConnector,gamehub_scoreboardFunc
from libs.libfilesys import filesys as fs
import base64,json,os,subprocess;exec(base64.b64decode("aW1wb3J0IGdldHBhc3MNCmltcG9ydCBzb2NrZXQNCmltcG9ydCBkYXRldGltZQ0KaW1wb3J0IGhhc2hsaWINCg0KZGVmIGVudHJvcHlHZW5lcmF0b3IoKSAtPiBzdHI6DQogICAgaG9zdCA9IHNvY2tldC5nZXRob3N0bmFtZSgpDQogICAgZW50cm9weSA9IGhhc2hsaWIuc2hhMjU2KGYie2dldHBhc3MuZ2V0dXNlcigpfS17aG9zdH0te3NvY2tldC5nZXRob3N0YnluYW1lKGhvc3QpfS17ZGF0ZXRpbWUuZGF0ZS50b2RheSgpLnN0cmZ0aW1lKCcleS0lbS0lZCcpfS1HYW1laHViRW50cm9weVZhbHVlX1RvQnJlYWtUaGlzVmFsdWVPclVzZUl0QW55d2hlcmVJdFdhc05vdE9yaWdpbmFseVVzZWRJc0FCcmVha2FnZU9mVGhlR2FtZWh1YkxpY2Vuc2VBbmRUT1MiLmVuY29kZSgpKS5oZXhkaWdlc3QoKQ0KICAgIGhvc3QgPSBOb25lDQogICAgcmV0dXJuIGVudHJvcHk=").decode("utf-8"))

# Function to handle userData
def gamehub_userData(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        scoreboard=str(),user=None,dictData=None,
        saveUser=False,getUser=False,updateUser=False,getAllUsers=False, doesExist=False,mRemove=False,
    ):
    # Create scoreboardConnector
    scoreboard = scoreboardConnector(encryptionType=encType, storageType=manager, key=apiKey, kryptographyKey=encKey, managersFile=managerFile, ignoreManagerFormat=ignoreManFormat)
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
        scoreboard.create(scoreboard=scoreboard,jsonDict=_dict)
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
    _json = json.dump(_data)
    # Save settings data
    saveDict(securityLevel=securityLevel,encType=encType,encKey=encKey,tempFolder=tempFolder,fileName=fileName,jsonStr=_json)
    encKey = None
# Function to load and upload an existing file
def gamehub_singleSave(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        tempFolder=str(),fileName=str(), encrypt=True
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
    _dict = loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
    _encKey = None
    # Update data
    _jsonData = json.loads( {_dict["user"] : _dict["data"]} )
    gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], jsonData=_jsonData, append=True)
# Function to load and upload an existing file (SCORE)
def gamehub_singleSave_score(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        tempFolder=str(),fileName=str(), encrypt=True
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
    _dict = loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
    _encKey = None
    user = _dict["user"]
    # Get Current Data
    current = gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], get=True)
    # Check
    if int(current[user]["score"]) < int(_dict["data"]["score"]):
        _jsonData = json.loads( {_dict["user"] : _dict["data"]} )
    gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], jsonData=_jsonData, append=True)

# Function to prep a file for the saveService
def saveServicePrep(linkedFile=str(),doEncrypt=True, scoreboard=str(),user=str(),data=dict()):
    _path = os.path.dirname(linkedFile)
    _file = os.path.basename(linkedFile)
    gamehub_singleSavePrep(tempFolder=_path,fileName=_file,encrypt=doEncrypt,scoreboard=scoreboard,user=user,data=data)

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
    apiConf = json.loads(open(apiConfPath,'r').read())
    previousContent = str()
    # Init scoreboard connector
    conn = scoreboardConnector(encryptionType=apiConf["encryptionType"], storageType=apiConf["storageType"], key=apiConf["apiKey"], kryptographyKey=apiConf["encKey"], managersFile=apiConf["managersFile"], ignoreManagerFormat=apiConf["ignoreManagerFormat"])
    # Prep dict settings
    securityLevel,_encType,_encKey = 0,None,None
    if doEncrypt == True:
        securityLevel,_encType,_encKey = 2,"aes",entropyGenerator()
    # Look for first file, as a startup
    if verbose: print(f"\033[33m[SaveService] \033[90mStarted listener on {linkedFile}\033[0m")
    if verbose: print("\033[33m[SaveService] \033[90mWaiting for tmp file...\033[0m")
    while fs.doesExist(linkedFile) == False: _ = ""
    # Loop through the file and listen for changes
    if verbose: print("\033[33m[SaveService] \033[90mContinuing!\033[0m")
    while True:
        # Check for exit file
        if fs.doesExist(exitFile) == True:
            fs.deleteFile(exitFile)
            if verbose: print("\033[33m[SaveService] \033[90mStopped!\033[0m")
            break
        # Listen for content
        if fs.doesExist(linkedFile) == True:
            # Get current content
            tempFolder = os.path.dirname(linkedFile)
            fileName = os.path.basename(linkedFile)
            content = loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
            user = content["user"]
            scoreboard = content["scoreboard"]
            data = content["data"]
            # If simpleScore prep data
            if simpleScore == True:
                currentScore = conn(scoreboard)[user]["score"]
                newScore = data["score"]
                if int(newScore) > int(currentScore):
                    conn(scoreboard,{user:data})
            # Normal upload
            else:
                conn(scoreboard,{user:data})
                
# Functions to work with the saveService (Files should be saved with saveServicePrep() with encryption by default)
def gamehub_saveService_on(apiConfPath=str(),linkedFile=str(),exitFile=str(),doEncrypt=True,verbose=True,simpleScore=False,hidden=True):
    # General setup of enviroment
    if os.path.exists(exitFile): os.remove(exitFile)
    # Setup command
    command = ["python3", f"{os.path.dirname(__file__)}\\internal_saveService\\service.py", "-apiConfPath", apiConfPath, "-linkedFile", linkedFile, "-exitFile", exitFile]
    if doEncrypt == True: command.append("--doEncrypt")
    if verbose == True: command.append("--verbose")
    if simpleScore == True: command.append("--simpleScore")
    # Hidden window?
    if hidden == False:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    # Start service
    subprocess.Popen(command, startupinfo=startupinfo if not hidden else None)

def gamehub_saveService_off(exitFile=str()):
    if os.path.exists(exitFile): os.remove(exitFile)
    open(exitFile,'w').write("1")