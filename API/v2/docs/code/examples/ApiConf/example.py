# Please read the InternalUsage.py example first

# Lets start by importing our ScoreboardConnector, however this time from the quickuseAPI so we can use apiConf files
from .....Source.quickuseAPI import apiConfigScoreboardConnector

# Then create an object for it, this time we only have to send a path to our apiconf file
scoreboard = apiConfigScoreboardConnector(apiConfPath=".\\api.conf")

# That is al for setup so lets use it:

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