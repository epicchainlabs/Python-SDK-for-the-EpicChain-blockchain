import unittest
from epicchain.contracts import contract, xef, manifest
from epicchain.core import types


class ContractStateTestCase(unittest.TestCase):
    def test_equals(self):
        manifest_ = manifest.ContractManifest()
        xef_ = xef.XEF()
        state = contract.ContractState(1, xef_, manifest_, 0, types.UInt160.zero())
        clone = contract.ContractState(1, xef_, manifest_, 0, types.UInt160.zero())
        self.assertEqual(state, clone)

        xef2 = xef.XEF()
        state2 = contract.ContractState(
            2, xef2, manifest_, 0, types.UInt160(b"\x01" * 20)
        )
        self.assertNotEqual(state, state2)
        self.assertNotEqual(state, None)
        self.assertNotEqual(state, object())
