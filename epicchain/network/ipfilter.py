""" A module for filtering IPs via black and whitelists on P2P nodes (`EpicChainNode`).

A global instance ``ipfilter`` can be imported directly from the module and is taken into account by default in the
`EpicChainNode` class when connections are established.
"""
from ipaddress import IPv4Network
from contextlib import suppress
from copy import deepcopy


class IPFilter:
    """
    Filtering rules.

    * The whitelist has precedence over the blacklist settings.
    * Host masks can be applied.
    * When using host masks do not set host bits (leave them to 0) or an exception will occur.

    The following are `configuration` examples for common scenario's.

    1. Accept only specific trusted IPs.

            {
                'blacklist': [
                    '0.0.0.0/0'
                ],
                'whitelist': [
                    '10.10.10.10',
                    '15.15.15.15'
                ]
            }

    2. Accept only a range of trusted IPs.

            # Accepts any IP in the range of 10.10.10.0 - 10.10.10.255

            {
                'blacklist': [
                    '0.0.0.0/0'
                ],
                'whitelist': [
                    '10.10.10.0/24',
                ]
            }

    3. Accept all except specific IPs.

            # Can be used for banning bad actors

            {
                'blacklist': [
                    '12.12.12.12',
                    '13.13.13.13'
                ],
                'whitelist': [
                ]
            }
    """

    default_config: dict = {"blacklist": [], "whitelist": []}

    def __init__(self):
        self._config = deepcopy(self.default_config)

    def is_allowed(self, address: str) -> bool:
        """
        Test if a given address passes the configured restrictions.

        Args:
            address: an IPv4 address as defined in the :py:class:`standard library <python:ipaddress.IPv4Network>`.
        """
        ipv4_address = IPv4Network(address)

        is_allowed = True

        for ip in self._config["blacklist"]:
            disallowed = IPv4Network(ip)
            if disallowed.overlaps(ipv4_address):
                is_allowed = False
                break
        else:
            return is_allowed

        # can override blacklist
        for ip in self._config["whitelist"]:
            allowed = IPv4Network(ip)
            if allowed.overlaps(ipv4_address):
                is_allowed = True

        return is_allowed

    def blacklist_add(self, address: str) -> None:
        """
        Add an address that will not pass restriction checks.

        Args:
            address: an IPv4 address as defined in the :py:class:`standard library <python:ipaddress.IPv4Network>`.
        """
        self._config["blacklist"].append(address)

    def blacklist_remove(self, address: str) -> None:
        """
        Remove an address from the blacklist.

        Args:
            address: an IPv4 address as defined in the :py:class:`standard library <python:ipaddress.IPv4Network>`.
        """
        with suppress(ValueError):
            self._config["blacklist"].remove(address)

    def whitelist_add(self, address: str) -> None:
        """
        Add an address that will pass restriction checks.

        Args:
            address: an IPv4 address as defined in the :py:class:`standard library <python:ipaddress.IPv4Network>`.
        """
        self._config["whitelist"].append(address)

    def whitelist_remove(self, address: str) -> None:
        """
        Remove an address from the whitelist.

        Args:
            address: an IPv4 address as defined in the :py:class:`standard library <python:ipaddress.IPv4Network>`.
        """
        with suppress(ValueError):
            self._config["whitelist"].remove(address)

    def load_config(self, config: dict[str, list[str]]) -> None:
        """
        Load filtering rules from a configuration object.

        Args:
            config: a _dictionary holding 2 keys, `blacklist` & `whitelist`, each  having a
                    :py:class:`list <python:list>` type value holding :py:class:`str <python:str>` type ``address`` es.
                    See :ref:`IPFilter examples`. For ``address`` format refer to the
                    :py:class:`standard library <python:ipaddress.IPv4Network>`.
        Raises:
            ValueError: if the required config keys are not found.
        """
        if "whitelist" not in config:
            raise ValueError("whitelist key not found")
        if "blacklist" not in config:
            raise ValueError("blacklist key not found")
        self._config = config

    def reset(self) -> None:
        """
        Clear the filter rules.
        """
        self._config = deepcopy(self.default_config)


ipfilter = IPFilter()
