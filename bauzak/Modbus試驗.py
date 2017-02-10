from bauzak.Modbus控制器 import Modbus控制器


class Modbus試驗(Modbus控制器):

    'https://pypi.python.org/pypi/fatek-fbs-lib/0.1.4'
    Fatek_PLC_offset = {
        'Y': 0,
        'X': 1000,
        'M': 2000,
        'S': 6000,
        'T': 9000,
        'R': 0,
        'D': 6000,
        'C': 9500
    }

    def __init__(self, ip, port, 對應表):
        super(Modbus試驗, self).__init__(ip, port)
        self.對應表 = 對應表

    def __getattr__(self, name):
        位址 = self.對應表[name]
        if 位址.startswith('R'):
            開始 = int(位址.strip('R'))
            結果 = self.連線.read_holding_registers(開始, 1)
            return 結果.registers[0]
        if 位址.startswith('M'):
            開始 = int(位址.strip('M')) + self.Fatek_PLC_offset['M']
            結果 = self.連線.read_coils(開始, 1)
            return 結果.bits[0]
        raise ValueError()

    def __setattr__(self, name, value):
        if name in ["連線", "對應表"]:
            return super(Modbus試驗, self).__setattr__(name, value)
        位址 = self.對應表[name]
        if 位址.startswith('R'):
            開始 = int(位址.strip('R'))
            self.連線.write_registers(開始, [value])
            return
        if 位址.startswith('M'):
            開始 = int(位址.strip('M'))
            self.連線.write_coil(開始, value)
            return
        raise ValueError()
