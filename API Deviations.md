# Deviations from Sophos API

- [FirewallRule](#FirewallRule)
  - [HTTPBasedPolicy - AccessPath](#HTTPBasedPolicy---AccessPath)
  - [HTTPBasedPolicy - Exception](#HTTPBasedPolicy---Exception)
- [LocalServiceACL](#LocalServiceACL)

## FirewallRule

### HTTPBasedPolicy - AccessPath

The AccessPath entity can have multiple `backend`, `allowed_networks` and
`denied_networks` entries. These are represented as lists in the JSON reply.

``` xml
<FirewallRule>
    <Name>rulename</Name>
    <HTTPBasedPolicy>
        <HostedAddress>Address</HostedAddress>
        <AccessPaths>
            <AccessPath>
                <path>/access</path>
                <backend>b1</backend>
                <backend>b2</backend>
                <auth_profile>auth_prof</auth_profile>
                <allowed_networks>a1</allowed_networks>
                <allowed_networks>a2</allowed_networks>
                <denied_networks>d1</denied_networks>
                <denied_networks>d2</denied_networks>
                <stickysession_status>1</stickysession_status>
                <hot_standby>1</hot_standby>
                <websocket_passthrough>1</websocket_passthrough>
            </AccessPath>
        </AccessPaths>
    </HTTPBasedPolicy>
</FirewallRule>
```

``` python
{
    "Name": "rulename",
    "HTTPBasedPolicy": {
        "HostedAddress": "Address",
        "AccessPaths": [
            {
                "path": "/access",
                "backends": ["b1", "b2"],  # note here
                "auth_profile": "auth_prof",
                "allowed_networks": ["a1", "a2"],  # note here
                "denied_networks": ["d1", "d2"],  # note here
                "stickysession_status": "1",
                "hot_standby": "1",
                "websocket_passthrough": "1",
            }
        ]
    }
}

```

### HTTPBasedPolicy - Exception

The Exception entity can have multiple `path`, `source` and
`skip_threats_filter_categories` entries. These are represented as lists in
the JSON reply.

``` xml
<FirewallRule>
    <Name>rulename</Name>
    <HTTPBasedPolicy>
        <HostedAddress>Address</HostedAddress>
        <Exceptions>
            <Exception>
                <path>path_1</path>
                <path>path_2</path>
                <op>and</op>
                <source>source_1</source>
                <source>source_2</source>
                <skip_threats_filter_categories>application_attacks</skip_threats_filter_categories>
                <skip_threats_filter_categories>sql_injection_attacks</skip_threats_filter_categories>
                <skipav>1</skipav>
                <skipbadclients>0</skipbadclients>
                <skipcookie>1</skipcookie>
                <skipform>0</skipform>
                <skipurl>1</skipurl>
            </Exception>
        </Exceptions>
    </HTTPBasedPolicy>
</FirewallRule>
```

``` python
{
    "Name": "rulename",
    "HTTPBasedPolicy": {
        "HostedAddress": "Address",
        "Exceptions": [
            {
                "paths": ["path_1", "path_2"],  # note here
                "op": "and",
                "sources": ["source_1", "source_2"],  # note here
                "skip_threats_filter_categories": [  # note here
                    "application_attacks",
                    "sql_injection_attacks",
                ],
                "skipav": "1",
                "skipbadclients": "0",
                "skipcookie": "1",
                "skipform": "0",
                "skipurl": "1"
            }
        ]
    }
}

```

## LocalServiceACL

LocalServiceACLs list both source hosts and destination hosts in the same
list, with different tags. In the JSON reply, these are split into two lists.
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
{
    "RuleName": "acl-rule",
    "SourceZone": "WAN",
    "Hosts": ["host1", "host2"],  # note here
    "DstHosts": ["dsthost3", "dsthost4"],  # note here
}
```
