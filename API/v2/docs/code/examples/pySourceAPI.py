from ....Source.gamehubAPI import scoreboardConnector

# Initializing a scoreboard connector with the storagetype being pantry (BuiltInPantryManager) and supply our pantryKey
# In this example we haven't encrypted our pantryKey, which is a requirement if you want to share your software using GamehubAPI,
#  To encrypt it we would have to supply 'encryptionType' as either "legacy" or "aes", legacy being safer but aes being crossplatform (any platform supporting Fernet) JUST MAKE SURE TO ALWAYS USE THE SAME!!!
#  We also need 'kryptographyKey' as the key to decrypt the encrypted key.
scoreboard = scoreboardConnector(storageType="pantry",key="<pantryKey>")
# Creating a scoreboard:
scoreboard.create("snake2")
# Getting the data
print( scoreboard.get("snake2") )

# Lets wait so we dont reach an API limit
import time
time.sleep(3)

# Adding values
scoreboard.append("snake2",{"bob":5})
# Getting the new values
print( scoreboard.get("snake2") )