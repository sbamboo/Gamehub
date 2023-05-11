import os
import tempfile
import uuid
import json

from ..libs.libhasher import hashFile
from ..libs.libfilesys import filesys as fs
from ..gamehubAPI import scoreboardConnector,requireAPI
from ..ManagerAPI import registerManager,unregisterManager

# This file should be able to be runned with arguments instead of importing it's functions, this is for future connectors

# registering should start with choosing a security level:
# 0. No extra meassures
# 1. Hash savefile and check it before save
# 2. Encrypt the savefile content and decrypt on upload
# 3. Both hash and encrypt the content of the savefile


# Class to handle the temp file (creation/reading-removing)
class tempfile():
    savedFiles = dict()
    def __init__(securityLevel=int(),encType=None,encKey=None,hashType=None):
        self.securityLevel = securityLevel
        self.hashType = hashType
        self.encKey = encKey
        # Import correct crypto
        if encType == "legacy":
            from ..libs.libcrypto import legacy as crypto
            self.cryptLib = crypto
        elif encType == "aes":
            from ..libs.libcrypto import aes as crypto
            self.cryptLib = crypto
        # Create directory
        self.tempDir = createTempDir()
    # Save to a file
    def saveDict(content=dict()) -> str:
        fileId = str( len(savedFiles.keys())+1 )
        toSave = json.dumps(content)
        # encrypt
        isEnc = False
        if self.securityLevel == 2 or self.securityLevel == 3:
            isEnc = True
            toSave = self.cryptLib.encdec(key=self.encKey,inputs=toSave,mode="enc")
        # Should hash
        isHashed = False
        if self.securityLevel == 1 or self.securityLevel == 3:
            isHashed = True
        # Save file
        filePath = os.path.join(self.tempDir, f"{fileId}.ghs") # ghs = GamehubSync File
        fs.writeToFile(inputs=toSave,filepath=filePath,autocreate=True)
        self.savedFiles[fileId] = {"path":filePath,"encrypted":isEnc,"hashed":isHashed, "hash":None}
        # hash
        if isHashed == True:
            self.savedFiles[fileId]["hash"] = hashFile(filePath, self.hashType)
        return fileId
    # Load from a file
    def loadDict(fileId=str()) -> dict:
        fileMeta = self.savedFiles[fileId]
        filePath = fileMeta["path"]
        # Match hash
        fileHash = hashFile(filePath, self.hashType)
        if str(fileHash) != str(fileMeta["hash"]):
            raise Exception("Hash of file didn't match, loading aborted!")
            return {}
        # Get content
        toGive = fs.readFromFile(filePath)
        # Decrypt content

        if fileMeta["encrypted"] == True:
            toGive = self.cryptLib.encdec(key=self.encKey,inputs=toGive,mode="dec")
        # Convert to dictionary
        return json.loads(toGive)