from bitarray import bitarray  # type: ignore
from epicchaincrypto import mmh3_hash  # type: ignore
from typing import Optional


class BloomFilter:
    """
    """

    def __init__(self, m: int, k: int, ntweak: int, elements: Optional[bytes] = None):
        """

        Args:
            m: size of bitarray.
            k: number of hash functions.
            ntweak: correction factor.
            elements: hex-escaped bytearray of values to create the bitarray from.
                Warning: the bit array is truncated to size `m`.

        """
        self.K = k
        self.seeds = [(p * 0xFBA4C795 + ntweak) % 4294967296 for p in range(0, k)]
        if elements:
            tmp_bits = bitarray(endian="little")
            tmp_bits.frombytes(elements)
            # truncate to m bits
            self.bits = tmp_bits[:m]
        else:
            self.bits = bitarray(m, endian="little")
            self.bits.setall(False)
        self.tweak = ntweak

    def add(self, element: bytes) -> None:
        """
        Add an element to the filter.

        Args:
            element: hex-escaped bytearray.
        """
        for s in self.seeds:
            h = mmh3_hash(element, s, signed=False)
            self.bits[h % len(self.bits)] = True

    def check(self, element: bytes) -> bool:
        """
        Check if the element is present

        Args:
            element: hex-escaped bytearray

        Returns: True if present. False if not present.
        """
        for s in self.seeds:
            h = mmh3_hash(element, s, signed=False)
            if not self.bits[h % len(self.bits)]:
                return False
        return True

    def get_bits(self) -> bytes:
        """
        Return the filter bits.
        """
        return self.bits.tobytes()
