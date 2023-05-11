import json,os,subprocess
from libs.importa import fromPath
import managerAPI as manAPI

# requireAPI
def gamehub_requireAPI(apiVid=str(),verFileOverwrite=None):
    if verFileOverwrite == None: verFileOverwrite = f"{os.path.dirname(__file__)}\\API.json"
    rawAPIdata = json.loads(open(verFileOverwrite,'r').read())
    matching = False
    newer = False
    older = False
    apiVer = rawAPIdata["Version"]["Vid"]
    if "+" in apiVid:
        apiVid = apiVid.replace("+", "")
        newer = True
    if "-" in apiVid:
        apiVid = apiVid.replace("-", "")
        older = True
    if apiVid < apiVer:
        if newer:
            matching = True
            msg = "Installed API version is correct!"
        else:
            msg = "Installed API version is newer then the required one!"
    elif apiVid > apiVer:
        if older:
            matching = True
            msg = "Installed API version is correct!"
        else:
            msg = "Installed API version is older then the required one!"
    elif apiVid != apiVer:
        msg = "Installed API version does not match the required one!"
    elif apiVid == apiVer:
        msg = "Installed API version is correct!"
        matching = True
    return matching,msg


# ScoreboardConnector
class scoreboardConnector():
    # Functions/Code for dynamic imports
    @staticmethod
    def GetDynamicImports(managersFile=str()):
        managersRaw = open(managersFile,'r').read()
        managers_dict = json.loads(managersRaw)
        managers = dict()
        for manager in list(managers_dict.keys()):
            managers[manager] = {"module":fromPath(managers_dict[manager]["path"]),"needKey":managers_dict[manager]["needKey"]}
        return managers
    # Initator
    def __init__(self, encryptionType=None, storageType=None, key=None, kryptographyKey=None, managersFile=None, ignoreManagerFormat=False):
        '''
        encryptionType: "aes" or "legacy" or "None"
        storegeType: "pantry"
        key should only be supplied if the storageType needs it
        kryptographyKey should only be supplied if encryptionType needs it
        managersFile is if you want to load dynamicManagers
        ignoreManagerFormat is used if you want to ignore a managers format
        '''
        # Variables
        self.parentPath = os.path.dirname(__file__)
        self.managerFormat = [1, "https://sbamboo.github.io/websa/Gamehub/API/v2/docs/managers/format1.html"]
        # Manager file
        if managersFile == "GLOBAL":
            managersFile = f"{self.parentPath}\\managers.jsonc"
        # Keyfile
        if "Keyfile:" in key:
            key = key.replace("Keyfile:","")
            key = open(key, 'r').read()
        # CryptoType
        if encryptionType == None: encryptionType = "None"
        if encryptionType == "legacy":
            import libs.libcrypto.legacy as encryptor
        elif encryptionType == "aes":
            import libs.libcrypto.aes as encryptor
        self.needKey = False
        if encryptionType != "None":
            self.GenerateKey = encryptor.GenerateKey
            self.encdec = encryptor.encdec
            self.encdec_dict = encryptor.encdec_dict
        # Dynamic storageTypes
        if managersFile != None and managersFile != "None":
            dynamicManagers = self.GetDynamicImports(managersFile)
            if storageType in list(dynamicManagers.keys()):
                # check format
                if ignoreManagerFormat == False:
                    if int(dynamicManagers[storageType]["module"].managerFormat[0]) != int(self.managerFormat[0]):
                        raise Exception(f"Manager for {storageType} is not supported on this version of gamehubAPI, managerFormat:{dynamicManagers[storageType]['module'].managerFormat[0]} whilst apiFormat:{self.managerFormat[0]}. See {self.managerFormat[1]}")
                self.storageManager = dynamicManagers[storageType]["module"].Manager()
                self.needKey = bool(dynamicManagers[storageType]["needKey"])
            else:
                raise Exception(f"Storage type '{storageType}' not found!")
        # handle keys
        if self.needKey == True:
            if encryptionType != "None":
                self.kryptokey = self.GenerateKey(kryptographyKey)
                self.key = self.encdec(key=self.kryptokey,inputs=key,mode="dec")
            else:
                self.key = key
        else:
            self.key = None
    # Method functions
    def create(self,scoreboard=str(),jsonDict=None):
        return self.storageManager.create(self.key,scoreboard,jsonDict)
    def remove(self,scoreboard=str()):
        return self.storageManager.remove(self.key,scoreboard)
    def get(self,scoreboard=str()):
        return self.storageManager.get(self.key,scoreboard)
    def append(self,scoreboard=str(),jsonDict=dict()):
        return self.storageManager.append(self.key,scoreboard,jsonDict)
    def doesExist(self,scoreboard=str()) -> bool:
        return self.storageManager.doesExist(self.key,scoreboard)
    # Mapped methods
    def EncDec(self,string,mode):
        return self.encdec(key=self.kryptokey,inputs=string,mode=mode)
    def EncDecDict(self,_dict,mode):
        return self.encdec_dict(key=self.kryptokey,dictionary=_dict,mode=mode)

# Function to get TOS
def gamehub_getTOS(net=bool()):
    if net == True:
        import requests
        r = requests.get("https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/tos.txt", allow_redirects=True)
        return r.content
    else:
        return open("..\\tos.txt",'r').read()

# Main function for handling a scoreboard from a function
def gamehub_scoreboardFunc(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        scoreboard=str(),jsonData=str(),
        create=False,remove=False,get=False,append=False, doesExist=False
    ):
    # Create scoreboardConnector
    scoreboard = scoreboardConnector(encryptionType=encType, storageType=manager, key=apiKey, kryptographyKey=encKey, managersFile=managerFile, ignoreManagerFormat=ignoreManFormat)
    # Actions
    if create == True: scoreboard.create(scoreboard=scoreboard,jsonDict=jsonData)
    elif remove == True: scoreboard.remove(scoreboard=scoreboard)
    elif get == True: scoreboard.get(scoreboard=scoreboard)
    elif append == True: scoreboard.append(scoreboard=scoreboard,jsonDict=jsonData)
    elif doesExist == True: scoreboard.doesExist(scoreboard=scoreboard)

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