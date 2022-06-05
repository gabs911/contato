from modulos.EletronicModule import BaseEletronicModule

class MockEletronicModule(BaseEletronicModule):
    def __init__(self) -> None:
        super().__init__()
        self.data_list = [(15, 0), (-1, 0), (-1, 0), (-1, 1), (28, 0), (12, 0), (50,0), (-1, 0),
         (-1, 0), (-1, 0), (-1, 1), (49, 0), (100, 0), (90, 0)]
        self.data_index = 0


    def getData(self):
        giro = -1
        accel = 0
        if(self.data_index < len(self.data_list)):
            giro = self.data_list[self.data_index][0]
            accel = self.data_list[self.data_index][1]
            self.data_index += 1
        return {
            "giroscopio": giro,
            "acelerometro": accel,
            "toque": 1
        }

    
    def send(self, info):
        return super().send(info)