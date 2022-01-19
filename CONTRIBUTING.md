# Sophos Python SDK design

- [Quick start](#quick-start)
- [Some notes on Sophos's API](#some-notes-on-sophos-s-api)
  - [Main reference](#main-reference)
  - [Authentication](#authentication)
  - [XML](#xml)
  - [Transactions](#transactions)
- [This API's design](#this-api-s-design)
  - [JSON instead of XML](#json-instead-of-xml)
  - [Matching the Sophos API Nomenclature](#matching-the-sophos-api-nomenclature)
  - [Key interfaces](#key-interfaces)
  - [Internal design](#internal-design)
  - [A note on the XML <-> JSON conversions](#a-note-on-the-xml-----json-conversions)

## Quick start

Thank you for your interest to contribute!

You are highly encouraged to read through this design document so that your
contributions match the general idea of the package. If you disagree with any
design decision, please raise an issue for discussion of a way forward. The
same goes if your contribution is for something that has not yet been
designed.

To contribute to this package, you may follow these steps:
- clone the repository: `git clone ...`
- create a virtual environment: `virtualenv venv`
- install the dev requirements: `pip install -r requirements-dev.txt`
- install the API locally in edit mode: `pip install -e .`
- set up the pre-commit hooks: `pre-commit install`
- launch an initial run of pre-commit: `pre-commit run --all-files`
- launch an initial run of mypy: `mypy ./sophosapi/`
- launch an initial run of the tests: `pytest`
- Create your branch and contribute away!

## Some notes on Sophos's API

### Main reference

https://docs.sophos.com/nsg/sophos-firewall/18.5/API/index.html

### Authentication

The Sophos API requires that each request is sent with a username and
password. There's no such things a session token.

This means that the username and password need to remain available until the
script ends.

We have a client which the users interface with. The client stores the username
and password. Something like:
``` python
client = Client(username='my_user', password='my_pass', ...)

response = client.make_api_call(...)
```

The client takes care of using the username and password to make the call.

### XML

The Sophos API used XML to exchange data. The API passes data using the text
inside of XML tags. For example:
``` xml
<Network>my_network</Network>
```

is a reference to a network object called my_network.

XML Elements can also have children when a list is needed, for example:
``` xml
<Networks>
  <Network>my_network01</Network>
  <Network>my_network02</Network>
  <Network>my_network03</Network>
</Networks>
```

There is an element factory to create these elements, with a tag and text.
Then each API function generates the required Elements and sets up their
relationship (children, etc).

We are using the package defusedxml to have a more secure implementation of
ElementTree than the built-in version.

### Transactions

A single API request can have multiple transactions, that is multiple API
calls. Each transaction can be identified by a transaction ID:
``` xml
<Set operation="add">
  <IPHost transactionid="1">
    <Name>host01</Name>
    <IPFamily>IPv4</IPFamily>
    <HostType>IP</HostType>
    <IPAddress>1.1.1.1</IPAddress>
  </IPHost>
  <IPHost transactionid="2">
    <Name>host02</Name>
    <IPFamily>IPv4</IPFamily>
    <HostType>IP</HostType>
    <IPAddress>2.2.2.2</IPAddress>
  </IPHost>
</Set>
```

The server then responds with a status for each transaction. It might be
useful for the user to know exactly which transaction failed, so it would be
best if we stored the transaction IDs and their corresponding request so that
we can refer to them when showing errors to the users.

## This API's design

### JSON instead of XML

The API is built in such a way that the user interfaces with it via JSON,
rather than XML. That is, the user will provide requests using JSON, and
receive responses in JSON. There are respective internal helper functions
which do the necessary conversions. There are a couple of noteworthy caveats
that are discussed a bit later.

### Matching the Sophos API Nomenclature

Sophos use the verbs Set, Get, Remove for different tasks, this API does
the same. For Set, there are also the optional 'add' and 'update' parameters,
which have their seperate verb alongside the main three.

The term 'transaction' will be used to refer to a single call in a request,
and 'entity' will be used to refer to a top-level objects such as 'IPHost' or
'FirewallRule'.

### Key interfaces

There are 3 key objects that the user interacts with.
- Client: the client stores the credentials as well as sends requests to the
  server and receives the responses from the server (firewall).
- Request: the request is built by the user, by adding transactions to it.
- Response: this is the reply by the firewall, listing all successful and
  failed API calls.

Generally speaking the user will have this sort of script:
``` python
client = Client(...)

request = Request()

request.set_host(...)
request.set_host(...)
request.set_network(...)
request.set_firewall_rule(...)

responses = client.send(request)

for response in responses:
    print(response.data)

```

It is expected that the user will provide all the required data, especially for
Set tasks. This API does not do validations for required data, data types, etc.
Not yet... and probably not at all.

### Internal design

To be fair, a user most likely expects the API to be in the form of:
``` python
client = Client(...)

response = client.set_host(...)
print(response.data)

response = client.set_host(...)
...
```

If we try to keep both interfaces in mind, the functions in the Client would
duplicate the functions of Request. To avoid duplicate code, the internals of
Client.api_call(...) simply call Request.api_call(...).

Then, the one-call-at-a-time is a wrapper to multiple-calls-at-a-time, but with
a single call.

Therefore we have the following:
``` python
# Request class:
def set_host(self, arg1, arg2, ...):
    # implementation here
    ...

# Client class:
def set_host(self, *args, **kwargs):
    # this just calls Request.set_host(...)
    return self._request_proxy_call("set_host", *args, **kwargs)

def _request_proxy_call(self, fn_name, *args, **kwargs):
    request = Request()
    # call: request.fn_name(*args, **kwargs)
    getattr(request, fn_name)(*args, **kwargs)

    response = self.send(request)
    return response

# User interface:
response = client.set_host(...)
```

### A note on the XML <-> JSON conversions

Generally speaking, XML Elements and sub-elements can be easily represented
as JSON, especially as the Sophos design is quite straightforward, using only
tags and text to define key-value pairs. So the following:
``` xml
<IPHost>
  <Name>My_host</Name>
  <Type>IP</Type>
  <IP>1.1.1.1<IP>
</IPHost>
```

Can be easily represented as:
``` python
{
    "IPHost": {
        "Name": "My_host",
        "Type: "IP",
        "IP": "1.1.1.1"
    }
}
```

The caveat come due to Sophos using a concept of lists in this form:
``` xml
<SourceNetworks>
  <Network>Net_01</Network>
  <Network>Net_02</Network>
  ...
</SourceNetworks>
```

Which needs to be converted to:
``` python
{
    "SourceNetworks": ["Net_01", "Net_02"]
}
```

Converting back and forth requires the API to know that when creating a list of
SourceNetworks, the tag of the children should be "Network". Such a mapping is
hard-coded, but sometimes the same parent is used with different child tags.

For example, FirewallRule and SSLTLSInspectionRule both have an `Identity` tag
with a list of members. But for FirewallRule, the individual members are tagged
as `Member` while for SSLTLSInspectionRule they are tagged as `Members`.
``` xml
<FirewallRule>
  :
  <Identity>
    <Member>users/groups</Member>
    :
  </Identity>
  :
</FirewallRule

<SSLTLSInspectionRule>
  :
  <Identity>
    <Members>users/groups</Members>
    :
  </Identity>
  :
</SSLTLSInspectionRule>
```

This particular example has a special handler in place, along with other
instances such as the LocalServiceACL/Hosts list. This list has elements of
both `Host` and `DstHost`. In this case, the API must deviate from Sophos'
API, and creates an extra list for DstHosts, like so:
``` xml
<LocalServiceACL>
    <RuleName>acl-rule</RuleName>
    <SourceZone>WAN</SourceZone>
    <Hosts>
        <Host>host1</Host>
        <Host>host2</Host>
        <DstHost>dsthost3</DstHost>
        <DstHost>dsthost4</DstHost>
    </Hosts>
</LocalServiceACL>
```

``` python
acl: {
    "RuleName": "acl-rule",
    "SourceZone": "WAN",
    "Hosts": ["host1", "host2"],
    "DstHosts": ["dsthost3", "dsthost4"]
}
```

**These need to be clearly noted to the user. (insert link to user guide)**
