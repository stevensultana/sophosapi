from __future__ import annotations

from xml.etree.ElementTree import Element

from defusedxml import ElementTree as ET

from .api_factory import _create_element
from .api_factory import _make_filter
from .api_factory import Filter


class Request:
    def __init__(self, apiversion: str = ""):
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

    def __str__(self):
        return ET.tostring(self.request).decode("utf-8")

    def set_login(self, login: Element):
        self.request.insert(0, login)

    # ZONES
    def get_zones(self):
        zone = _create_element("Zone", transactionid="get_zones")
        self._get.append(zone)

    def _get_zone_filter(self, transactionid: str, type: Filter, name: str):
        zone = _create_element("Zone", transactionid=transactionid)
        filter_elem = _make_filter(type, name)
        zone.append(filter_elem)
        self._get.append(zone)

    def get_zone(self, name: str):
        self._get_zone_filter("get_zone_equal", Filter.EQUAL, name)

    def get_zones_like(self, name: str):
        self._get_zone_filter("get_zone_like", Filter.LIKE, name)

    def get_zones_except(self, name: str):
        self._get_zone_filter("get_zone_except", Filter.EXCEPT, name)

    def set_zone(self, *args, **kwargs):
        pass

    def add_zone(self, *args, **kwargs):
        pass

    def update_zone(self, *args, **kwargs):
        pass

    def remove_zone(self, *args, **kwargs):
        pass

    # IPHost
    def set_host(
        self,
        *,
        name: str,
        ipaddress: str,
        ipfamily: str = "IPv4",
        host_group: list[str],
    ):
        # use _create_element() to create the required transaction
        # add the transaction to the request.
        pass

    def _get_host(self):
        # generic call to create the required transaction
        # add the transaction to the request.
        pass

    def get_all_hosts(self):
        # get all hosts
        #   <Get>
        #     <IPHost></IPHost>
        #   </Get>
        # calls _get_host()
        pass

    def get_host(self, name: str):
        # add transaction to get host with exact name (filter =)
        # calls _get_host()
        pass

    def get_hosts_not(self, name: str):
        # add transaction to get all hosts not with name (filter !=)
        # calls _get_host()
        pass

    def get_hosts_like(self, name: str):
        # add transaction to get all hosts with name like (filter like)
        # calls _get_host()
        pass

    # remove functions
    def remove_host(self, name: str):
        # add transaction to remove host with name
        # how does the Sophos API work? List all IPHost names under a single
        # tag? Or have multiple Remove tags?
        pass
