from config.Config import *

config = Config("config.json")
app = config.createApp()
app.run()