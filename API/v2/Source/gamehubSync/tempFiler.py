import os
import tempfile
import uuid
import json

from ..libs.libhasher import hashFile,hashString
from ..libs.libfilesys import filesys as fs

# Internal function to get a tempFile
def createTempDir() -> str:
    """
    Creates a temporary folder with a random name and returns the path to it.
    """
    temp_folder = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
    os.mkdir(temp_folder)
    return temp_folder

# Function to save a dictionary to a tempFile
def saveDict(securityLevel=int(),encType=None,encKey=None,hashType=None, fileName=str(), content=dict()):
    # Import encryption lib
    if encType == "legacy":
        from ..libs.libcrypto.legacy import encdec
    elif encType == "aes":
        from ..libs.libcrypto.aes import encdec
    # Get secure fileName
    fileId = hashString(message=fileName, )
    toSave = json.dumps(content)
    # encrypt
    isEnc = False
    if securityLevel == 2 or securityLevel == 3:
        isEnc = True
        toSave = self.cryptLib.encdec(key=self.encKey,inputs=toSave,mode="enc")
    # Should hash
    isHashed = False
    if securityLevel == 1 or securityLevel == 3:
        isHashed = True
    # Save file
    filePath = os.path.join(self.tempDir, f"{fileId}.ghs") # ghs = GamehubSync File
    fs.writeToFile(inputs=toSave,filepath=filePath,autocreate=True)
    self.savedFiles[fileId] = {"path":filePath,"encrypted":isEnc,"hashed":isHashed, "hash":None}
    # hash
    if isHashed == True:
        self.savedFiles[fileId]["hash"] = hashFile(filePath, self.hashType)
    return fileId

# Function to load a dictionary from a tempFile
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