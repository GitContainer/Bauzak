
class Modbus試驗:

    def __init__(self, 對應表):
        self.對應表 = 對應表

    def __getattr__(self, name):
        print('n', name)
        return False

    def __setattr__(self, name, value):
        print('aa,', name, value
              )
