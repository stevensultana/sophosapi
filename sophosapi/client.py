from __future__ import annotations

from typing import TYPE_CHECKING

from .api_factory import _create_element
from .request import Request
from .response import Response

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element


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

    def new_request(self) -> Request:
        # create a new, empty Request object and return it
        pass

    def send(self, request: Request) -> Response:
        # make web call using the request
        # wait for the respone from the server
        # create a Response object using the respone and return it
        pass
