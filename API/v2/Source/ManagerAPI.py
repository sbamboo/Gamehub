# GamehubAPI - ManagerAPI: Handles registration and unregistration of global managers, for local ones (ones in your own files, provide managerFile path or create your own implementation of the ManagerAPI)
import json,os

parentPath = os.path.dirname(__file__)

def registerManager(managerFile=f"{parentPath}\\managers.jsonc",name=str(),path=str(),needKey=bool()):
    '''
       Registers a manager, by default in the global manager file. If your custom manager file is wanted give it's path to managerFile.
       managerFile = <str>, Supply managerFile, otherwise will fallback to "os.path.dirname(__file__)\\managers.jsonc"
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

def unregisterManager(managerFile=f"{parentPath}\\managers.jsonc",name=str()):
    '''
       Unregisters a manager, by default in the global manager file. If your custom manager file is wanted give it's path to managerFile.
       managerFile = <str>, Supply managerFile, otherwise will fallback to "os.path.dirname(__file__)\\managers.jsonc"
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
    