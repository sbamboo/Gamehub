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
def saveDict(securityLevel=int(),encType=None,encKey=None,hashType=None, tempFolder=str(), fileName=str(), content=dict()):
    # Import encryption lib
    if encType == "legacy":
        from ..libs.libcrypto.legacy import encdec
    elif encType == "aes":
        from ..libs.libcrypto.aes import encdec
    # Get secure fileName
    fileId = hashString(message=fileName, hashType=hashType)
    toSave = json.dumps(content)
    # encrypt
    isEnc = False
    if securityLevel == 2 or securityLevel == 3:
        isEnc = True
        toSave = encdec(key=encKey,inputs=toSave,mode="enc")
    # Should hash
    isHashed = False
    if securityLevel == 1 or securityLevel == 3:
        isHashed = True
    # Save file
    filePath = os.path.join(tempFolder, f"{fileId}.ghs") # ghs = GamehubSync File
    fs.writeToFile(inputs=toSave,filepath=filePath,autocreate=True)
    # Return file
    return str(hashFile(filePath, hashType))

# Function to load a dictionary from a tempFile
def loadDict(securityLevel=int(),encType=None,encKey=None,hashType=None, tempFolder=str(), fileName=str(), filehash=str()) -> dict:
    # Import encryption lib
    if encType == "legacy":
        from ..libs.libcrypto.legacy import encdec
    elif encType == "aes":
        from ..libs.libcrypto.aes import encdec
    # encrypt
    isEnc = False
    if securityLevel == 2 or securityLevel == 3:
        isEnc = True
        toSave = encdec(key=encKey,inputs=toSave,mode="enc")
    # Should hash
    isHashed = False
    if securityLevel == 1 or securityLevel == 3:
        isHashed = True
    # Get secure fileName
    fileId = hashString(message=fileName, hashType=hashType)
    # Filepath
    filePath = os.path.join(tempFolder, f"{fileId}.ghs") # ghs = GamehubSync File
    # Match hash
    if isHashed == True:
        fileHash = hashFile(filePath, hashType)
        if str(fileHash) != filehash:
            raise Exception("Hash of file didn't match, loading aborted!")
    # Get content
    toGive = fs.readFromFile(filePath)
    # Decrypt content
    if isEnc == True:
        toGive = encdec(key=encKey,inputs=toGive,mode="dec")
    # Convert to dictionary
    return json.loads(toGive)