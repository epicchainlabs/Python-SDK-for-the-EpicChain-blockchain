"""
Smart contract and account contract classes. Contains a list of all native contracts.
"""
from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass
from epicchain.contracts import abi, utils, xef, manifest
from epicchain.core import cryptography, utils as coreutils, types, serialization, Size as s


@dataclass
class _ContractHashes:
    CRYPTO_HIVE = types.UInt160.from_string("0x494c1594ccfa500e9b1fdf567f9e55d8338f3495")
    EPICPULSE_TOKEN = types.UInt160.from_string("0xbc8459660544656355b4f60861c22f544341e828")
    QUANTUMVAULTASSET = types.UInt160.from_string("0x8fd7b7687ff40a5ddd6ea466a8787df2633ed3df")
    MANAGEMENT = types.UInt160.from_string("0xfffdc93764dbaddd97c48f252a53ea4643faa3fd")
    EPICCHAIN_TOKEN = types.UInt160.from_string("0x6dc3bff7b2e6061f3cad5744edf307c14823328e")
    ORACLE_NEXUS = types.UInt160.from_string("0xf95f1e73b6b852e0cdf1535d5371d211707a2d95")
    COVENANTCHAIN = types.UInt160.from_string("0xadd3e350a8789c507686ea677da85d89272f064b")
    QUANTUMGUARDNEXUS = types.UInt160.from_string(
        "0xcffffd77bb491d262eda1056bd976e881fc18142"
    )
    ESSENTIAL_LIB = types.UInt160.from_string("0x410276eb5920d29475c203e04a5015b99c44846a")


#: List of EpicChain's native contract hashes.
CONTRACT_HASHES = _ContractHashes()


class Contract:
    """
    Generic contract.
    """

    def __init__(
        self, script: bytes, parameter_list: Sequence[abi.ContractParameterType]
    ):
        #: The contract instructions (OpCodes)
        self.script = script
        self.parameter_list = parameter_list
        self._script_hash = coreutils.to_script_hash(self.script)
        self._address = None

    @property
    def script_hash(self) -> types.UInt160:
        """
        The contract script hash.
        """
        return self._script_hash

    @classmethod
    def create_multisig_contract(
        cls, m: int, public_keys: Sequence[cryptography.ECPoint]
    ) -> Contract:
        """
        Create a multi-signature contract requiring `m` signatures from the list `public_keys`.

        Args:
            m: minimum number of signature required for signing. Can't be lower than 2.
            public_keys: public keys to use during verification.
        """
        return cls(
            script=utils.create_multisig_redeemscript(m, public_keys),
            parameter_list=[abi.ContractParameterType.SIGNATURE] * m,
        )

    @classmethod
    def create_signature_contract(cls, public_key: cryptography.ECPoint) -> Contract:
        """
        Create a signature contract.

        Args:
            public_key: the public key to use during verification.
        """
        return cls(
            utils.create_signature_redeemscript(public_key),
            [abi.ContractParameterType.SIGNATURE],
        )


class ContractState(serialization.ISerializable):
    """
    Smart contract chain state container.
    """

    def __init__(
        self,
        id_: int,
        xef: xef.XEF,
        manifest_: manifest.ContractManifest,
        update_counter: int,
        hash_: types.UInt160,
    ):
        self.id = id_
        self.xef = xef
        self.manifest = manifest_
        self.update_counter = update_counter
        self.hash = hash_

    def __len__(self):
        return (
            s.uint32  # id
            + len(self.xef.to_array())
            + len(self.manifest)
            + s.uint16  # update counter
            + len(self.hash)
        )

    def __eq__(self, other):
        if other is None:
            return False
        if type(self) != type(other):
            return False
        if self.hash != other.hash:
            return False
        return True

    def __deepcopy__(self, memodict={}):
        return ContractState.deserialize_from_bytes(self.to_array())

    @property
    def script(self) -> bytes:
        """
        XEF script
        """
        return self.xef.script

    @script.setter
    def script(self, value: bytes) -> None:
        self.xef.script = value

    def serialize(self, writer: serialization.BinaryWriter) -> None:
        writer.write_int32(self.id)
        writer.write_serializable(self.xef)
        writer.write_serializable(self.manifest)
        writer.write_uint16(self.update_counter)
        writer.write_serializable(self.hash)

    def deserialize(self, reader: serialization.BinaryReader) -> None:
        self.id = reader.read_int32()
        self.xef = reader.read_serializable(xef.XEF)
        self.manifest = reader.read_serializable(manifest.ContractManifest)
        self.update_counter = reader.read_uint16()
        self.hash = reader.read_serializable(types.UInt160)

    def can_call(self, target_contract: ContractState, target_method: str) -> bool:
        """
        Utility function to check if the contract has permission to call `target_method` on `target_contract`.

        Args:
            target_contract:
            target_method:

        Returns:
            `True` if allowed. `False` if not possible.
        """
        results = list(
            map(
                lambda p: p.is_allowed(
                    target_contract.hash, target_contract.manifest, target_method
                ),
                self.manifest.permissions,
            )
        )
        return any(results)

    @classmethod
    def _serializable_init(cls):
        return cls(
            0,
            xef.XEF._serializable_init(),
            manifest.ContractManifest(),
            0,
            types.UInt160.zero(),
        )
