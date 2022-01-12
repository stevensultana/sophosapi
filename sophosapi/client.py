from __future__ import annotations

import ssl  # noqa: F401
import urllib.parse  # noqa: F401
from urllib.request import urlopen  # noqa: F401
from xml.etree.ElementTree import Element

from defusedxml import ElementTree as ET

from .api_factory import _create_element
from .request import Request
from .response import Response


class Client:
    """
    Interfaces with the Sophos XG API server.
    """

    def __init__(
        self,
        *,
        username: str,
        password: str,
        is_encrypted: bool = True,
        server: str,
        port: int = 4444,
    ):
        self.username = username
        self.password = password
        self.is_encrypted = is_encrypted
        self.server = server
        self.port = port

    def get_login_tag(self) -> Element:
        login = _create_element("Login")
        login_username = _create_element("Username", text=self.username)
        login_password = _create_element("Password", text=self.password)
        if self.is_encrypted:
            login_password.set("passwordform", "encrypt")
        # else inform the user how to encrypt their password

        login.append(login_username)
        login.append(login_password)

        return login

    def _request_proxy_call(self, fn_name, *args, **kwargs):
        request = Request(apiversion="1805.2")
        getattr(request, fn_name)(args, kwargs)

        response = self.send(request)
        return response

    def get_zones(self):
        # returns a list of Zones
        return self._request_proxy_call("get_zones")

    def set_host(self, *args, **kwargs):
        # returns the result of the set command - single element
        return self._request_proxy_call("set_host", args, kwargs)[0]

    def send(self, request: Request) -> Response:
        # request.set_login(self.get_login_tag())
        # req_str = urllib.parse.quote(str(request))
        # # try
        # response_http = urlopen(
        #     f"https://{self.server}:{self.port}/webconsole/APIController?reqxml={req_str}"  # noqa: E501
        # )
        #
        # response_element = ET.fromstring(response_http.read())
        mock_reponse = """
<Response>

<Login>
    <status>Authentication Successful</status>
</Login>

<Zone transactionid="get_zones">
    <Name>RED</Name>
    <Type>DMZ</Type>
    <Description />
    <SourceNetworks>
      <Network>Net_01</Network>
      <Network>Net_02</Network>
      <Network>Net_03</Network>
    </SourceNetworks>
</Zone>

<Zone transactionid="get_zones">
    <Name>LAN</Name>
    <Type>LAN</Type>
    <Description>Some description</Description>
    <SourceNetworks>
      <Network>Net_04</Network>
      <Network>Net_05</Network>
    </SourceNetworks>
</Zone>

</Response>
        """
        response_element = ET.fromstring(mock_reponse)

        responses = self._parse_response(response_element)

        return responses

    def _parse_response(self, response_element: Element):
        responses = [Response(e) for e in response_element]

        # don't need to store the Successful Authentication response:
        login_response = next(
            (
                r
                for r in responses
                if r.data["message"] == "Authentication Successful"
            ),
            None,
        )
        if login_response is not None:
            responses.remove(login_response)

        # for each response:
        #     find corresponding request using transactionid
        #     set a reference to the request in the response
        return responses
