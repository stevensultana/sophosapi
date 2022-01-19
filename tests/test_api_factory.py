import pytest
from defusedxml import ElementTree as ET

from sophosapi.api_factory import _create_element
from sophosapi.api_factory import json_to_xml
from sophosapi.api_factory import xml_to_json


def element_equality(e1, e2):
    if e1.tag != e2.tag:
        return False
    if e1.text != e2.text:
        return False
    if len(e1) != len(e2):
        return False

    # recurse
    e2_copy = list(e2)
    for sub1 in e1:
        for sub2 in e2_copy:
            if element_equality(sub1, sub2):
                e2_copy.remove(sub2)
                break
        else:
            return False
    return True


def test_create_element():
    # Practically testing that the standard library's Element class works
    element = _create_element("MyTag")
    assert ET.tostring(element) == b"<MyTag />"

    element = _create_element("MyTag", text="")
    assert ET.tostring(element) == b"<MyTag />"

    element = _create_element("MyTag", text="MyText")
    assert ET.tostring(element) == b"<MyTag>MyText</MyTag>"


@pytest.mark.parametrize(
    "xml_string, expected",
    [
        (
            """
            <IPHost>
                <Name>name</Name>
                <HostType>IP</HostType>
                <IPAddress>1.1.1.1</IPAddress>
            </IPHost>
            """,
            {"Name": "name", "HostType": "IP", "IPAddress": "1.1.1.1"},
        ),
        (
            """
            <IPHostGroup>
                <Name>name</Name>
                <HostList>
                    <Host>Hostname1</Host>
                    <Host>Hostname2</Host>
                    <Host>Hostname3</Host>
                    <Host>Hostname4</Host>
                </HostList>
            </IPHostGroup>
            """,
            {
                "Name": "name",
                "HostList": [
                    "Hostname1",
                    "Hostname2",
                    "Hostname3",
                    "Hostname4",
                ],
            },
        ),
        (
            """
            <Interface>
                <Name>Port1-LAN</Name>
                <MTU>1500</MTU>
                <MSS>
                    <OverrideMSS>Enable</OverrideMSS>
                    <MSSValue>1455</MSSValue>
                </MSS>
                <InterfaceSpeed>Auto Negotiate</InterfaceSpeed>
            </Interface>
            """,
            {
                "Name": "Port1-LAN",
                "MTU": "1500",
                "MSS": {"OverrideMSS": "Enable", "MSSValue": "1455"},
                "InterfaceSpeed": "Auto Negotiate",
            },
        ),
        (
            """
            <SSLTLSInspectionRule>
                <Name>Name</Name>
                <Websites>
                    <Activity>
                        <Name>Name1</Name>
                        <Type>Web1 Category</Type>
                    </Activity>
                    <Activity>
                        <Name>Name2</Name>
                        <Type>Web2 Category</Type>
                    </Activity>
                </Websites>
            </SSLTLSInspectionRule>
            """,
            {
                "Name": "Name",
                "Websites": [
                    {
                        "Name": "Name1",
                        "Type": "Web1 Category",
                    },
                    {
                        "Name": "Name2",
                        "Type": "Web2 Category",
                    },
                ],
            },
        ),
        (
            """
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
            """,
            {
                "RuleName": "acl-rule",
                "SourceZone": "WAN",
                "Hosts": ["host1", "host2"],
                "DstHosts": ["dsthost3", "dsthost4"],
            },
        ),
        (
            """
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
                        <AccessPath>
                            <path>/access2</path>
                            <backend>b12</backend>
                            <backend>b22</backend>
                            <auth_profile>auth_prof2</auth_profile>
                            <allowed_networks>a12</allowed_networks>
                            <allowed_networks>a22</allowed_networks>
                            <denied_networks>d12</denied_networks>
                            <denied_networks>d22</denied_networks>
                            <stickysession_status>12</stickysession_status>
                            <hot_standby>12</hot_standby>
                            <websocket_passthrough>12</websocket_passthrough>
                            </AccessPath>
                    </AccessPaths>
                </HTTPBasedPolicy>
            </FirewallRule>
            """,
            {
                "Name": "rulename",
                "HTTPBasedPolicy": {
                    "HostedAddress": "Address",
                    "AccessPaths": [
                        {
                            "path": "/access",
                            "backends": ["b1", "b2"],
                            "auth_profile": "auth_prof",
                            "allowed_networks": ["a1", "a2"],
                            "denied_networks": ["d1", "d2"],
                            "stickysession_status": "1",
                            "hot_standby": "1",
                            "websocket_passthrough": "1",
                        },
                        {
                            "path": "/access2",
                            "backends": ["b12", "b22"],
                            "auth_profile": "auth_prof2",
                            "allowed_networks": ["a12", "a22"],
                            "denied_networks": ["d12", "d22"],
                            "stickysession_status": "12",
                            "hot_standby": "12",
                            "websocket_passthrough": "12",
                        },
                    ],
                },
            },
        ),
        (
            """
            <FirewallRule>
                <Name>rulename</Name>
                <HTTPBasedPolicy>
                    <HostedAddress>Address</HostedAddress>
                    <Exceptions>
                        <Exception>
                            <path>psql1</path>
                            <path>abcd1</path>
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
                        <Exception>
                            <path>psql2</path>
                            <path>abcd2</path>
                            <op>or</op>
                            <source>source_3</source>
                            <source>source_4</source>
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
            """,
            {
                "Name": "rulename",
                "HTTPBasedPolicy": {
                    "HostedAddress": "Address",
                    "Exceptions": [
                        {
                            "paths": ["psql1", "abcd1"],
                            "op": "and",
                            "sources": ["source_1", "source_2"],
                            "skip_threats_filter_categories": [
                                "application_attacks",
                                "sql_injection_attacks",
                            ],
                            "skipav": "1",
                            "skipbadclients": "0",
                            "skipcookie": "1",
                            "skipform": "0",
                            "skipurl": "1",
                        },
                        {
                            "paths": ["psql2", "abcd2"],
                            "op": "or",
                            "sources": ["source_3", "source_4"],
                            "skip_threats_filter_categories": [
                                "application_attacks",
                                "sql_injection_attacks",
                            ],
                            "skipav": "1",
                            "skipbadclients": "0",
                            "skipcookie": "1",
                            "skipform": "0",
                            "skipurl": "1",
                        },
                    ],
                },
            },
        ),
    ],
    ids=[
        "basic",
        "list",
        "nested",
        "list_nested",
        "LocalServiceACL",
        "HTTPBasedPolicy_AccessPaths",
        "HTTPBasedPolicy_Exceptions",
    ],
)
def test_xml_to_json(xml_string, expected):
    elem = ET.fromstring(xml_string)
    output = xml_to_json(elem)

    assert output == expected


