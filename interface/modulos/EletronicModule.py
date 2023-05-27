from typing import Any
from serial import Serial, STOPBITS_ONE
from serial.tools.list_ports import comports

class BaseEletronicModule:
    '''
    Uma 'interface' que vai definir os métodos em comum no Mock e no real e prover a documentação das funções
    '''
        
    def setup(self, porta):
        '''
        Conecta o Bluetooth na porta especificada
        '''
        
    def getData(self) -> Any:
        ''' 
        busca dados da identificação do dispositivo eletrônico, giroscópio, acelerometro e toque
        :return: os dados na forma de um json {"id", "giroscopio", "acelerometro", "toque"}
        '''
    def listCOMPorts(self):
        '''
        retorna uma lista dos nomes das portas COM
        '''
        pass

    def teardown(self):
        '''
        Fecha a conexão com a porta COM
        '''
        pass

#implementacao da parte que vai interagir com as partes eletronicas
class EletronicModule(BaseEletronicModule):
    def __init__(self) -> None:
        pass

    def listCOMPorts(self):
        super().listCOMPorts()
        print("recuperou lista")
        return list(map(lambda port: port.name , comports()))

    def setup(self, porta):
        super().setup(porta)
        self.serialPort = Serial(port = porta, baudrate=115200, bytesize=8, timeout=2, stopbits=STOPBITS_ONE)

    def getData(self) -> Any:
        super().getData()
        if(self.serialPort.in_waiting > 0):
            serialString = self.serialPort.readline()
            # a informação vem do Serial na forma id/giroscopio/acelerometro/toque
            sensorData = (serialString.decode('utf-8').split('/'))

            data = {
                "id": sensorData[0],
                "giroscopio": float(sensorData[1]),
                "acelerometro": float(sensorData[2]),
                "toque": int(sensorData[3])
            }
            print(data)
            return data
    
    def teardown(self):
        self.serialPort.close()
