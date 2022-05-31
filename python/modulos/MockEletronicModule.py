from modulos.EletronicModule import BaseEletronicModule

class MockEletronicModule(BaseEletronicModule):
    def __init__(self) -> None:
        super().__init__()
    
    def getData(self):
        return super().getData()
    
    def send(self, info):
        return super().send(info)