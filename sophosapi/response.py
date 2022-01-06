from __future__ import annotations


class Response:
    def __init__(self, full_xml: str):
        # most likely, the full response text will be needed to be parsed
        pass

    def failures(self) -> list[TransactionResponse]:
        # for each transaction response, return just the failures
        # probably good to be a property
        pass


class TransactionResponse:
    def __init__(self):
        # start from the full text of a single transaction response
        # get the status and message text
        pass
