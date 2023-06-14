# Format 3

**The manager python file should include a variable called "managerFormat" being a list of three entries, first the formatNumber being an integer, secondly a link to the format information (like this page) and lastly the supported other versions as a list of ints, then the file should include a class called "Manager"**

*OBS! Format 3 is the first format to implement support for multiple formats, and format3 is compatible with Format2,*
*Format3 should be compatible with GamehubAPI.ManagerFormat2 but otherSupportedFormats will be ignored, so use the **"ignoreManagerFormat"** flag.*
*GamehubAPI.ManagerFormat3 is compatible with managerFormat2, but otherSupported will be APIside*

## The format requires the following methods and arguments inside the class

### create
creates a scoreboard, taking "scoreboard" of string and optionally "key" of string, optionally "doCheck" boolean

### replace
replaces a scoreboard and/or it's content, taking "scoreboard" of string and "jsonDict" of dictionary and optionally "key" of string, optionally "doCheck" boolean

### remove
removes a scoreboard, taking "scoreboard" of string and optionally "key" of string, optionally "doCheck" boolean

### get
gets the content of a scoreboard, taking "scoreboard" of string and optionally "key" of string

### append
appends a value of dictionary to the scoreboard, taking "scoreboard" of string "jsonDict" of dictionary and optionally "key" of string

### doesExist:
checks weather or not a scoreboard exists, taking "scoreboard" of string and optionally "key" of string

*Format was created on 2023-06-13*

## Changelog

1. Added the doCheck flag to each method, can be sent toMethod or globaly to the API