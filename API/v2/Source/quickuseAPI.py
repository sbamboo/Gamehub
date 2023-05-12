from gamehubAPI import saveDict,loadDict,scoreboardConnector
import getpass,json,subprocess,os

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
        # remove scoreboard
        scoreboard.remove(scoreboard=scoreboard)
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
        tempFolder=str(),fileName=str(), encrypt=True,
        scoreboard=str(),user=str(),data=dict()
    ):
    if encrypt == True:
        securityLevel = 2
        encType = "aes"
        encKey = f"GAMEHUB_SINGLESAVE_id@8w392A_{getpass.getuser()}"
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
        _encKey = f"GAMEHUB_SINGLESAVE_id@8w392A_{getpass.getuser()}"
    else:
        securityLevel = 0
        _encType = None
        _encKey = None
    # Load data
    _dict = loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
    # Update data
    gamehub_userData(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,
        scoreboard=_dict["scoreboard"], user=_dict["user"], dictData=_dict["data"], updateUser=True
    )
# Function to load and upload an existing file (SCORE)
def gamehub_singleSave_score(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        tempFolder=str(),fileName=str(), encrypt=True
    ):
    if encrypt == True:
        securityLevel = 2
        _encType = "aes"
        _encKey = f"GAMEHUB_SINGLESAVE_id@8w392A_{getpass.getuser()}"
    else:
        securityLevel = 0
        _encType = None
        _encKey = None
    # Load data
    _dict = loadDict(securityLevel=securityLevel,encType=_encType,encKey=_encKey, tempFolder=tempFolder, fileName=fileName)
    # Get current data
    current = gamehub_userData(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,
        scoreboard=_dict["scoreboard"], user=_dict["user"], getUser=True
    )
    # Check
    if int(current["score"]) < int(_dict["data"]["score"]):
        gamehub_userData(encType=encType,manager=manager,apiKey=apiKey,encKey=encKey,managerFile=managerFile,ignoreManFormat=ignoreManFormat,
            scoreboard=_dict["scoreboard"], user=_dict["user"], dictData=_dict["data"], updateUser=True
        )

# Functions to work with the saveService (Files should be saved with gamehub_singleSavePrep() without encryption)
def gamehub_saveService_on(dataLocation=str(),dataFile=str(),doDebug=bool(),scoreboard=str()):
    command = ["python3", f"{os.path.dirname(__file__)}\\internal_saveService\service.py", "-loc", dataLocation, "-datafile", dataFile, "-scoreboard", scoreboard]
    if doDebug == False:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(command, startupinfo=startupinfo if not doDebug else None)

def gamehub_saveService_off():
    fp = f"{os.path.dirname(__file__)}\\internal_saveService\\exit.state"
    if os.path.exists(fp): os.remove(fp)
    open(fp,'w').write("1")