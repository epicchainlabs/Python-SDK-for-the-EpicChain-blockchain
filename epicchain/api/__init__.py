"""
Classes to interact with the network such as a specialised RPC Client for EpicChain Node RPC API and a facade for interacting
 with smart contracts over RPC.
"""
from .noderpc import (
    EpicRpcClient,
    JsonRpcError,
    StackItem,
    StackItemType,
)

__all__ = [
    "EpicRpcClient",
    "JsonRpcError",
    "StackItem",
    "StackItemType",
]
