from ....Source.gamehubAPI import scoreboardConnector

# Initializing a scoreboard connector with the storagetype being pantry (BuiltInPantryManager) and supply our pantryKey
# In this example we haven't encrypted our pantryKey, which is a requirement if you want to share your software using GamehubAPI,
#  To encrypt it, we would have to supply 'encryptionType' as either "legacy" or "aes", legacy being safer but aes being crossplatform (legacy supports any platform supporting Fernet) JUST MAKE SURE TO ALWAYS USE THE SAME!!!
#  We would also need 'kryptographyKey' as the key to decrypt the encrypted key.
scoreboard = scoreboardConnector(storageType="pantry",key="<pantryKey>")
# Creating a scoreboard:
scoreboard.create("example")
# Getting the data
print( scoreboard.get("example") )

# Lets wait so we dont reach an API limit
import time
time.sleep(3)

# Adding values
scoreboard.append("example",{"bob":5})
# Getting the new values
print( scoreboard.get("example") )