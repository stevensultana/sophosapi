from enum import Enum
from xml.etree.ElementTree import Element

tags_of_lists = ("SourceNetworks",)


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

    new_element = Element(elem_name)
    new_element.text = text
    new_element.set("transactionid", transactionid)
    return new_element


def _make_filter(type: Filter, name: str) -> Element:
    filter_elem = _create_element("Filter")
    key_elem = _create_element("key", text=name)
    key_elem.set("name", "Name")
    key_elem.set("criteria", type.value)

    filter_elem.append(key_elem)
    return filter_elem


def xml_to_json(elem: Element) -> dict:
    obj = {}
    for attribute in elem:
        if len(attribute) > 0:  # has children
            if attribute.tag in tags_of_lists:
                # handle list
                obj[attribute.tag] = [e.text for e in attribute]

            else:
                obj[attribute.tag] = xml_to_json(attribute)

        else:
            obj[attribute.tag] = attribute.text
            if obj[attribute.tag] is None:
                obj[attribute.tag] = ""

    return obj
