import unittest
import binascii
from epicchain.contracts import callflags, xef
from epicchain.core import types
from copy import deepcopy


class XEFTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """
        var xef = new XefFile
        {
            Compiler = "test-compiler 0.1",
            Source = "source_link",
            Script = new byte[] {(byte) OpCode.RET},
            Tokens = new MethodToken[]
            {
                new MethodToken()
                {
                    Hash = UInt160.Zero,
                    Method = "test_method",
                    ParametersCount = 0,
                    HasReturnValue = true,
                    CallFlags = CallFlags.None
                }
            }
        };
        xef.CheckSum = XefFile.ComputeChecksum(xef);
        Console.WriteLine(xef.ToArray().ToHexString());
        Console.WriteLine(xef.Size);
        """
        cls.expected = binascii.unhexlify(
            b"4e454633746573742d636f6d70696c657220302e3100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000b736f757263655f6c696e6b000100000000000000000000000000000000000000000b746573745f6d6574686f64000001000000014072adaf87"
        )
        cls.expected_length = 126
        compiler = "test-compiler 0.1"
        source = "source_link"
        ret = b"\x40"  # vm.OpCode.RET
        tokens = [
            xef.MethodToken(
                types.UInt160.zero(), "test_method", 0, True, callflags.CallFlags.NONE
            )
        ]
        cls.xef = xef.XEF(
            compiler_name=compiler, script=ret, tokens=tokens, source=source
        )

    def test_serialization(self):
        self.assertEqual(self.expected, self.xef.to_array())

    def test_deserialization(self):
        xef_ = xef.XEF.deserialize_from_bytes(self.expected)
        self.assertEqual(self.xef.magic, xef_.magic)
        self.assertEqual(self.xef.source, xef_.source)
        self.assertEqual(self.xef.compiler, xef_.compiler)
        self.assertEqual(self.xef.script, xef_.script)
        self.assertEqual(self.xef.checksum, xef_.checksum)

    def test_deserialization_error(self):
        xef1 = deepcopy(self.xef)
        xef1.magic = 0xDEADBEEF
        with self.assertRaises(ValueError) as context:
            xef.XEF.deserialize_from_bytes(xef1.to_array())
        self.assertEqual(
            "Deserialization error - Incorrect magic", str(context.exception)
        )

        xef_ = deepcopy(self.xef)
        xef_.script = b""
        with self.assertRaises(ValueError) as context:
            xef.XEF.deserialize_from_bytes(xef_.to_array())
        self.assertEqual(
            "Deserialization error - Script can't be empty", str(context.exception)
        )

        # test with wrong checksum
        xef_ = deepcopy(self.xef)
        xef_._checksum = 0xDEADBEEF
        with self.assertRaises(ValueError) as context:
            xef.XEF.deserialize_from_bytes(xef_.to_array())
        self.assertEqual(
            "Deserialization error - Invalid checksum", str(context.exception)
        )

    def test_len(self):
        self.assertEqual(self.expected_length, len(self.xef))

    def test_eq(self):
        compiler = "test-compiler 0.1"
        ret = b"\x40"  # vm.OpCode.RET
        xef1 = xef.XEF(compiler_name=compiler, script=ret)
        xef2 = xef.XEF(compiler_name=compiler, script=ret)
        self.assertFalse(xef1 == object())
        self.assertTrue(xef1 == xef2)
