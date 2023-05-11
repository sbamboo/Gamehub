# General imports
import os
import tempfile
import uuid
import json
import argparse

# Local imports
from libs.libhasher import hashFile,hashString
from libs.libfilesys import filesys as fs

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
        from libs.libcrypto.legacy import encdec,GenerateKey
    elif encType == "aes":
        from libs.libcrypto.aes import encdec,GenerateKey
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
        from libs.libcrypto.legacy import encdec,GenerateKey
    elif encType == "aes":
        from libs.libcrypto.aes import encdec,GenerateKey
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