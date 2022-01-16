from __future__ import annotations

from xml.etree.ElementTree import Element

from .api_factory import JsonData
from .api_factory import xml_to_json


class Response:
    def __init__(self, response_elem: Element) -> None:
        self.data: JsonData = {}
        self.status_code = 0
        self.original_request = response_elem.get("transactionid")

        # check for errors
        if response_elem.tag == "Status":
            self.status_code = int(response_elem.get("code"))
            self.data["message"] = response_elem.text
            return

        # check for Login status
        if response_elem.tag == "Login":
            if response_elem.find("./status").text == "Authentication Failure":
                self.status_code = 401  # unofficial: to indicate unauthorized
                self.data["message"] = (
                    "Authentication Failure: Can be either incorrect "
                    "username/password, user not an administrator, MFA is "
                    "required, or password is plaintext but not marked as "
                    "`is_encrypted = False` in Client(...) definition."
                )
                return
            else:
                self.status_code = 200  # unofficial: to indicate successful auth  # noqa: E501
                auth_success = response_elem.find("./status").text
                assert auth_success == "Authentication Successful"
                self.data["message"] = auth_success
                return

        # Check for return data
        if self.original_request.startswith("get"):  # eg get_zones
            self.data = xml_to_json(response_elem)
            self.status_code = 200

        else:  # set, add, update, remove
            status = response_elem.find("./Status")
            self.data["message"] = status.text
            self.status_code = int(status.get("code"))
