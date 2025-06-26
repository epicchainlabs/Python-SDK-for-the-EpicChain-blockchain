import unittest
from epicchain.contracts import utils, xef
from epicchain.core import types


class TestContractUtils(unittest.TestCase):
    def test_get_contract_hash(self):
        xef_ = xef.XEF("test", b"\x01\x02\x03")
        actual = utils.get_contract_hash(types.UInt160.zero(), xef_.checksum, "test")
        expected = types.UInt160.from_string(
            "0x576c9c6f22eea8fd823155b00141a4327bac8263"
        )
        self.assertEqual(expected, actual)

        actual = utils.get_contract_hash(
            types.UInt160.from_string("0xa400ff00ff00ff00ff00ff00ff00ff00ff00ff01"),
            xef_.checksum,
            "test",
        )
        expected = types.UInt160.from_string(
            "0x55f776130883b2d486dec295ca74533663d0f8ea"
        )
        self.assertEqual(expected, actual)
