# Imports & Setup
import json,os,uuid,tempfile,argparse,sys,importlib.util,platform
parentPath = os.path.dirname(__file__)

# Functions
def fromPath(path):
    path = path.replace("\\",os.sep)
    spec = importlib.util.spec_from_file_location("module", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Dynamic imports
libhasher = fromPath(f"{parentPath}{os.sep}libs{os.sep}libhasher.py")
hashFile = libhasher.hashFile
hashString = libhasher.hashString
libfilesys = fromPath(f"{parentPath}{os.sep}libs{os.sep}libfilesys.py")
fs = libfilesys.filesys

# ========================================================[require API]========================================================
def requireAPI(apiVid=str(),verFileOverwrite=None):
    if verFileOverwrite == None: verFileOverwrite = f"{os.path.dirname(__file__)}{os.sep}API.json"
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

# ========================================================[Manager API]========================================================
def registerManager(managerFile=f"{parentPath}{os.sep}managers.jsonc",name=str(),path=str(),needKey=bool()):
    '''
       Registers a manager, by default in the global manager file. If your custom manager file is wanted give it's path to managerFile.
       managerFile = <str>, Supply managerFile, otherwise will fallback to "os.path.dirname(__file__){os.sep}managers.jsonc"
       name = <str>,        Name of manager to register.
       path = <str>,        Path to the manager that will be registered. (.py files only)
       needKey = <bool>,    Whether or not the manager needs a key. (Encryption is choosen by user, so al cryptolib ones should be available or inform user otherwise)
    '''
    # No manager file
    if bool(os.path.exists(managerFile)) == False:
        raise Exception(f"ManagerFile {managerFile} could not be found!")
    # No manager
    if bool(os.path.exists(path)) == False:
        raise Exception(f"Path to manager {path}, could not be found!")
    # Get old list
    oldList = json.loads(open(managerFile,'r').read())
    # Check for duplicates
    if name in list(oldList.keys()):
        raise Exception(f"Manager '{name}' is already registered!")
    # add new manager
    oldList[name] = {"path":path, "needKey":str(needKey)}
    # replace file
    json.dump(oldList, open(managerFile,'w'))

def unregisterManager(managerFile=f"{parentPath}{os.sep}managers.jsonc",name=str()):
    '''
       Unregisters a manager, by default in the global manager file. If your custom manager file is wanted give it's path to managerFile.
       managerFile = <str>, Supply managerFile, otherwise will fallback to "os.path.dirname(__file__){os.sep}managers.jsonc"
       name = <str>,        Name of manager to unregister.
    '''
    # No manager file
    if bool(os.path.exists(managerFile)) == False:
        raise Exception(f"ManagerFile {managerFile} could not be found!")
    # Get old list
    oldList = json.loads(open(managerFile,'r').read())
    # Check for duplicates
    if name not in list(oldList.keys()):
        raise Exception(f"Manager '{name}' is not registered!")
    # remove manager
    oldList.pop(name)
    # replace file
    json.dump(oldList, open(managerFile,'w'))

# ========================================================[tempfile API]========================================================
# Functions to handle tempFiles
def createTempDir() -> str:
    """
    Creates a temporary folder with a random name and returns the path to it.
    """
    temp_folder = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
    os.mkdir(temp_folder)
    return temp_folder

def deleteTempDir(tempFolder=str()):
    fs.deleteDirNE(tempFolder)

def cleanFolder(tempFolder=str()):
    for file in os.listdir(tempFolder):
        fs.deleteFile(os.path.join(tempFolder,file))

# Function to save a dictionary to a tempFile
def saveDict(securityLevel=int(),encType=None,encKey=None,hashType=None, tempFolder=str(), fileName=str(), jsonStr=str()) -> str:
    # Import encryption lib
    if encType == "legacy":
        crypto = fromPath(f"{parentPath}{os.sep}libs{os.sep}libcrypto{os.sep}legacy.py")
        encdec = crypto.encdec
        GenerateKey = crypto.GenerateKey
    elif encType == "aes":
        crypto = fromPath(f"{parentPath}{os.sep}libs{os.sep}libcrypto{os.sep}aes.py")
        encdec = crypto.encdec
        GenerateKey = crypto.GenerateKey
    # Get secure fileName
    fileId = hashString(message=fileName, hashType="sha256")
    toSave = jsonStr
    # encrypt
    isEnc = False
    if int(securityLevel) == 2 or int(securityLevel) == 3:
        isEnc = True
        encKey = GenerateKey(encKey)
        toSave = encdec(key=encKey,inputs=toSave,mode="enc")
    # Should hash
    isHashed = False
    if int(securityLevel) == 1 or int(securityLevel) == 3:
        isHashed = True
    # Save file
    filePath = os.path.join(tempFolder, f"{fileId}.ghs") # ghs = GamehubSync File
    fs.writeToFile(inputs=toSave,filepath=filePath,autocreate=True)
    # Return file
    if isHashed == True:
        return str(hashFile(filePath, hashType))

# Function to load a dictionary from a tempFile
def loadDict(securityLevel=int(),encType=None,encKey=None,hashType=None, tempFolder=str(), fileName=str(), filehash=None) -> dict:
    # Import encryption lib
    if encType == "legacy":
        crypto = fromPath(f"{parentPath}{os.sep}libs{os.sep}libcrypto{os.sep}legacy.py")
        encdec = crypto.encdec
        GenerateKey = crypto.GenerateKey
    elif encType == "aes":
        crypto = fromPath(f"{parentPath}{os.sep}libs{os.sep}libcrypto{os.sep}aes.py")
        encdec = crypto.encdec
        GenerateKey = crypto.GenerateKey
    # encrypt
    isEnc = False
    if int(securityLevel) == 2 or int(securityLevel) == 3:
        encKey = GenerateKey(encKey)
        isEnc = True
    # Should hash
    isHashed = False
    if int(securityLevel) == 1 or int(securityLevel) == 3:
        isHashed = True
    # Get secure fileName
    fileId = hashString(message=fileName, hashType="sha256")
    # Filepath
    filePath = os.path.join(tempFolder, f"{fileId}.ghs") # ghs = GamehubSync File
    # Match hash
    if isHashed == True:
        fileHash = hashFile(filePath, hashType)
        if str(fileHash) != filehash:
            raise Exception("Hash of file didn't match, loading aborted! (Use the 'createTempDir' to remove broken files)")
    # Get content
    toGive = fs.readFromFile(filePath)
    # Decrypt content
    if isEnc == True:
        toGive = encdec(key=encKey,inputs=toGive,mode="dec")
    # Remove file
    fs.deleteFile(filePath)
    # Convert to dictionary
    try:
        return json.loads(toGive)
    except: raise Exception("Failed to load Json, probably wrong encKey")

# ========================================================[Main GamehubAPI]========================================================
# Function for formatVersion compatCheck
def formatIsCompat(hostFormat=list,manFormat=list) -> bool:
    compat = False
    # Get how check
    if len(hostFormat) > 2 and len(manFormat) > 2:
        hostSups = hostFormat[2]
        manSups = manFormat[2]
    elif len(hostFormat) > 2 and len(manFormat) < 3:
        hostSups = hostFormat[2]
        manSups = []
    elif len(hostFormat) < 3 and len(manFormat) > 2:
        hostSups = []
        manSups = manFormat[2]
    elif len(hostFormat) < 3 and len(manFormat) < 3:
        hostSups = []
        manSups = []
    # CHECK
    hostVer = int(hostFormat[0])
    manVer = int(manFormat[0])
    if hostVer == manVer:
        compat = True
    elif hostVer in manSups:
        compat = True
    elif manVer in hostSups:
        compat = True
    return compat

# ScoreboardConnector
class scoreboardConnector():
    # Functions/Code for dynamic imports
    @staticmethod
    def GetDynamicImports(managersFile=str(),rawData=None):
        if rawData != None:
            if isinstance(rawData, dict) != True: raise TypeError("If rawData is defined it must be of type dict!")
            managers_dict = rawData
        else:
            managersRaw = open(managersFile,'r').read()
            managers_dict = json.loads(managersRaw)
        managers = dict()
        for manager in list(managers_dict.keys()):
            managers[manager] = {"module":fromPath(managers_dict[manager]["path"]),"needKey":managers_dict[manager]["needKey"]}
        return managers
    # Initator
    def __init__(self, encryptionType=None, storageType=None, key=None, kryptographyKey=None, managersFile=None, ignoreManagerFormat=False, doCheckExistance=None, autoHandlePingRemoval=True, autoFindGlobalManagerFile=True):
        '''
        encryptionType: "aes" or "legacy" or "None"
        storegeType: "pantry"
        key should only be supplied if the storageType needs it
        kryptographyKey should only be supplied if encryptionType needs it
        managersFile is if you want to load dynamicManagers, if not use 'GLOBAL'
        ignoreManagerFormat is used if you want to ignore a managers format
        doCheckExistance if set to True, wont check scoreboard existance (Less requests sent but less safe) NOTE WILL GET SENT EVEN TO UNSUPPORTING MANAGER, SO DONT SET TO TRUE IF YOUR MANAGER DOESN'T SUPPORT IT
        autoHandlePingRemoval: if set to true, runs the output data through a filter removing any BackupService-Ping data, this to ensure compatability.

        '''
        # Variables
        self.parentPath = os.path.dirname(__file__)
        self.managerFormat = [3, "https://sbamboo.github.io/websa/docview/?markdown=https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/docs/managers/format3.md&css=https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/docs/managers/docs.css&json=https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/docs/docview_files.json",[2]]
        self.doCheckExistance = doCheckExistance
        self.autoHandlePingRemoval = autoHandlePingRemoval
        self.autoFindGlobalManagerFile = autoFindGlobalManagerFile
        # Manager file
        if managersFile == "GLOBAL":
            managersFile = f"{self.parentPath}{os.sep}managers.jsonc"
        # Keyfile
        if "Keyfile:" in key:
            key = key.replace("Keyfile:","")
            key = open(key, 'r').read()
        # CryptoType
        if encryptionType == None: encryptionType = "None"
        if encryptionType == "legacy":
            encryptor = fromPath(f"{parentPath}{os.sep}libs{os.sep}libcrypto{os.sep}legacy.py")
        elif encryptionType == "aes":
            encryptor = fromPath(f"{parentPath}{os.sep}libs{os.sep}libcrypto{os.sep}aes.py")
        self.needKey = False
        if encryptionType != "None" and encryptionType != None:
            self.GenerateKey = encryptor.GenerateKey
            self.encdec = encryptor.encdec
            self.encdec_dict = encryptor.encdec_dict
        # Dynamic storageTypes
        if managersFile != None and managersFile != "None":
            # Autofind global manager file
            if self.autoFindGlobalManagerFile == True:
                # get content
                content_json = open(managersFile,'r').read()
                content = json.loads(content_json)
                # dynamicate
                for _key,value in content.items():
                    _path = value["path"]
                    _suffix = f"managers" + _path.split("managers")[-1]
                    _prefix = os.path.abspath(os.path.abspath(parentPath))
                    _newpath = f"{_prefix}{os.sep}{_suffix}"
                    content[_key]["path"] = _newpath
                # Load
                dynamicManagers = self.GetDynamicImports(managersFile,rawData=content)
            else:
                dynamicManagers = self.GetDynamicImports(managersFile)
            if storageType in list(dynamicManagers.keys()):
                # check format
                if ignoreManagerFormat == False:
                    if formatIsCompat(hostFormat=self.managerFormat, manFormat=dynamicManagers[storageType]["module"].managerFormat) == False:
                        raise Exception(f"Manager for {storageType} is not supported on this version of gamehubAPI, managerFormat:{dynamicManagers[storageType]['module'].managerFormat[0]} whilst apiFormat:{self.managerFormat[0]}. See {self.managerFormat[1]}")
                if doCheckExistance == None:
                    self.storageManager = dynamicManagers[storageType]["module"].Manager()
                else:
                    self.storageManager = dynamicManagers[storageType]["module"].Manager(doCheckExistance)
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
    # RemovePing
    def _filterPing(self,jsonDict=None):
        if jsonDict != None and type(jsonDict) == dict and self.autoHandlePingRemoval == True:
            if jsonDict.get("GamehubBackupServicePing") != None:
                jsonDict.pop("GamehubBackupServicePing")
        return jsonDict
    # Method functions
    def create(self,scoreboard=str(),jsonDict=None,doCheck=None):
        if doCheck == None:
            returnData = self.storageManager.create(self.key,scoreboard,jsonDict)
        else:
            returnData = self.storageManager.create(self.key,scoreboard,jsonDict,doCheck=doCheck)
        # Return
        return self._filterPing(returnData)
    def replace(self,scoreboard=str(),jsonDict=None,doCheck=None):
        if doCheck == None:
            returnData = self.storageManager.replace(self.key,scoreboard,jsonDict)
        else:
            returnData = self.storageManager.replace(self.key,scoreboard,jsonDict,doCheck=doCheck)
        # Return
        return self._filterPing(returnData)
    def remove(self,scoreboard=str(),doCheck=None):
        if doCheck == None:
            returnData = self.storageManager.remove(self.key,scoreboard)
        else:
            returnData = self.storageManager.remove(self.key,scoreboard,doCheck=doCheck)
        # Return
        return self._filterPing(returnData)
    def get(self,scoreboard=str()):
        returnData = self.storageManager.get(self.key,scoreboard)
        # Return
        return self._filterPing(returnData)
    def append(self,scoreboard=str(),jsonDict=dict()):
        returnData = self.storageManager.append(self.key,scoreboard,jsonDict)
        # Return
        return self._filterPing(returnData)
    def doesExist(self,scoreboard=str()) -> bool:
        returnData = self.storageManager.doesExist(self.key,scoreboard)
        # Return
        return self._filterPing(returnData)
    # Mapped methods
    def EncDec(self,string,mode):
        returnData = self.encdec(key=self.kryptokey,inputs=string,mode=mode)
        # Return
        return self._filterPing(returnData)
    def EncDecDict(self,_dict,mode):
        returnData = self.encdec_dict(key=self.kryptokey,dictionary=_dict,mode=mode)
        # Return
        return self._filterPing(returnData)

class experimental_linkedDictionary():
    # INIT
    def __init__(self,connector,scoreboard):
        self.connector = connector
        self.scoreboard = scoreboard
    # Internal
    def _get(self):
        return self.connector.get(self.scoreboard)
    def _set(self,data):
        self.connector.replace(self.scoreboard, data)
    # Methods
    def __setitem__(self, key, value):
        self.connector.append(self.scoreboard,{key:value})
    def __ior__(self, other):
        if isinstance(other, dict):
            self.connector.append(self.scoreboard,other)
        return self
    def __getitem__(self, key):
        local = self._get()
        return local[key]
    def append(self,data):
        self.connector.append(self.scoreboard,data)
    def update(self,data):
        local = self._get()
        local.update(data)
        self._set(local)
    def get(self,key=None):
        if key != None:
            return self._get()[key]
        else:
            return self._get()
    def set(self,data):
        self.connector.replace(self.scoreboard,data)
    # ConnectorMethods
    def conn_create(self,data=None):
        if data != None:
            self.connector.create(self.scoreboard, data)
        else:
            self.connector.create(self.scoreboard)
    def conn_replace(self,data):
        self.connector.replace(self.scoreboard,data)
    def conn_append(self,data):
        self.connector.append(self.scoreboard,data)
    def conn_get(self):
        self.connector.get(self.scoreboard)
    def conn_remove(self):
        self.connector.remove(self.scoreboard)

# Function to get TOS
def gamehub_getTOS(net=bool(),decode=True):
    if net == True:
        import requests
        r = requests.get("https://raw.githubusercontent.com/sbamboo/Gamehub/main/API/v2/tos.txt", allow_redirects=True)
        if decode == False:
            return r.content
        else:
            return r.content.decode()
    else:
        return open(f"{os.path.abspath(os.path.dirname(__file__))}{os.sep}tos.txt",'r').read()

# Main function for handling a scoreboard from a function
def gamehub_scoreboardFunc(
        encType=None,manager=None,apiKey=None,encKey=None,managerFile=None,ignoreManFormat=None,
        _scoreboard=str(),jsonData=dict(),
        create=False,replace=False,remove=False,get=False,append=False, doesExist=False,
        doCheckExistance=None, autoHandlePingRemoval=True, autoFindGlobalManagerFile=True
    ):
    # Create scoreboardConnector
    scoreboard = scoreboardConnector(encryptionType=encType, storageType=manager, key=apiKey, kryptographyKey=encKey, managersFile=managerFile, ignoreManagerFormat=ignoreManFormat, doCheckExistance=doCheckExistance, autoHandlePingRemoval=autoHandlePingRemoval, autoFindGlobalManagerFile=autoFindGlobalManagerFile)
    # Actions
    if create == True: return scoreboard.create(scoreboard=_scoreboard,jsonDict=jsonData)
    elif replace == True: return scoreboard.replace(scoreboard=_scoreboard,jsonDict=jsonData)
    elif remove == True: return scoreboard.remove(scoreboard=_scoreboard)
    elif get == True: return scoreboard.get(scoreboard=_scoreboard)
    elif append == True: return scoreboard.append(scoreboard=_scoreboard,jsonDict=jsonData)
    elif doesExist == True: return scoreboard.doesExist(scoreboard=_scoreboard)

# ========================================================[CLI Executor]========================================================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="GamehubAPI")
    # Flags
    ## [requireAPI]
    parser.add_argument('--requireAPI','--require', dest="requireAPI", action='store_true', help="Function to check/require an API version to be installed.")
    ## [ManagerAPI]
    parser.add_argument('--registerManager','--regMan', action='store_true', help="Function to register a manager.")
    parser.add_argument('--unregisterManager','--unregMan', action='store_true', help="Function to unregister a manager.")
    ## [tempfileAPI]
    parser.add_argument('--createTempDir', action='store_true', help="Creates a tempDir and returns it's path.")
    parser.add_argument('--deleteTempDir', action='store_true', help="Deletes a tempDir, takes path see params.")
    parser.add_argument('--cleanFolder', action='store_true', help="Cleans a tempDir, takes path see params.")
    parser.add_argument('--saveDict', action='store_true', help="Executes the saveDict function, see params.")
    parser.add_argument('--loadDict', action='store_true', help="Executes the loadDict function, see params.")
    ## [mainAPI]
    parser.add_argument('--getTOS', action='store_true', help="Function to get the tos.")
    parser.add_argument('--asFunction', action='store_true', help="Executes the loadDict function, see params.")
    # Arguments
    ## [requireAPI]
    parser.add_argument('-rq_apiVid', dest="rq_apiVid", help="requireAPI: The version required to test (str)")
    parser.add_argument('-rq_verFileOverwrite','-rq_verfover', dest="rq_verFileOverwrite", help="requireAPI: Overwrite path of verFile (str)")
    ## [managerAPI]
    parser.add_argument('-mg_managerFile', dest="mg_managerFile", help="managerAPI: Supply managerFile, otherwise will fallback to 'os.path.dirname(__file__){os.sep}managers.jsonc' (str)")
    parser.add_argument('-mg_name', dest="mg_name", help="managerAPI: Name of manager to register/unregister (str)")
    parser.add_argument('-mg_path', dest="mg_path", help="managerAPI: Path to the manager that will be registered, '.py' files only (str)")
    parser.add_argument('--mg_needKey', action='store_true', dest="mg_needKey", help="managerAPI: Whether or not the manager needs a key. Encryption is choosen by user, so al cryptolib ones should be available or inform user otherwise (str)")
    ## [tempfileAPI]
    parser.add_argument('-tf_securityLevel','-tf_slvl', dest="tf_securityLevel", help="tempfileAPI: The security level to use (int: 0,1,2,3) see docs")
    parser.add_argument('-tf_encType', dest="tf_encType", help="tempfileAPI: Encryption type to use (str: 'legacy' or 'aes')")
    parser.add_argument('-tf_encKey', dest="tf_encKey", help="tempfileAPI: Encryption key to use (str)")
    parser.add_argument('-tf_hashType', dest="tf_hashType", help="tempfileAPI: Hash algorithm to use key to use (str) see docs")
    parser.add_argument('-tf_tempFolder', dest="tf_tempFolder", help="TtempfileAPI: he path to the tempFolder, USE THE --createTempDir TO GET THIS, see docs (str)")
    parser.add_argument('-tf_fileName', dest="tf_fileName", help="tempfileAPI: The filename to save/load the file to. (str)")
    parser.add_argument('-tf_filehash', dest="tf_fileHash", help="tempfileAPI: The hash of the tile, to match to. |ONLY FOR 'loadDict'| (str)")
    parser.add_argument('-tf_jsonStr', dest="tf_jsonStr", help="tempfileAPI: The content to save to the file in json form. |ONLY FOR 'saveDict'| (str)")
    ## [mainAPI]
    parser.add_argument('--m_net', dest='m_net', help="mainAPI: getTos from internet of local.", action='store_true')
    parser.add_argument('-m_encType', dest='m_encType', help="mainAPI: encryption type (str)")
    parser.add_argument('-m_encKey', dest='m_encKey', help="mainAPI: encryption key (str)")
    parser.add_argument('-m_manager', dest='m_manager', help="mainAPI: manager to use (str)")
    parser.add_argument('-m_apiKey', dest='m_apiKey', help="mainAPI: api key(str)")
    parser.add_argument('-m_managerFile', dest='m_managerFile', help="mainAPI: path to managerFile (str)")
    parser.add_argument('--m_ignoreManFormat', dest='m_ignoreManFormat', help="mainAPI: ignoreManFormat.", action="store_true")
    parser.add_argument('-m_scoreboard', dest='m_scoreboard', help="mainAPI: scoreboard to use (str)")
    parser.add_argument('-m_jsonData', dest='m_jsonData', help="mainAPI: json data to send (str)")
    parser.add_argument('--m_create', dest='m_create', help="mainAPI: Creates a scoreboard.", action='store_true')
    parser.add_argument('--m_replace', dest='m_replace', help="mainAPI: Replaces a scoreboard.", action='store_true')
    parser.add_argument('--m_remove', dest='m_remove', help="mainAPI: Remove a scoreboard.", action='store_true')
    parser.add_argument('--m_get', dest='m_get', help="mainAPI: Gets a scoreboard.", action='store_true')
    parser.add_argument('--m_append', dest='m_append', help="mainAPI: Appends data to a scoreboard.", action='store_true')
    parser.add_argument('--m_doesExist', dest='m_doesExist', help="mainAPI: Checks if a scoreboard exists.", action='store_true')
    parser.add_argument('--m_doCheckExistance', dest='m_doCheckExistance', help="mainAPI: Flag for if the manager should check for scoreboard existance before calling, see format3.", action='store_true')
    parser.add_argument('--m_autoHandlePingRemoval', dest='m_autoHandlePingRemoval', help="mainAPI: Should the connector filter backupService pings?.", action='store_true')
    parser.add_argument('--m_autoFindGlobalManagerFile', dest='m_autoFindGlobalManagerFile', help="mainAPI: Should the connector attempt again to find the manager file.", action='store_true')
    ## [General]
    parser.add_argument('autoComsume', nargs='*', help="AutoConsume")
    # Get Inputs
    args = parser.parse_args(sys.argv)
    # [requireAPI]
    if args.requireAPI == True:
        out = requireAPI(apiVid=args.rq_apiVid,verFileOverwrite=args.rq_verFileOverwrite)
        print(out)
    # [managerAPI]
    if args.registerManager == True:
        if args.mg_managerFile:
            out = registerManager(managerFile=args.mg_managerFile,name=args.mg_name,path=args.mg_path,needKey=args.mg_needKey)
        else:
            out = registerManager(name=args.mg_name,path=args.mg_path,needKey=args.mg_needKey)
        print(out)
    if args.unregisterManager == True:
        if args.mg_managerFile:
            out = registerManager(managerFile=args.mg_managerFile,name=args.mg_name)
        else:
            out = unregisterManager(name=args.mg_name)
        print(out)
    # [tempfileAPI]
    if args.createTempDir == True:
        out = createTempDir()
        print(out)
    if args.deleteTempDir == True:
        out = deleteTempDir(tempFolder=args.tf_tempFolder)
        print(out)
    if args.cleanFolder == True:
        out = cleanFolder(tempFolder=args.tf_tempFolder)
        print(out)
    if args.saveDict == True:
        out = saveDict(securityLevel=args.tf_securityLevel,encType=args.tf_encType,encKey=args.tf_encKey,hashType=args.tf_hashType,tempFolder=args.tf_tempFolder, fileName=args.tf_fileName, jsonStr=args.tf_jsonStr)
        print(out)
    if args.loadDict == True:
        out = loadDict(securityLevel=args.tf_securityLevel,encType=args.tf_encType,encKey=args.tf_encKey,hashType=args.tf_hashType,tempFolder=args.tf_tempFolder, fileName=args.tf_fileName, filehash=args.tf_fileHash)
        print(out)
    # [mainAPI]
    if args.getTOS == True:
        out = gamehub_getTOS(net=args.m_net)
        print(out)
    if args.asFunction == True:
        if args.doCheckExistance != None:
            out = gamehub_scoreboardFunc(encType=args.m_encType,manager=args.m_manager,apiKey=args.m_apiKey,encKey=args.m_encKey,managerFile=args.m_managerFile,ignoreManFormat=args.m_ignoreManFormat,_scoreboard=args.m_scoreboard,jsonData=args.m_jsonData,create=args.m_create,replace=args.m_replace,remove=args.m_remove,get=args.m_get,append=args.m_append,doesExist=args.m_doesExist,autoHandlePingRemoval=args.m_autoHandlePingRemoval,autoFindGlobalManagerFile=args.m_autoFindGlobalManagerFile,doCheckExistance=args.m_doCheckExistance)
        else:
            out = gamehub_scoreboardFunc(encType=args.m_encType,manager=args.m_manager,apiKey=args.m_apiKey,encKey=args.m_encKey,managerFile=args.m_managerFile,ignoreManFormat=args.m_ignoreManFormat,_scoreboard=args.m_scoreboard,jsonData=args.m_jsonData,create=args.m_create,replace=args.m_replace,remove=args.m_remove,get=args.m_get,append=args.m_append,doesExist=args.m_doesExist,autoHandlePingRemoval=args.m_autoHandlePingRemoval,autoFindGlobalManagerFile=args.m_autoFindGlobalManagerFile)
        print(out)

# Info
# registering should start with choosing a security level:
# 0. No extra meassures
# 1. Hash savefile and check it before save
# 2. Encrypt the savefile content and decrypt on upload
# 3. Both hash and encrypt the content of the savefile

# Examples of tempFile management
## Creation of tempPath:
# $tempPath = python3 gamehubAPI.py --createTempDir
# python3 gamehubAPI.py --deleteTempDir --tempFolder $tempPath
## SecurityLevel 0:
# python3 gamehubAPI.py --saveDict -tf_slvl 0 -tf_tempFolder $tempPath -tf_fileName "bob" -tf_jsonStr '{"bob":5}'
# python3 gamehubAPI.py --loadDict -tf_slvl 0 -tf_tempFolder $tempPath -tf_fileName "bob"
## SecurityLevel 1:
# $fileHash = python3 gamehubAPI.py --saveDict -tf_slvl 1 -tempFolder $tP -tf_fileName "bob" -tf_jsonStr '{"bob":10}' -tf_hashType "sha256"
# python3 gamehubAPI.py --loadDict -tf_slvl 1 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_hashType "sha256" -tf_filehash $fileHash
## SecurityLevel 2:
# python3 gamehubAPI.py --saveDict -tf_slvl 3 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_jsonStr '{"bob":10}' -tf_encType "aes" -tf_encKey "secret"
# python3 gamehubAPI.py --loadDict -tf_slvl 3 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_encType "aes" -tf_encKey "secret"
## SecurityLevel 3:
# $fileHash = python3 gamehubAPI.py --saveDict -slvl 3 -tempFolder $tempFolder -tf_fileName "bob" -tf_jsonStr '{"bob":10}' -tf_encType "aes" -tf_encKey "secret" -tf_hashType "sha256"
# python3 gamehubAPI.py --loadDict -tf_slvl 3 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_encType "aes" -tf_encKey "secret" -tf_hashType "sha256" -tf_filehash $fileHash
## Cleaning up if a problem occurs:
# python3 gamehubAPI.py --cleanFolder -tf_tempFolder $tempFolder

# Examples of managerAPI:
## Register/Unregister
