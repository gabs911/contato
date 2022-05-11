#Uma 'interface' que vai definir os métodos em comum no Mock e no real
class BaseEletronicModule:
    def getGyro(self):
        pass
    def getAccel(self):
        pass
    #faz o setup do que vai ser necessário no programa
    def setup(self):
        pass
    #aceita um valor para enviar para o processo eletronico
    def accept(self):
        pass

#implementacao da parte que vai interagir com as partes eletronicas
class EletronicModule(BaseEletronicModule):
    def __init__(self) -> None:
        pass