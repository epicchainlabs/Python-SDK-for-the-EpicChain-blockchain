from epicchain.core import serialization
from epicchain.core.serialization import BinaryReader, BinaryWriter


class SerializableObject(serialization.ISerializable):
    def serialize(self, writer: BinaryWriter) -> None:
        pass

    def deserialize(self, reader: BinaryReader) -> None:
        pass

    def __len__(self):
        return 0
