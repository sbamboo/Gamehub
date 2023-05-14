from gamehubAPI import saveDict,loadDict,scoreboardConnector,gamehub_scoreboardFunc
import getpass,json,subprocess,os
import base64;exec(base64.b64decode("aW1wb3J0IGdldHBhc3MNCmltcG9ydCBzb2NrZXQNCmltcG9ydCBkYXRldGltZQ0KaW1wb3J0IGhhc2hsaWINCg0KZGVmIGVudHJvcHlHZW5lcmF0b3IoKSAtPiBzdHI6DQogICAgdXNlciA9IGdldHBhc3MuZ2V0dXNlcigpDQogICAgaG9zdCA9IHNvY2tldC5nZXRob3N0bmFtZSgpDQogICAgZGF0ZSA9IGRhdGV0aW1lLmRhdGUudG9kYXkoKS5zdHJmdGltZSgnJXktJW0tJWQnKQ0KICAgIGVudHJvcHlfc3RyID0gZid7dXNlcn0te2hvc3R9LXtkYXRlfScNCiAgICBlbnRyb3B5ID0gaGFzaGxpYi5zaGEyNTYoZW50cm9weV9zdHIuZW5jb2RlKCkpLmhleGRpZ2VzdCgpDQogICAgcmV0dXJuIGVudHJvcHk=").decode("utf-8"))

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
    # Update data
    scoreboard = _dict["scoreboard"]
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
    scoreboard = _dict["scoreboard"]
    user = _dict["user"]
    # Get Current Data
    current = gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], get=True)
    # Check
    if int(current[user]["score"]) < int(_dict["data"]["score"]):
        _jsonData = json.loads( {_dict["user"] : _dict["data"]} )
    gamehub_scoreboardFunc(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,_scoreboard=_dict["scoreboard"], jsonData=_jsonData, append=True)

# Functions to work with the saveService (Files should be saved with gamehub_singleSavePrep() without encryption)
def gamehub_saveService_on(dataLocation=str(),dataFile=str(),doDebug=bool(),scoreboard=str()):
    command = ["python3", f"{os.path.dirname(__file__)}\\internal_saveService\\service.py", "-loc", dataLocation, "-datafile", dataFile, "-scoreboard", scoreboard]
    if doDebug == False:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(command, startupinfo=startupinfo if not doDebug else None)

def gamehub_saveService_off():
    fp = f"{os.path.dirname(__file__)}\\internal_saveService\\exit.state"
    if os.path.exists(fp): os.remove(fp)
    open(fp,'w').write("1")