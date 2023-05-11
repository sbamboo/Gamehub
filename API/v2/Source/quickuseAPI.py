from tempfileAPI import saveDict,loadDict
from gamehubAPI import gamehub_userData
import getpass

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
        scoreboard=_dict["scoreboard"], user=_dict["user"], dictData={user:_dict["data"]}, updateUser=True
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
            scoreboard=_dict["scoreboard"], user=_dict["user"], dictData={user:_dict["data"]}, updateUser=True
        )

# Functions to work with the saveService (Files should be saved with gamehub_singleSavePrep() without encryption)
def gamehub_saveService_on(dataLocation=str(),dataFile=str(),doDebug=bool(),scoreboard=str()):
    command = ["python3", f"{os.path.dirname(__file__)}\\_internal_saveService.py", "-loc", dataLocation, "-datafile", dataFile, "-scoreboard", scoreboard]
    if dodebug == False:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.Popen(command, startupinfo=startupinfo if not dodebug else None)

def gamehub_saveService_off():
    fp = f"{os.path.dirname(__file__)}\\saveService_end.state"
    if os.path.exists(fp): os.remove(fp)
    open(fp,'w').write("1")