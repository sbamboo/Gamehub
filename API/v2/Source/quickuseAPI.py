from gamehubAPI import saveDict,loadDict,scoreboardConnector,gamehub_scoreboardFunc
from libs.libfilesys import filesys as fs
from libs.libRSA import decrypt_string
import base64,json,os,subprocess,getpass,socket
exec(base64.b64decode("aW1wb3J0IGdldHBhc3MKaW1wb3J0IHNvY2tldAppbXBvcnQgZGF0ZXRpbWUKaW1wb3J0IGhhc2hsaWIKCmRlZiBlbnRyb3B5R2VuZXJhdG9yKCkgLT4gc3RyOgogICAgdXNlciA9IGdldHBhc3MuZ2V0dXNlcigpCiAgICBob3N0ID0gc29ja2V0LmdldGhvc3RuYW1lKCkKICAgIGlwX2FkZHJlc3MgPSBzb2NrZXQuZ2V0aG9zdGJ5bmFtZShob3N0KQogICAgZGF0ZSA9IGRhdGV0aW1lLmRhdGUudG9kYXkoKS5zdHJmdGltZSgnJXktJW0tJWQnKQogICAgZW50cm9weV9zdHIgPSBmJ3t1c2VyfS17aG9zdH0te2lwX2FkZHJlc3N9LXtkYXRlfScKICAgIGVudHJvcHkgPSBoYXNobGliLnNoYTI1NihlbnRyb3B5X3N0ci5lbmNvZGUoKSkuaGV4ZGlnZXN0KCkKICAgIHJldHVybiBlbnRyb3B5CgpkZWYgZ2V0U2FmZUNvbmZpZ0tleSgpIC0+IHN0cjoKICAgIHJldHVybiAnJyctLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS0KTUlJRXZRSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2N3Z2dTakFnRUFBb0lCQVFDbHErV0cwRVhsM3I5Twp1MDNnQmx5ejk5dUJScXExR1Z0R01PL3M3c2ZpSjZPeVU1UkVURmJtWDlZMkxpZVdiNFVybU5SNlBRVkJRNEtWCnp5UDRudVNxL3MvSFFwZHdmZ2ZsdU1xL0t2dW1LOE5lWEF5N2ZpSm9SbTRzc0NESTd4NWIvVUxhYmYwSk1OTGwKN2tzQ1FBMVFPNmJDcFVLMDE5VDg1VFdzcktwdmNGeWc2WWFOajgvaTFUSXB3TnVqR1ZzeW1nYUNPUEtjdmF5OQpxR1FMcXordFQydEdMclA0UElDTjJqNHpmWlZXLytkR2dFOFgzWHN4WG5PVjF6RFFYZjI2dlRyL2kxTHFHTzZEClcza2FwYzdXS2ZuV0lJQW8ySCtGb3pWMUFoY1RtQVJDTjI1d25nL2U2SW5udy9WNzd0L1JHWkRKeFdMSmhnblAKdnJQaWcxR2JBZ01CQUFFQ2dnRUFTN21JQnJpQkVvSmZlRG0xN1QyTE52bUdQQTlVYk1XanlqQUpJb2U4Rmx1ZQovNTRqU1pxSkovRExSV1dRVTdzeXFBeEpwbnZvd0gxK25VSWFnNFFCS2tXaExFZDhWLzlMVmMzQzRtRmZ1QU1OCjREMzcxZUZnRWNDTGtHS0xBYjBHWis2WmxhU3JnWDF2RUlqOGdSRk01SXozZXNXMStWb2o4TnBGeitEMllFdkQKWFpEeUNIRHAyOXhObmV3Y2RzVjhWK3VKbXo0OVAwUU1BWXRxK011T0Q3R21oN2I4WHQxY1RlazlIWXFmVkVQMgpZVUtubWtqejRvemtUU0RhK2V5UHdmVFZVYytmQzdmWVNpK2srdWpObzFOU0tOWTcwY2w3c01iaUhEUzBGeTVzCnBYbTVjV2xMemFkQjJYejVjN2Z0SnRONUhaQTBsSEliMUJUb3NMbXNpUUtCZ1FEQVNFVGlVbGJ2eDM2MDBUR3kKd2FwUyszd3llSUtXYUhJQ1E1QmMrZDNxNjNvS3orMVF5a093RllsVFBRTlVPOUlGS3pXWTUvaENSWVdhQWF4dgpIQnhPWitsbUs5VXlwenZyc1M2OFhmQVVNL1Q3Rlk0NitnWTlCSGVFeTdZVW5xeUxMT1VzaytKTmRwanF1SWlJCk9jblI5eDNMTjduRE9NSHJNT3J0WldlbE13S0JnUURja2l3V0hjNm9wU1pBZXJVR0ZRNXJJS3ZqYkRHUVZidk0KMFh0UzFSWXpLam00M2daMEVuRjVXR25ZcDZTU0xMRVk4SzkzVFVKTzdWN0RUSldVdFAzQVJqODQ4VGlubkNoQgpHWXNGQ2tyYlEvVXJYRzRkY1pzV1FXRGJGQ1FHU1V2c3VvODg3eTZtYnJxQzBYVlJacWlhbkZUZFNpVWo5WUFsCmhpTERoOWZSK1FLQmdDTWFEbGt5cHVSSEN2NS9ZZzg4QTVmNmlRVzlzams2Ly9VaDJHemd3SDV1Vm0wNjRCdnIKa01mSVpyVm5ZZ0F5bTNpT0ZzNi9LamNPOGdEWFpWOHpSb2VadUtZS1FuVm95aXVRd1BOcVFyV3RkbitQdzlOSQphWE1pS1o5NGdOanF6cHpwcVR5bUVwNEpsSWprL3llL1JQU3JwQ2pCRjR4b0JCNm5ZM3ZMRTB5NUFvR0JBSUdnCk9kNkpoL0VlbFh0aFljK0FRbWY4M0dlY0p3aXZDZDVWNGdjTkNhM3FDK0EwUTFDbG9pQnhNRXRPUW01UmE0YS8KdEM4RnJZbGJBTXovemd5RnpYYlpFY0N5S3R4OTdqNUw5Nkp2cVF4eFJMMUY1Y1RTQmhXdk9HK254NEFXUlZPTApWREM0VkE4bGxlRFpuZnZIdkNDWTdWcmJmelpCeWh6RFZ0ellrYUpwQW9HQUQzYTJFOUFVUjRyQjJzNjF6NHFMCjZaM05WTzVZWkZHVTFsY29pbXl0bGJQMVJjcWVsUnpWTWFBWmdFNndpUFhLc1JoUWtOMm9GZGswSnpOZWhoK2YKbS9uMjIyVEdPSkY3MENrNU8rWklyeERTWnlJUldnSmlRaVZ0THpGZDdFbFRBb0JqeTd3bUVkWndWamgrVUx1bgpMWVZ5blY0RnJtbUVUa0VBdzU0ZUhldz0KLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLScnJw==").decode("utf-8"))

parentDir = os.path.dirname(__file__)

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
    return json.loads(content)

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
    apiConf = json.loads( getAPIConfig(apiConfPath) )
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