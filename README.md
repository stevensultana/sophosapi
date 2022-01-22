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

## Usage

- The available APIs are:
  - `get(entity)` - get a list of all entities of this type.

    Eg. `responses = client.get("Zone")  # list of all Zones`

  - `get_filter(entity_name, filter_type, name)` - get a list of entities which
    match the name, or except the given name. Note that the output is a list,
    even for 1 item.

    Eg. `responses = client.get_filter("Zone", Filter.EQUAL, "LAN")  # get LAN zone`

    Eg. `responses = client.get_filter("Zone", Filter.LIKE, "AN")  # get zones with "AN" in the name`

    Eg. `responses = client.get_filter("Zone", Filter.EXCEPT, "LAN")  # get all zones except LAN`

    **Note:** To use filters, you need to import the Filter enum: `from sophosapi import Filter`

  - `set(entity, data)` - create or update an entity, with the given data.
    The response is not a list, but the direct data.
    Eg.
    ``` python
    data = {
        "Name": "new_zone",
        "Type": "LAN",
        "ApplianceAccess": {
            "AuthenticationServices": {
                "CaptivePortal": "Enable"
            },
            "NetworkServices": {
                "DNS": "Enable",
                "Ping": "Enable"
            }
        }
    }

    response = client.set("Zone", data)
    ```

  - `add(entity, data)` - like set, but will fail if an entity with the same name exists.

  - `update(entity, data)` - like set, but will fail if the entity does not exist.

  - `remove(entity, name)` - remove the entity with the given name.

    Eg. `response = client.remove(entity, name)`

- For the `get` functions, the output is a list of `Response` objects. A `Response`
  has 2 main properties: the `data` and the `status_code`.

- For the `set`, `add`, `update` and `remove` functions, the output is a single
  `Response`. The data and status code indicate the success of the call.

- use `get` calls to familiarize yourself with the API. This way you would
  have a good example of how your `set` data should be built, as well as an
  indication if there is some missing function in this SDK.

- if you do not provide the username, password or Firewall IP, you will be
  asked to provide these. The password that you provide needs to be the
  plaintext password in this case.

  You can also set environment variables for the username, encrypted password
  and Firewall IP or hostname:
  - SOPHOS_API_USERNAME
  - SOPHOS_API_PASSWORD_ENCRYPTED
  - SOPHOS_API_FIREWALL_IP

- You can aggregate calls by building a `Request`.
  ``` python
  from sophosapi import Client
  from sophosapi import Request

  client = Client()
  request = Request(apiversion="1805.2")

  request.set("Zone", {...})
  request.set("IPHost", {...})
  request.get("FirewallRule")

  responses = client.send(request)
  ...
  ```

  In this case, note that the order that you prepare the calls is not preserved.
  `get` requests are processed first, followed by `set`, `add`, `update` and
  `remove`. The `Response`s have a `transactionid` field which can help determine
  which call the response belongs to.