@pytest.mark.parametrize(
    "entity, data, expected",
    [
        (
            "IPHost",
            {"Name": "name", "HostType": "IP", "IPAddress": "1.1.1.1"},
            (
                "<IPHost>"
                "<Name>name</Name>"
                "<HostType>IP</HostType>"
                "<IPAddress>1.1.1.1</IPAddress>"
                "</IPHost>"
            ),
        ),
        (
            "IPHostGroup",
            {
                "Name": "name",
                "HostList": [
                    "Hostname1",
                    "Hostname2",
                    "Hostname3",
                    "Hostname4",
                ],
            },
            (
                "<IPHostGroup>"
                "<Name>name</Name>"
                "<HostList>"
                "<Host>Hostname1</Host>"
                "<Host>Hostname2</Host>"
                "<Host>Hostname3</Host>"
                "<Host>Hostname4</Host>"
                "</HostList>"
                "</IPHostGroup>"
            ),
        ),
        (
            "Interface",
            {
                "Name": "Port1-LAN",
                "MTU": "1500",
                "MSS": {"OverrideMSS": "Enable", "MSSValue": "1455"},
                "InterfaceSpeed": "Auto Negotiate",
            },
            (
                "<Interface>"
                "<Name>Port1-LAN</Name>"
                "<MTU>1500</MTU>"
                "<MSS>"
                "<OverrideMSS>Enable</OverrideMSS>"
                "<MSSValue>1455</MSSValue>"
                "</MSS>"
                "<InterfaceSpeed>Auto Negotiate</InterfaceSpeed>"
                "</Interface>"
            ),
        ),
        (
            "SSLTLSInspectionRule",
            {
                "Name": "Name",
                "Websites": [
                    {
                        "Name": "Name1",
                        "Type": "Web1 Category",
                    },
                    {
                        "Name": "Name2",
                        "Type": "Web2 Category",
                    },
                ],
            },
            (
                "<SSLTLSInspectionRule>"
                "<Name>Name</Name>"
                "<Websites>"
                "<Activity>"
                "<Name>Name1</Name>"
                "<Type>Web1 Category</Type>"
                "</Activity>"
                "<Activity>"
                "<Name>Name2</Name>"
                "<Type>Web2 Category</Type>"
                "</Activity>"
                "</Websites>"
                "</SSLTLSInspectionRule>"
            ),
        ),
        (
            "LocalServiceACL",
            {
                "RuleName": "acl-rule",
                "SourceZone": "WAN",
                "Hosts": ["host1", "host2"],
                "DstHosts": ["dsthost3", "dsthost4"],
            },
            (
                "<LocalServiceACL>"
                "<RuleName>acl-rule</RuleName>"
                "<SourceZone>WAN</SourceZone>"
                "<Hosts>"
                "<Host>host1</Host>"
                "<Host>host2</Host>"
                "<DstHost>dsthost3</DstHost>"
                "<DstHost>dsthost4</DstHost>"
                "</Hosts>"
                "</LocalServiceACL>"
            ),
        ),
        (
            "FirewallRule",
            {
                "Name": "rulename",
                "HTTPBasedPolicy": {
                    "HostedAddress": "Address",
                    "AccessPaths": [
                        {
                            "path": "/access",
                            "backends": ["b1", "b2"],
                            "auth_profile": "auth_prof",
                            "allowed_networks": ["a1", "a2"],
                            "denied_networks": ["d1", "d2"],
                            "stickysession_status": "1",
                            "hot_standby": "1",
                            "websocket_passthrough": "1",
                        },
                        {
                            "path": "/access2",
                            "backends": ["b12", "b22"],
                            "auth_profile": "auth_prof2",
                            "allowed_networks": ["a12", "a22"],
                            "denied_networks": ["d12", "d22"],
                            "stickysession_status": "12",
                            "hot_standby": "12",
                            "websocket_passthrough": "12",
                        },
                    ],
                },
            },
            (
                "<FirewallRule>"
                "<Name>rulename</Name>"
                "<HTTPBasedPolicy>"
                "<HostedAddress>Address</HostedAddress>"
                "<AccessPaths>"
                "<AccessPath>"
                "<path>/access</path>"
                "<backend>b1</backend>"
                "<backend>b2</backend>"
                "<auth_profile>auth_prof</auth_profile>"
                "<allowed_networks>a1</allowed_networks>"
                "<allowed_networks>a2</allowed_networks>"
                "<denied_networks>d1</denied_networks>"
                "<denied_networks>d2</denied_networks>"
                "<stickysession_status>1</stickysession_status>"
                "<hot_standby>1</hot_standby>"
                "<websocket_passthrough>1</websocket_passthrough>"
                "</AccessPath>"
                "<AccessPath>"
                "<path>/access2</path>"
                "<backend>b12</backend>"
                "<backend>b22</backend>"
                "<auth_profile>auth_prof2</auth_profile>"
                "<allowed_networks>a12</allowed_networks>"
                "<allowed_networks>a22</allowed_networks>"
                "<denied_networks>d12</denied_networks>"
                "<denied_networks>d22</denied_networks>"
                "<stickysession_status>12</stickysession_status>"
                "<hot_standby>12</hot_standby>"
                "<websocket_passthrough>12</websocket_passthrough>"
                "</AccessPath>"
                "</AccessPaths>"
                "</HTTPBasedPolicy>"
                "</FirewallRule>"
            ),
        ),
        (
            "FirewallRule",
            {
                "Name": "rulename",
                "HTTPBasedPolicy": {
                    "HostedAddress": "Address",
                    "Exceptions": [
                        {
                            "paths": ["psql1", "abcd1"],
                            "op": "and",
                            "sources": ["source_1", "source_2"],
                            "skip_threats_filter_categories": [
                                "application_attacks",
                                "sql_injection_attacks",
                            ],
                            "skipav": "1",
                            "skipbadclients": "0",
                            "skipcookie": "1",
                            "skipform": "0",
                            "skipurl": "1",
                        },
                        {
                            "paths": ["psql2", "abcd2"],
                            "op": "or",
                            "sources": ["source_3", "source_4"],
                            "skip_threats_filter_categories": [
                                "application_attacks",
                                "sql_injection_attacks",
                            ],
                            "skipav": "1",
                            "skipbadclients": "0",
                            "skipcookie": "1",
                            "skipform": "0",
                            "skipurl": "1",
                        },
                    ],
                },
            },
            (
                "<FirewallRule>"
                "<Name>rulename</Name>"
                "<HTTPBasedPolicy>"
                "<HostedAddress>Address</HostedAddress>"
                "<Exceptions>"
                "<Exception>"
                "<path>psql1</path>"
                "<path>abcd1</path>"
                "<op>and</op>"
                "<source>source_1</source>"
                "<source>source_2</source>"
                "<skip_threats_filter_categories>application_attacks</skip_threats_filter_categories>"
                "<skip_threats_filter_categories>sql_injection_attacks</skip_threats_filter_categories>"
                "<skipav>1</skipav>"
                "<skipbadclients>0</skipbadclients>"
                "<skipcookie>1</skipcookie>"
                "<skipform>0</skipform>"
                "<skipurl>1</skipurl>"
                "</Exception>"
                "<Exception>"
                "<path>psql2</path>"
                "<path>abcd2</path>"
                "<op>or</op>"
                "<source>source_3</source>"
                "<source>source_4</source>"
                "<skip_threats_filter_categories>application_attacks</skip_threats_filter_categories>"
                "<skip_threats_filter_categories>sql_injection_attacks</skip_threats_filter_categories>"
                "<skipav>1</skipav>"
                "<skipbadclients>0</skipbadclients>"
                "<skipcookie>1</skipcookie>"
                "<skipform>0</skipform>"
                "<skipurl>1</skipurl>"
                "</Exception>"
                "</Exceptions>"
                "</HTTPBasedPolicy>"
                "</FirewallRule>"
            ),
        ),
        (
            "FirewallRule",
            {
                "Name": "Name",
                "UserPolicy": {"Identity": ["User_1", "User_2"]},
            },
            (
                "<FirewallRule>"
                "<Name>Name</Name>"
                "<UserPolicy>"
                "<Identity>"
                "<Member>User_1</Member>"
                "<Member>User_2</Member>"
                "</Identity>"
                "</UserPolicy>"
                "</FirewallRule>"
            ),
        ),
        (
            "SSLTLSInspectionRule",
            {"Name": "Name", "Identity": ["User_1", "User_2"]},
            (
                "<SSLTLSInspectionRule>"
                "<Name>Name</Name>"
                "<Identity>"
                "<Members>User_1</Members>"
                "<Members>User_2</Members>"
                "</Identity>"
                "</SSLTLSInspectionRule>"
            ),
        ),
    ],
    ids=[
        "basic",
        "list",
        "nested",
        "list_nested",
        "LocalServiceACL",
        "HTTPBasedPolicy_AccessPaths",
        "HTTPBasedPolicy_Exceptions",
        "FirewallRule_Identity",
        "SSLTLSInspectionRule_Identity",
    ],
)
def test_json_to_xml(entity, data, expected):
    elem = json_to_xml(entity, data)

    assert element_equality(elem, ET.fromstring(expected))
