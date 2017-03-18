from unittest.case import TestCase
from unittest.mock import MagicMock
from bauzak.Modbus控制器 import Modbus控制器


class 讀線圈(TestCase):

    def setUp(self):
        self.PLC控制 = Modbus控制器(
            'localhost', '502'
        )
        self.PLC控制.連線 = MagicMock()

    def test_無半个(self):
        表 = {
        }
        self.PLC控制.讀線圈的資料(表)
        self.PLC控制.連線.read_coils.assert_not_called()

    def test_一个(self):
        表 = {
            'A做了幾項': 'M1036',
        }
        self.PLC控制.讀線圈的資料(表)
        self.PLC控制.連線.read_coils.assert_called_once_with(3036, 1)

    def test_特殊counter(self):
        表 = {
            'A做了幾項': 'C255',
        }
        self.PLC控制.讀線圈的資料(表)
        self.PLC控制.連線.read_coils.assert_called_once_with(
            9755, 1
        )

    def test_讀的表佇仝一段(self):
        表 = {
            'A做了幾項':  'S36',
            'B做了幾項': 'S38',
        }
        self.PLC控制.讀線圈的資料(表)
        self.PLC控制.連線.read_coils.assert_called_once_with(6036, 3)

    def test_仝段上遠(self):
        表 = {
            'A做了幾項':  'M0',
            'B做了幾項': 'M1999',
        }
        self.PLC控制.讀線圈的資料(表)
        self.PLC控制.連線.read_coils.assert_called_once_with(2000, 2000)

    def test_讀的表佇無仝一段(self):
        表 = {
            'A做了幾項': 'M0',
            'B做了幾項': 'M2000',
        }
        self.PLC控制.讀線圈的資料(表)
        self.PLC控制.連線.read_coils.assert_any_call(2000, 1)
        self.PLC控制.連線.read_coils.assert_any_call(4000, 1)

    def test_無仝的暫存器嘛會使(self):
        表 = {
            'A做了幾項': 'Y36',
            'AA做了幾項': 'Y136',
            'B做了幾項': 'T100',
            'BB做了幾項': 'T110',
        }
        self.PLC控制.讀線圈的資料(表)
        self.PLC控制.連線.read_coils.assert_any_call(36, 101)
        self.PLC控制.連線.read_coils.assert_any_call(9100, 11)

    def test_暫存器數字(self):
        表 = {
            '0做了幾項': 'Y100',
            '00做了幾項': 'Y104',
            'A做了幾項': 'C36',
            'AA做了幾項': 'C39',
        }
        答案 = {
            '0做了幾項': True,
            '00做了幾項': True,
            'A做了幾項':  True,
            'AA做了幾項': False,
        }
        頭一个回應 = MagicMock()
        頭一个回應.bits = [True, False, True, False, True, False, True, False]
        第二个回應 = MagicMock()
        第二个回應.bits = [True, True, True, False, True, True, True, True]
        self.PLC控制.連線.read_coils.side_effect = [頭一个回應, 第二个回應]

        結果 = self.PLC控制.讀線圈的資料(表)
        self.assertEqual(結果, 答案)

    def test_連續暫存器(self):
        表 = {
            'A做了幾項': 'X36',
            'AA做了幾項': 'X37',
            'AAA做了幾項': 'X38',
        }
        答案 = {
            'A做了幾項':  True,
            'AA做了幾項': False,
            'AAA做了幾項':  True,
        }
        頭一个回應 = MagicMock()
        頭一个回應.bits = [
            True, False, True, False, False, False, False, False
        ]
        self.PLC控制.連線.read_coils.return_value = 頭一个回應

        結果 = self.PLC控制.讀線圈的資料(表)
        self.assertEqual(結果, 答案)
