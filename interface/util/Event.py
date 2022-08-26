class SimpleEvent:
    def __init__(self) -> None:
        self.listeners = list()
    
    def add_listenter(self, listener) -> None:
        self.listeners.append(listener)
    
    def clear(self) -> None:
        self.listeners.clear()
    
    def invoke(self, arg) -> None:
        for listener in self.listeners:
            listener(arg)

