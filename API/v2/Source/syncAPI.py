# [Imports]
import sys
import managerAPI as manAPI
from gamehubAPI import *

# [Executor]
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(prog="GamehubAPI_tempFiler")
    # Flags
    ## [tempfileAPI]
    parser.add_argument('--createTempDir', action='store_true', help="Creates a tempDir and returns it's path.")
    parser.add_argument('--deleteTempDir', action='store_true', help="Deletes a tempDir, takes path see params.")
    parser.add_argument('--cleanFolder', action='store_true', help="Cleans a tempDir, takes path see params.")
    parser.add_argument('--saveDict', action='store_true', help="Executes the saveDict function, see params.")
    parser.add_argument('--loadDict', action='store_true', help="Executes the loadDict function, see params.")
    ## [requireAPI]
    parser.add_argument('--require', action='store_true', help="Checks if the correct API version is installed.")
    ## [managerAPI]
    parser.add_argument('--registerManager', action='store_true', help="Registers a manager, see params.")
    parser.add_argument('--unregisterManager', action='store_true', help="Unregisters a manager, see params.")
    # Arguments
    ## [tempfileAPI]
    parser.add_argument('-tf_securityLevel','-tf_slvl', dest="tf_securityLevel", help="tempfileAPI: The security level to use (int: 0,1,2,3) see docs")
    parser.add_argument('-tf_encType', dest="tf_encType", help="tempfileAPI: Encryption type to use (str: 'legacy' or 'aes')")
    parser.add_argument('-tf_encKey', dest="tf_encKey", help="tempfileAPI: Encryption key to use (str)")
    parser.add_argument('-tf_hashType', dest="tf_hashType", help="tempfileAPI: Hash algorithm to use key to use (str) see docs")
    parser.add_argument('-tf_tempFolder', dest="tf_tempFolder", help="TtempfileAPI: he path to the tempFolder, USE THE --createTempDir TO GET THIS, see docs (str)")
    parser.add_argument('-tf_fileName', dest="tf_fileName", help="tempfileAPI: The filename to save/load the file to. (str)")
    parser.add_argument('-tf_filehash', dest="tf_fileHash", help="tempfileAPI: The hash of the tile, to match to. |ONLY FOR 'loadDict'| (str)")
    parser.add_argument('-tf_jsonStr', dest="tf_jsonStr", help="tempfileAPI: The content to save to the file in json form. |ONLY FOR 'saveDict'| (str)")
    ## [requireAPI]
    parser.add_argument('-rq_apiVid', dest="rq_apiVid", help="requireAPI: The version required to test (str)")
    parser.add_argument('-rq_verFileOverwrite', dest="rq_verFileOverwrite", help="requireAPI: Overwrite path of verFile (str)")
    ## [managerAPI]
    parser.add_argument('-mg_managerFile', dest="mg_managerFile", help="managerAPI: Supply managerFile, otherwise will fallback to 'os.path.dirname(__file__)\\managers.jsonc' (str)")
    parser.add_argument('-mg_name', dest="mg_name", help="managerAPI: Name of manager to register/unregister (str)")
    parser.add_argument('-mg_path', dest="mg_path", help="managerAPI: Path to the manager that will be registered, '.py' files only (str)")
    parser.add_argument('--mg_needKey', action='store_true', dest="mg_needKey", help="managerAPI: Whether or not the manager needs a key. Encryption is choosen by user, so al cryptolib ones should be available or inform user otherwise (str)")
    ## [General]
    parser.add_argument('autoComsume', nargs='*', help="AutoConsume")
    # Get Inputs
    args = parser.parse_args(sys.argv)
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
    # [requireAPI]
    if args.require == True:
        pass
    # [managerAPI]
    if args.registerManager == True:
        if args.mg_managerFile:
            out = manAPI.registerManager(managerFile=args.mg_managerFile,name=args.mg_name,path=args.mg_path,needKey=args.mg_needKey)
        else:
            out = manAPI.registerManager(name=args.mg_name,path=args.mg_path,needKey=args.mg_needKey)
        print(out)
    if args.unregisterManager == True:
        if args.mg_managerFile:
            out = manAPI.registerManager(managerFile=args.mg_managerFile,name=args.mg_name)
        else:
            out = manAPI.unregisterManager(name=args.mg_name)
        print(out)

# Info
# registering should start with choosing a security level:
# 0. No extra meassures
# 1. Hash savefile and check it before save
# 2. Encrypt the savefile content and decrypt on upload
# 3. Both hash and encrypt the content of the savefile

# Examples of tempFile management
## Creation of tempPath:
# $tempPath = python3 syncAPI.py --createTempDir
# python3 syncAPI.py --deleteTempDir --tempFolder $tempPath
## SecurityLevel 0:
# python3 syncAPI.py --saveDict -tf_slvl 0 -tf_tempFolder $tempPath -tf_fileName "bob" -tf_jsonStr '{"bob":5}'
# python3 syncAPI.py --loadDict -tf_slvl 0 -tf_tempFolder $tempPath -tf_fileName "bob"
## SecurityLevel 1:
# $fileHash = python3 syncAPI.py --saveDict -tf_slvl 1 -tempFolder $tP -tf_fileName "bob" -tf_jsonStr '{"bob":10}' -tf_hashType "sha256"
# python3 syncAPI.py --loadDict -tf_slvl 1 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_hashType "sha256" -tf_filehash $fileHash
## SecurityLevel 2:
# python3 syncAPI.py --saveDict -tf_slvl 3 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_jsonStr '{"bob":10}' -tf_encType "aes" -tf_encKey "secret"
# python3 syncAPI.py --loadDict -tf_slvl 3 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_encType "aes" -tf_encKey "secret"
## SecurityLevel 3:
# $fileHash = python3 syncAPI.py --saveDict -slvl 3 -tempFolder $tempFolder -tf_fileName "bob" -tf_jsonStr '{"bob":10}' -tf_encType "aes" -tf_encKey "secret" -tf_hashType "sha256"
# python3 syncAPI.py --loadDict -tf_slvl 3 -tf_tempFolder $tempFolder -tf_fileName "bob" -tf_encType "aes" -tf_encKey "secret" -tf_hashType "sha256" -tf_filehash $fileHash
## Cleaning up if a problem occurs:
# python3 syncAPI.py --cleanFolder -tf_tempFolder $tempFolder

# Examples of managerAPI:
## Register/Unregister