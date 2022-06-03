from modulos.EletronicModule import BaseEletronicModule

class MockEletronicModule(BaseEletronicModule):
    def __init__(self) -> None:
        super().__init__()
        self.data_list = [15, -1, -1, -1, 28, 12, 50, -1, -1, -1, -1, 49, 100, 90]
        self.data_index = 0


    def getData(self):
        giro = -1
        if(self.data_index < len(self.data_list)):
            giro = self.data_list[self.data_index]
            self.data_index += 1
        return {
            "giroscopio": giro
        }

    
    def send(self, info):
        return super().send(info)