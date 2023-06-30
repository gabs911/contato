from config.Config import *
from logging import getLogger

try:
    config = Config("config.json")
    app = config.createApp()
    del config
    app.run()
except Exception as e:
    print("Erro durante execução do programa")
    logger = getLogger('root')
    logger.exception(e,stack_info=False)
    raise e
finally:
    print("Pressione 'Enter' para fechar")
    wait = input()