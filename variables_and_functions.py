import configparser as cfg

CONFIG_FILE = 'config.cfg'

def read_from_config_file(config, *args):
    parser = cfg.ConfigParser()
    parser.read(config)
    return parser.get(*args)
