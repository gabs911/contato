from config.Config import *

try:
    config = Config("config.json")
    app = config.createApp()
    app.run()
except Exception as e:
    print("Erro durante execução do programa")
    raise e
finally:
    print("Pressione 'Enter' para fechar")
    wait = input()