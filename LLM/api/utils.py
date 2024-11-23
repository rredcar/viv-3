def config_parser(config_path):
    with open(config_path, 'r') as config_file:
        config = dict()
        lines = config_file.readlines()
        for line in lines:
            i, j = line.split( ' = ')
            config[i] = j.split('\n')[0]
        return config