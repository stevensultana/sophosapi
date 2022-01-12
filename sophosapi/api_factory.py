from xml.etree.ElementTree import Element

tags_of_lists = ("SourceNetworks",)


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


def xml_to_json(elem: Element):
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
