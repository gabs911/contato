from time import sleep
from modulos.EletronicModule import BaseEletronicModule

class MockEletronicModule(BaseEletronicModule):
    def __init__(self) -> None:
        super().__init__()
        # Cria uma lista de (giroscopio, acelerometro) para simular o retorno do componente eletrônico
        self.data_list = [(15, 0), (-1, 10), (-1, 0), (-1, 1), (28, 0), (12, 0), (50,0), (-1, 0),
         (-1, 0), (-1, 0), (-1, 1), (49, 0), (100, 20), (90, 0)]
        self.data_index = 0

    def setup(self, porta):
        super().setup(porta)
        sleep(2)
        print(porta)

    def listCOMPorts(self):
        return ["COM3 (Mock)", "COM5 (Mock)", "COM7 (Mock)"]

    def getData(self):
        giro = 360
        accel = 0
        # itera sobre a lista de (giroscopio, acelerometro) com cada chamada da função
        if(self.data_index < len(self.data_list)):
            giro = self.data_list[self.data_index][0]
            accel = self.data_list[self.data_index][1]
            self.data_index += 1
        return {
            "id": "/01",
            "giroscopio": giro,
            "acelerometro": accel,
            "toque": 1
        }

    
    def teardown(self):
        super().teardown()
        self.data_index = 0