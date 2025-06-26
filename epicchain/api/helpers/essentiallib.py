"""
This module holds helper functions for data that has been serialized using the EssentialLib native contract
"""

from epicchain import vm
from typing import NamedTuple, cast, Any
from epicchain.core import serialization, types


class PlaceHolder(NamedTuple):
    type: vm.StackItemType
    count: int  # type: ignore


def binary_deserialize(data: bytes):
    """
    Deserialize data that has been serialized using EssentialLib.serialize()

    This is the equivalent of the EssentialLib.deserialize()
    and can be used to deserialize data from smart contract storage that was serialized when stored.
    """
    max_size = 0xFFFF * 2
    if len(data) == 0:
        raise ValueError("Nothing to deserialize")

    deserialized: list[Any | PlaceHolder] = []
    to_deserialize = 1
    with serialization.BinaryReader(data) as reader:
        while not to_deserialize == 0:
            to_deserialize -= 1
            item_type = vm.StackItemType(reader.read_byte()[0])
            if item_type == vm.StackItemType.ANY:
                deserialized.append(None)
            elif item_type == vm.StackItemType.BOOLEAN:
                deserialized.append(reader.read_bool())
            elif item_type == vm.StackItemType.INTEGER:
                deserialized.append(int(types.BigInteger(reader.read_var_bytes(32))))
            elif item_type in [vm.StackItemType.BYTESTRING, vm.StackItemType.BUFFER]:
                deserialized.append(reader.read_var_bytes(len(data)))
            elif item_type in [vm.StackItemType.ARRAY, vm.StackItemType.STRUCT]:
                count = reader.read_var_int(max_size)
                deserialized.append(PlaceHolder(item_type, count))
                to_deserialize += count
            elif item_type == vm.StackItemType.MAP:
                count = reader.read_var_int(max_size)
                deserialized.append(PlaceHolder(item_type, count))
                to_deserialize += count * 2
            else:
                raise ValueError("unreachable")

    temp: list = []
    while len(deserialized) > 0:
        item = deserialized.pop()
        if type(item) == PlaceHolder:
            item = cast(PlaceHolder, item)
            if item.type == vm.StackItemType.ARRAY:
                array = []
                for _ in range(0, item.count):
                    array.append(temp.pop())
                temp.append(array)
            elif item.type == vm.StackItemType.STRUCT:
                struct = []
                for _ in range(0, item.count):
                    struct.append(temp.pop())
                temp.append(struct)
            elif item.type == vm.StackItemType.MAP:
                m = dict()
                for _ in range(0, item.count):
                    k = temp.pop()
                    v = temp.pop()
                    m[k] = v
                temp.append(m)
        else:
            temp.append(item)
    return temp.pop()
