# The unofficial Sophos SFOS Python SDK
This package is a Python SDK used to interface with the Sophos SFOS API. Its
interface is JSON-based, as opposed to Sophos' XML. This means that sometimes, there are small deviations from Sophos' API, which are listed [here](./API%20Deviations.md).

## Quick start
1. Set up a python virtual environment
2. Install the package: `pip install git+https://github.com/stevensultana/sophosapi`
3. Set up your Firewall for API, create an API user on your Firewall and get an encrypted form of the password:
    - https://docs.sophos.com/nsg/sophos-firewall/18.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/API/APIUsingAPI/index.html
   - https://docs.sophos.com/nsg/sophos-firewall/18.5/Help/en-us/webhelp/onlinehelp/AdministratorHelp/BackupAndFirmware/API/index.html#get-the-encrypted-password-for-api-requests
4. Run an initial test script:
``` python
from sophosapi import Client

client = Client(
    username="your_username",
    password="your_encrypted_password",
    server="host_name_or_ip_address",
    port="4444",  # default is 4444 - so you can omit this
)

login = client.test_login()
if login["status_code"] != 200:
    print(login["message"])
    exit(login["status_code"])
else:
    print(login["message"])
    exit 0
```

## Tips and tricks

TODO
