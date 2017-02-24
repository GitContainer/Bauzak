from unittest.case import TestCase
from unittest.mock import MagicMock
from bauzak.Modbus控制器 import Modbus控制器


class 讀coils(TestCase):

    def setUp(self):
        self.PLC控制 = Modbus控制器(
            'localhost', '502'
        )
        self.PLC控制.連線 = MagicMock()

    def test_讀一个(self):
        self.PLC控制.讀一个('M0')
        self.PLC控制.連線.read_coils.assert_called_once_with(2000, 1)
