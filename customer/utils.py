import configparser

config = configparser.ConfigParser()
config.read('config.ini')

configUI = config['UI']