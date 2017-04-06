import Viper

newViperApp = Viper.Viper()
newViperApp.setup(12500)

def hello():
    return 'Hello World!'

newViperApp.add_method('/hello/', 'GET', hello)

newViperApp.run()