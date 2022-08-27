from tkinter import StringVar


class PresetFormData:
    def __init__(self, data = None) -> None:
        self.item_data = data
        self.notas = []
        self.angulo_inicial: StringVar = None
        self.nome: StringVar = None
        self.root = None

    def addNota(self, angulo: StringVar, id: StringVar) -> None:
        self.notas.append({
            "id":id,
            "angulo":angulo
        })
    
    def notaNula(self):
        return {
            "id": StringVar(self.root, ""),
            "angulo": StringVar(self.root, "0")
        }
    
    def deletaNota(self):
        self.notas.pop()
    
    def converteParaView(self) -> None:
        if self.item_data == None:
            self.angulo_inicial = StringVar(self.root, "0")
            self.nome = StringVar(self.root, "")
            return

        self.notas = []
        for nota in self.item_data["notas"]:
            self.addNota(
                StringVar(self.root, nota["proximo_angulo"]),
                StringVar(self.root, nota["id"])
            )
        self.angulo_inicial = StringVar(self.root, self.item_data["angulo_inicial"])
        self.nome = StringVar(self.root, self.item_data["nome"])

    def converteParaSalvar(self):
        notas = []
        for nota in self.notas:
            notas.append({
                "id": nota["id"].get(),
                "proximo_angulo": int(nota["angulo"].get())
            })
        return {
            "nome": self.nome.get(),
            "angulo_inicial": int(self.angulo_inicial.get()),
            "notas": notas
        }