from xml.etree.ElementTree import Element


def _create_element(
    elem_name: str,
    *,
    text: str = "",
) -> Element:

    new_element = Element(elem_name)
    new_element.text = text
    return new_element
