from modulos.EletronicModule import BaseEletronicModule

class MockEletronicModule(BaseEletronicModule):
    def __init__(self, accel, gyro) -> None:
        super().__init__()
        self.accel = accel
        self.gyro = gyro
    def getAccel(self):
        return self.accel
    def getGyro(self):
        return self.gyro
    def accept(self):
        pass