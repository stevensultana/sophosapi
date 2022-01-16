from __future__ import annotations

from enum import Enum
from typing import Dict
from typing import List
from typing import Union
from xml.etree.ElementTree import Element

tags_of_lists = {
    "SourceZones": "Zone",
    "DestinationZones": "Zone",
    "SourceNetworks": "Network",
    "DestinationNetworks": "Network",
    "Services": "Service",
    # "Identity": "Member",  # for FirewallRule
    # "Identity": "Members",  # SSLTLSInspectionRule
    "ApplicationObjects": "ApplicationObject",
    "Users": "User",
    "Domains": "Domain",
    "ExceptionNetworks": "Network",
    # "AccessPaths": "AccessPath",  # for FirewallRule
    # "AccessPath": "backend",
    # "AccessPath": "allowed_networks",
    # "AccessPath": "denied_networks",
    # "Exceptions": "Exception",
    # "Exception": "path",
    # "Exception": "source",
    # "Exception": "skip_threats_filter_categories",
    "SecurityPolicyList": "SecurityPolicy",
    # "Websites": "Activity",  # SSLTLSInspectionRule
    # "Hosts": "Host / DstHost",  # for LocalServiceACL
    "ServiceDetails": "ServiceDetail",
    "Vouchers": "Voucher",
    "Networks": "Network",
    "RefferredDomains": "Domains",
}


class Filter(Enum):
    EQUAL = "="
    LIKE = "like"
    EXCEPT = "!="


def _create_element(
    elem_name: str,
    *,
    text: str = "",
    transactionid: str = "",
) -> Element:
    """Create the Element:
    <elem_name "transactionid"="id">text</elem_name>
    """
    new_element = Element(elem_name)
    new_element.text = text
    if transactionid != "":
        new_element.set("transactionid", transactionid)
    return new_element


def _make_filter(type: Filter, name: str) -> Element:
    """Create the Element:
    <Filter>
        <key "name"="Name" "criteria"="type.value">name</key>
    </Filter>
    """
    # TODO: sometimes we can filter with something else which is not a name
    # Eg. for IPHost, we cna filter by IPAddress
    filter_elem = _create_element("Filter")
    key_elem = _create_element("key", text=name)
    key_elem.set("name", "Name")
    key_elem.set("criteria", type.value)

    filter_elem.append(key_elem)
    return filter_elem


JsonData = Dict[str, Union[str, List[str], dict]]


def xml_to_json(elem: Element) -> JsonData:
    """Create a dict with "attribute.tag":"text" pairs, or nesting/lists as
    needed
    """
    obj: JsonData = {}
    for attribute in elem:
        if len(attribute) > 0:  # has children
            if attribute.tag in tags_of_lists:  # handle list
                obj[attribute.tag] = [e.text for e in attribute]

            else:  # recurse
                obj[attribute.tag] = xml_to_json(attribute)

        else:
            obj[attribute.tag] = attribute.text
            if obj[attribute.tag] is None:
                obj[attribute.tag] = ""

    return obj


def json_to_xml(entity: str, data: JsonData) -> Element:
    """`entity` is the main item, eg Zone, IPHost, etc.
    `data` is dict of attributes of the entity, eg name, type, description
    """
    elem = Element(entity)
    elem.extend(_json_to_xml(data))
    return elem


def _json_to_xml(data: JsonData) -> list[Element]:
    """Works on the entity data to return a list of elements for each attribute
    It is expected that this list of elements is set to be the children of a
    root entity Element.
    """
    children = []  # to return

    for tag, value in data.items():
        e = Element(tag)
        children.append(e)

        if isinstance(value, str):
            e.text = value

        elif isinstance(value, dict):
            e.extend(_json_to_xml(value))  # recurse

        elif isinstance(value, list):
            sub_children_tag = tags_of_lists[tag]
            sub_children = [
                _create_element(sub_children_tag, text=item) for item in value
            ]
            e.extend(sub_children)

    return children
