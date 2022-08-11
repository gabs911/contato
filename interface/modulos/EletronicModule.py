from typing import Any
from serial import Serial, STOPBITS_ONE

class BaseEletronicModule:
    '''Uma 'interface' que vai definir os métodos em comum no Mock e no real e prover a documentação das funções'''
        
    def setup(self):
        '''faz o setup do que vai ser necessário no programa'''
        
    def getData(self) -> Any:
        ''' 
        busca dados da identificação do dispositivo eletrônico, giroscópio, acelerometro e toque
        :return: os dados na forma de um json {"id", "giroscopio", "acelerometro", "toque"}
        '''

    def teardown(self):
        pass

#implementacao da parte que vai interagir com as partes eletronicas
class EletronicModule(BaseEletronicModule):
    def __init__(self, porta) -> None:
        self.porta = porta


    def setup(self):
        super().setup()
        self.serialPort = Serial(port = self.porta, baudrate=115200, bytesize=8, timeout=2, stopbits=STOPBITS_ONE)

    def getData(self) -> Any:
        super().getData()
        if(self.serialPort.in_waiting > 0):
            serialString = self.serialPort.readline()
            sensorData = (serialString.decode('utf-8').split('/'))

            return {
                "id": sensorData[0],
                "giroscopio": float(sensorData[1]),
                "acelerometro": float(sensorData[2]),
                "toque": int(sensorData[3])
            }
    
    def teardown(self):
        self.serialPort.close()
