from __future__ import annotations


class Request:
    def __init__(self):
        pass

    # set functions
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

    # get functions
    def _get_host(self):
        # generic call to create the required transaction
        # add the transaction to the request.
        pass

    def get_all_hosts(self):
        # get all hosts (?)
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
