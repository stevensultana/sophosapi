tags_of_lists = {
    "SourceZones": "Zone",  # various
    "DestinationZones": "Zone",
    "SourceNetworks": "Network",
    "DestinationNetworks": "Network",
    "Services": "Service",
    "Identity": "Member",  # for FirewallRule/UserPolicy
    # "Identity": "Members",  # SSLTLSInspectionRule - handled as a special case in json_to_xml
    "ApplicationObjects": "ApplicationObject",
    "Users": "User",
    "Domains": "Domain",  # for FirewallRule/HTTPBasedPolicy
    "ExceptionNetworks": "Network",  # for FirewallRule/HTTPBasedPolicy
    "AccessPaths": "AccessPath",  # for FirewallRule/HTTPBasedPolicy
    "backends": "backend",  # invented for FirewallRule/HTTPBasedPolicy/AccessPaths/AccessPath
    "allowed_networks": "allowed_networks",  # invented for FirewallRule/HTTPBasedPolicy/AccessPaths/AccessPath
    "denied_networks": "denied_networks",  # invented for FirewallRule/HTTPBasedPolicy/AccessPaths/AccessPath
    "Exceptions": "Exception",  # for FirewallRule/HTTPBasedPolicy
    "paths": "path",  # invented for FirewallRule/HTTPBasedPolicy/Exceptions/Exception
    "sources": "source",  # invented for FirewallRule/HTTPBasedPolicy/Exceptions/Exception
    "skip_threats_filter_categories": "skip_threats_filter_categories",  # invented for FirewallRule/HTTPBasedPolicy/Exceptions/Exception
    "SecurityPolicyList": "SecurityPolicy",
    "Websites": "Activity",  # SSLTLSInspectionRule
    "Hosts": "Host",  # for LocalServiceACL
    "DstHosts": "DstHost",  # invented for LocalServiceACL - handled as a special case in xml_to_json and json_to_xml
    "ServiceDetails": "ServiceDetail",
    "Vouchers": "Voucher",
    "Networks": "Network",
    "RefferredDomains": "Domains",
    "HostList": "Host",  # IPHostGroup
    "HostException": "Host",  # ATP
    "TargetServers": "host",  # DNSRequestRoute
    "ScheduleDetails": "ScheduleDetail",  # Schedule
    "ThreatException": "Threat",  # ATP
}
