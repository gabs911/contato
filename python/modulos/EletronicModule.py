from typing import Any


class BaseEletronicModule:
    '''Uma 'interface' que vai definir os métodos em comum no Mock e no real e prover a documentação das funções'''
        
    def setup(self):
        '''faz o setup do que vai ser necessário no programa'''
        
    def getData(self) -> Any:
        ''' 
        busca dados da identificação do dispositivo eletrônico, giroscópio, acelerometro e toque
        :return: os dados na forma de um json {"id", "giroscopio", "acelerometro", "toque"}
        '''

    def send(self, info):
        '''
        aceita um valor para enviar para o processo eletronico
        :param1 info: json specificando a nota a ser tocada
        '''

#implementacao da parte que vai interagir com as partes eletronicas
class EletronicModule(BaseEletronicModule):
    def __init__(self, porta) -> None:
        self.porta = porta

    def setup(self):
        super().setup()
