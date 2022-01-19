from __future__ import annotations

from enum import Enum
from typing import Dict
from typing import List
from typing import Union
from xml.etree.ElementTree import Element

from .tags_of_lists import tags_of_lists


class Filter(Enum):
    EQUAL = "="
    LIKE = "like"
    EXCEPT = "!="


def _create_element(
    elem_name: str,
    *,
    text: str | None = None,
    transactionid: str | None = None,
) -> Element:
    """Create the Element:
    <elem_name "transactionid"="id">text</elem_name>
    """
    new_element = Element(elem_name)
    if text is not None:
        new_element.text = text
    if transactionid is not None:
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

    if len(elem) == 0:
        return elem.text or ""  # type: ignore

    for attribute in elem:
        if len(attribute) > 0:  # has children

            if attribute.tag == "Hosts":  # special case for LocalServiceACL
                obj["Hosts"] = [e.text for e in attribute.findall("./Host")]
                obj["DstHosts"] = [e.text for e in attribute.findall("./DstHost")]  # noqa: E501

            elif attribute.tag == "AccessPaths":  # special case for WAF Rules
                obj["AccessPaths"] = _handle_FirewallRule_HTTPBasedPolicy_AccessPaths(attribute)

            elif attribute.tag == "Exceptions":  # special case for WAF Rules
                obj["Exceptions"] = _handle_FirewallRule_HTTPBasedPolicy_Exceptions(attribute)

            elif attribute.tag in tags_of_lists:  # handle list
                obj[attribute.tag] = [xml_to_json(e) for e in attribute]  # type: ignore

            else:  # recurse
                obj[attribute.tag] = xml_to_json(attribute)

        else:
            obj[attribute.tag] = attribute.text or ""

    return obj


def json_to_xml(entity: str, data: JsonData) -> Element:
    """`entity` is the main item, eg Zone, IPHost, etc.
    `data` is dict of attributes of the entity, eg name, type, description
    """
    elem = Element(entity)
    elem.extend(_json_to_xml(data))

    if entity == "SSLTLSInspectionRule":
        elem = _handle_SSLTLSInspectionRule_Identity(elem)

    elif entity == "LocalServiceACL":
        elem = _handle_LocalServiceACL_Hosts(elem)

    elif entity == "FirewallRule" and elem.find("./HTTPBasedPolicy"):
        elem = _handle_FirewallRule_HTTPBasedPolicy(elem)

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
            sub_children = []
            sub_children_tag = tags_of_lists[tag]
            for sub_child in value:
                sub_child_elem = _create_element(sub_children_tag)
                if isinstance(sub_child, str):
                    sub_child_elem.text = sub_child

                elif isinstance(sub_child, dict):
                    sub_child_elem.extend(_json_to_xml(sub_child))
                sub_children.append(sub_child_elem)
            e.extend(sub_children)

    return children


# json_to_xml special cases
def _handle_SSLTLSInspectionRule_Identity(elem: Element) -> Element:
    # json_to_xml special case
    for e in elem.findall(".//Identity/Member"):
        e.tag = "Members"

    return elem


def _handle_LocalServiceACL_Hosts(elem: Element) -> Element:
    # json_to_xml special case
    dsthosts = elem.find(".//DstHosts")
    if dsthosts is not None:
        hosts = elem.find(".//Hosts") or Element("Hosts")
        hosts.extend(dsthosts)
        elem.remove(dsthosts)

    return elem


def _handle_FirewallRule_HTTPBasedPolicy(elem: Element) -> Element:
    # json_to_xml special case
    access_paths = elem.find("./HTTPBasedPolicy/AccessPaths")
    if access_paths is not None:
        for access_path in access_paths:
            backends = access_path.find("./backends")
            if backends is not None:
                access_path.extend(backends)
                access_path.remove(backends)

            allowed_networks = access_path.find("./allowed_networks")
            if allowed_networks is not None:
                access_path.extend(allowed_networks)
                access_path.remove(allowed_networks)

            denied_networks = access_path.find("./denied_networks")
            if denied_networks is not None:
                access_path.extend(denied_networks)
                access_path.remove(denied_networks)

    exceptions = elem.find("./HTTPBasedPolicy/Exceptions")
    if exceptions is not None:
        for exception in exceptions:
            paths = exception.find("./paths")
            if paths is not None:
                exception.extend(paths)
                exception.remove(paths)

            sources = exception.find("./sources")
            if sources is not None:
                exception.extend(sources)
                exception.remove(sources)

            stfc = exception.find("./skip_threats_filter_categories")
            if stfc is not None:
                exception.extend(stfc)
                exception.remove(stfc)

    return elem


# xml_to_json special cases
def _handle_FirewallRule_HTTPBasedPolicy_AccessPaths(AccessPaths: Element) -> list:  # noqa: E501
    # xml_to_json special case
    access_path_list = []
    for AccessPath in AccessPaths.findall("./AccessPath"):
        obj: JsonData = {}

        for attribute in AccessPath:
            if attribute.tag == "backend":
                if "backends" not in obj:
                    obj["backends"] = []
                obj["backends"].append(attribute.text)  # type: ignore

            elif attribute.tag == "allowed_networks":
                if "allowed_networks" not in obj:
                    obj["allowed_networks"] = []
                obj["allowed_networks"].append(attribute.text)  # type: ignore

            elif attribute.tag == "denied_networks":
                if "denied_networks" not in obj:
                    obj["denied_networks"] = []
                obj["denied_networks"].append(attribute.text)  # type: ignore

            else:
                obj[attribute.tag] = attribute.text or ""

        access_path_list.append(obj)

    return access_path_list


def _handle_FirewallRule_HTTPBasedPolicy_Exceptions(Exceptions: Element) -> list:  # noqa: E501
    # xml_to_json special case
    exception_list = []
    for Exception in Exceptions.findall("./Exception"):
        obj: JsonData = {}

        for attribute in Exception:
            if attribute.tag == "path":
                if "paths" not in obj:
                    obj["paths"] = []
                obj["paths"].append(attribute.text)  # type: ignore

            elif attribute.tag == "source":
                if "sources" not in obj:
                    obj["sources"] = []
                obj["sources"].append(attribute.text)  # type: ignore

            elif attribute.tag == "skip_threats_filter_categories":
                if "skip_threats_filter_categories" not in obj:
                    obj["skip_threats_filter_categories"] = []
                obj["skip_threats_filter_categories"].append(attribute.text)  # type: ignore

            else:
                obj[attribute.tag] = attribute.text or ""

        exception_list.append(obj)

    return exception_list
