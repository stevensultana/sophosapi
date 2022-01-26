tags_of_lists = {
    "AccessPaths": "AccessPath",  # FirewallRule/HTTPBasedPolicy
    "AccessPoints": "AccessPoint",  # WirelessGrouping
    # "AccessPoints": "MeshNetwork",  # WirelessMeshNetworks
    "AddressList": "Address",  # DNSHostEntry
    "AdminAccessNodeList": "IPAddress",  # User
    "allowed_networks": "allowed_networks",  # invented for FirewallRule/HTTPBasedPolicy/AccessPaths/AccessPath
    "AllowedNetworks": "Network",  # SPXConfiguration
    "AllowedUser": "User",  # VPNIPSecConnection
    "AllowedUsers": "User",  # SophosConnectClient
    "AllowedZone": "Zone",  # WirelessProtectionGlobalSettings
    "ApplicationList": "Application",  # ApplicationFilterPolicy
    "ApplicationObjects": "ApplicationObject",  # SDWANPolicyRoute
    "Assets": "Asset",  # FormTemplate
    "AuthenticationServerList": "AuthenticationServer",  # FirewallAuthentication, AdminAuthentication
    "backends": "backend",  # invented for FirewallRule/HTTPBasedPolicy/AccessPaths/AccessPath
    "BlockedEmailAddresses": "EmailAddress",  # MtaBlockedSenders
    "BlockFileTypes": "FileType",  # AntiVirusMailSMTPScanningRules, SMTPPolicy
    "BookmarkList": "Bookmark",  # SSLBookmarkGroup
    "BridgeMembers": "Member",  # BridgePair
    "CategoryList": "Category",  # ApplicationFilterPolicy, IPSPolicy, WebFilterPolicy
    "CCLList": "CCL",  # WebFilterPolicy
    "CharacteristicsList": "Characteristics",  # ApplicationFilterPolicy
    "ClassificationList": "Classification",  # ApplicationFilterPolicy
    "ContentList": "ContentString",  # ContentConditionList
    "CountryList": "Country",  # CountryGroup
    "CustomNTPServer": "NTPServer",  # Time
    "denied_networks": "denied_networks",  # invented for FirewallRule/HTTPBasedPolicy/AccessPaths/AccessPath
    "DestinationInterfaceList": "DestinationInterface",  # MulticastRoute
    "DestinationNetworks": "Network",  # various
    "DestinationZones": "Zone",  # various
    # "DomainList": "Domain",  # WebFilterCategory
    "DomainList": "DomainName",  # AntiSpamTrustedDomain
    # "DomainList": ??,  # WebFilterException
    "Domains": "Domain",  # FirewallRule/HTTPBasedPolicy, REDDevice
    "DstHosts": "DstHost",  # invented for LocalServiceACL - handled as a special case in xml_to_json and json_to_xml
    "EmailList": "EmailID",  # User
    "EnableOnZone": "Zone",  # SpoofPrevention
    "EntryURLList": "EntryURL",  # ProtocolSecurity
    "EtherTypeList": "EtherType",  # BridgePair
    "ExceptionNetworks": "Network",  # FirewallRule/HTTPBasedPolicy
    "Exceptions": "Exception",  # FirewallRule/HTTPBasedPolicy
    "FailoverCondition": "FailoverIF",  # VPNFailoverGroup
    "FileExtensionList": "FileExtension",  # FileType
    "FQDNHostGroupList": "FQDNHostGroup",  # FQDNHost
    "FQDNHostList": "FQDNHost",  # FQDNHostGroup
    "Gateways": "Gateway",  # invented for GatewayConfiguration
    "GroupIP": "IPAddress",  # PIMDynamicRouting
    "HostException": "Host",  # ATP
    "HostGroupList": "HostGroup",  # IPHost
    "HostList": "Host",  # IPHostGroup
    "Hosts": "Host",  # LocalServiceACL
    "HostsOrNetworks": "HostsOrNetwork",  # RelaySettings
    "Identity": "Member",  # FirewallRule/UserPolicy
    # "Identity": "Members",  # SSLTLSInspectionRule - handled as a special case in json_to_xml
    "InboundInterfaces": "Interface",  # NATRule
    "InitializationStrings": "String",  # CellularWAN
    "InterfaceList": "Interface",  # SchedulebasedPolicyRuleList, PIMDynamicRouting
    "InterfaceNATPolicyList": "Override",  # NATRule
    "Interfaces": "Interface",  # Hotspot
    "IPLease": "IP",  # DHCPServer, DHCPServerIpv6
    "KeywordList": "Keyword",  # WebFilterCategory
    "LocalNetworks": "Network",  # SiteToSiteServer
    "MACAddressList": "MACAddress",  # User
    "MemberConnections": "Connection",  # VPNFailoverGroup
    "MemberInterface": "Interface",  # LAG
    "MeshNetwoks": "MeshNetwok",  # WirelessAccessPoint - yes, with a typo
    "MIMEHeaderList": "MIMEHeader",  # FileType
    "MIMEWhiteList": "WhiteList",  # SMTPPolicy
    "MonitoringCondition": "Rule",  # GatewayHost
    "MonitorPorts": "Interface",  # HAConfigure
    "NetworkExceptions": "Host",  # WAFSlowHTTP
    "Networks": "Network",  # REDDevice
    "NodeList": "IPAddress",  # User, UserGroup
    "OriginalDestinationNetworks": "Network",  # NATRule
    "OriginalServices": "Service",  # NATRule
    "OriginalSourceNetworks": "Network",  # NATRule
    "OutboundInterfaces": "Interface",  # NATRule
    "paths": "path",  # invented for FirewallRule/HTTPBasedPolicy/Exceptions/Exception
    "PeerAdministrationList": "PeerConfiguration",  # HAConfigure
    "PermittedNetworkResourcesIPv4": "Resource",  # SophosConnectClient, SSLVPNPolicy
    "PermittedNetworkResourcesIPv6": "Resource",  # SSLVPNPolicy
    "PlatformList": "Platform",  # IPSPolicy
    "PolicyMembers": "Member",  # SSLVPNPolicy
    "PrefixAdvertisementConfiguration": "PrefixAdvertisementConfiguration",  # RouterAdvertisement
    "PUAWhitelist": "PUA",  # WebFilterProtectionSettings, WebFilterSettings
    "RBLList": "RBLName",  # SMTPPolicy
    "ReceiverList": "Receiver",  # AntiVirusMailSMTPScanningRules
    "RecipientAddresses": "Address",  # ExceptionPolicy
    "RecipientHeaders": "Header",  # EmailConfiguration
    "RefferredDomains": "Domains",  # SSLBookmark
    "RemoteLANNetwork": "Network",  # L2TPConnection
    "RemoteNetworks": "Network",  # SiteToSiteServer
    "RequestParamterList": "RequestParamter",  # SMSGateway - yes, with a typo
    "ResponseParamterList": "RequestParamter",  # SMSGateway - yes, with a typo
    "RiskList": "Risk",  # ApplicationFilterPolicy
    "RouteList": "HostName",  # SMTPPolicy
    "RuleList": "Rule",  # ApplicationFilterPolicy, IPSPolicy, WebFilterPolicy
    "Rules": "Rule",  # invented for GatewayConfiguration
    "SchedulebasedPolicyRuleList": "Rule",  # QOSPolicy
    "ScheduleDetails": "ScheduleDetail",  # Schedule
    "SearchQueries": "Query",  # AuthenticationServer
    "SecurityPolicyList": "SecurityPolicy",  # FirewallRuleGroup
    "SenderAddressesList": "Address",  # ExceptionPolicy
    "SenderList": "Sender",  # AntiVirusMailSMTPScanningRules
    "ServiceList": "Service",  # ServiceGroup
    "Services": "Service",  # various
    "ServiceDetails": "ServiceDetail",  # Services
    "SeverityList": "Severity",  # IPSPolicy
    "Signatures": "Signature",  # MTADataControlList
    "skip_threats_filter_categories": "skip_threats_filter_categories",  # invented for FirewallRule/HTTPBasedPolicy/Exceptions/Exception
    "SkipFilterRules": "FilterRules",  # ProtocolSecurity
    "SmarthostList": "Hostname",  # SmarthostSettings
    "sources": "source",  # invented for FirewallRule/HTTPBasedPolicy/Exceptions/Exception
    "SourceHostList": "SourceHost",  # ExceptionPolicy
    "SourceNetworks": "Network",  # various
    "SourceZones": "Zone",  # various
    "SSLVPNAuthenticationServerList": "AuthenticationServer",  # SSLVPNAuthentication
    "SSORadiusAccount": "Radius",  # FirewallAuthentication
    "StaticLease": "Lease",  # DHCPServer, DHCPServerIpv6
    "SupportedDHGroups": "DHGroup",  # VPNPolicy
    "TargetList": "Target",  # IPSPolicy
    "TargetServers": "Host",  # DNSRequestRoute
    "TechnologyList": "Technology",  # ApplicationFilterPolicy
    "ThreatException": "Threat",  # ATP
    "ThreatFilters": "Filter",  # ProtocolSecurity
    "TrustedPorts": "Port",  # WebFilterAdvancedSettings, WebProxy
    "UserList": "User",  # WebFilterPolicy
    "Users": "User",  # various
    "CategoryList": "Category",  # UserActivity
    "UserGroupList": "UserGroup",  # ReverseAuthentication
    "UsersOrGroups": "UsersOrGroup",  # RelaySettings
    "URLList": "URL",  # WebFilterURLGroup, WebFilterCategory
    "Vouchers": "Voucher",  # Hotspot
    "VPNAuthenticationMethods": "VPNAuthenticationServerList",  # VPNAuthentication
    "WalledGarden": "AllowedNetworks",  # AdvancedConfiguration
    "WirelessNetworks": "Network",  # WirelessAccessPoint, WirelessGrouping, WirelessLocalAP
    "Websites": "Activity",  # SSLTLSInspectionRule
}
