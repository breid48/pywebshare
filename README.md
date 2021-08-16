# pywebshare
Python Wrapper for Webshare API


## Client Authentication Setup

An `API_KEY` can be obtained from your Webshare Account through the [Webshare API Portal](https://proxy.webshare.io/userapi/keys)

There are two ways to provide authentication credentials to the module.
1. Directly invoking the `Webshare` object constructor with your Webshare `API_KEY`

```
client = webshare.Webshare(api_key=API_KEY)
```

2. By default, the object constructs itself through the `env.ini` Configuration File. An example of this file is provided in the project directory. 
  - If the `env.ini` configuration file is stored within the current working directory, or the parent file directory, the object will automatically invoke itself.
```
client = webshare.Webshare()
```
  - Else, the absolute path to the `env.ini` file can be supplied to the constructor:
  
```
client = webshare.Webshare(config_path=ABSOLUTE_PATH_TO_CONFIG)
```

## General Usage of the Webshare Object

```
from pywebshare import webshare

client = webshare.Webshare()
profile = client.get_profile()
```

```
from pywebshare import webshare

subuser_client = webshare.Webshare(portal="subuser", user_id=SUBUSER_ID)
```
