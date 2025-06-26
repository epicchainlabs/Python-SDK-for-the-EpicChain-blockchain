"""
    This version of the contract has an `add` method that increases the value by 1.
"""
from typing import Any
from viper.builtin import EpicChainMetadata, metadata, public
from viper.builtin.nativecontract.contractmanagement import ContractManagement


@metadata
def manifest_metadata() -> EpicChainMetadata:
    """
    Defines this smart contract's metadata information.
    """
    meta = EpicChainMetadata()
    meta.name = "Example Contract"
    return meta


@public(safe=False)
def update(xef_file: bytes, manifest: bytes, data: Any = None):
    ContractManagement.update(xef_file, manifest, data)


@public
def add(number: int) -> int:
    return number + 1


@public(safe=False)
def destroy():
    ContractManagement.destroy()
