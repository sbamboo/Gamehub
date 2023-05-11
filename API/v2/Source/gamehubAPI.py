import json,os
from libs.importa import fromPath
import ManagerAPI as manAPI

# requireAPI
def requireAPI(apiVid=str(),verFileOverwrite=None):
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

# ManagerAPI passthrough
def registerManager(**kwargs):
    '''
       (Passthrough of ManagerAPI.registerManager)
       Registers a manager, by default in the global manager file. If your custom manager file is wanted give it's path to managerFile.
       managerFile = <str>, Supply managerFile, otherwise will fallback to "os.path.dirname(__file__)\\managers.jsonc"
       name = <str>,        Name of manager to register.
       path = <str>,        Path to the manager that will be registered. (.py files only)
       needKey = <bool>,    Whether or not the manager needs a key. (Encryption is choosen by user, so al cryptolib ones should be available or inform user otherwise)
    '''
    manAPI.registerManager(**kwargs)
def unregisterManager(**kwargs):
    '''
       (Passthrough of ManagerAPI.registerManager)
       Unregisters a manager, by default in the global manager file. If your custom manager file is wanted give it's path to managerFile.
       managerFile = <str>, Supply managerFile, otherwise will fallback to "os.path.dirname(__file__)\\managers.jsonc"
       name = <str>,        Name of manager to unregister.
    '''
    manAPI.unregisterManager(**kwargs)