from __future__ import annotations

from xml.etree.ElementTree import Element

from defusedxml import ElementTree as ET  # type: ignore

from .api_factory import _create_element
from .api_factory import _make_filter
from .api_factory import Filter
from .api_factory import json_to_xml


class Request:
    def __init__(self, apiversion: str = "") -> None:
        self.request = _create_element("Request")
        self.request.set("APIVersion", apiversion)

        self._get = _create_element("Get")
        self._set = _create_element("Set")
        self._add = _create_element("Set")
        self._add.set("operation", "add")
        self._update = _create_element("Set")
        self._update.set("operation", "update")
        self._remove = _create_element("Remove")

        self.request.append(self._get)
        self.request.append(self._set)
        self.request.append(self._add)
        self.request.append(self._update)
        self.request.append(self._remove)

    def __str__(self) -> str:
        return ET.tostring(self.request).decode("utf-8")

    def set_login(self, login: Element) -> None:
        self.request.insert(0, login)

    # GENERIC METHODS
    def get(self, entity: str) -> None:
        elem = _create_element(entity, transactionid=f"get_{entity}s")
        self._get.append(elem)

    def get_filter(self, entity: str, type: Filter, name: str) -> None:
        elem = _create_element(
            entity, transactionid=f"get_{entity}_{type.name}"
        )
        filter_elem = _make_filter(type, name)
        elem.append(filter_elem)
        self._get.append(elem)

    def set(self, entity: str, data: dict) -> None:
        elem = json_to_xml(entity, data)
        elem.set("transactionid", f"set_{entity}")
        self._set.append(elem)

    def add(self, entity: str, data: dict) -> None:
        elem = json_to_xml(entity, data)
        elem.set("transactionid", f"set_{entity}")
        self._add.append(elem)

    def update(self, entity: str, data: dict) -> None:
        elem = json_to_xml(entity, data)
        elem.set("transactionid", f"set_{entity}")
        self._update.append(elem)

    def remove(self, entity: str, name: str) -> None:
        elem = json_to_xml(entity, {"Name": name})
        elem.set("transactionid", f"remove_{entity}")
        self._remove.append(elem)

    # ZONES
    def get_zones(self) -> None:
        self.get("Zone")

    def get_zone(self, name: str) -> None:
        self.get_filter("Zone", Filter.EQUAL, name)

    def get_zones_like(self, name: str) -> None:
        self.get_filter("Zone", Filter.LIKE, name)

    def get_zones_except(self, name: str) -> None:
        self.get_filter("Zone", Filter.EXCEPT, name)

    def set_zone(self, data: dict) -> None:
        self.set("zone", data)

    def add_zone(self, data: dict) -> None:
        self.add("zone", data)

    def update_zone(self, data: dict) -> None:
        self.update("zone", data)

    def remove_zone(self, name: str) -> None:
        self.remove("zone", name)
