class Config:

    all = dict()
    inexact = dict()
    semiexact = dict()

    def __init__(self):
        config_reader = open('config.csv', 'r')

        # skip the header
        config_reader.readline()
        config_lines = file.read(config_reader).splitlines()
        config_reader.close()

        for line in config_lines:
            tokens = line.split(',')
            Config.all[tokens[0]] = tokens[1:]
            if tokens[1] == 'inexact_mapping':
                Config.inexact[tokens[0]] = (tokens[2], float(tokens[3]))
            elif tokens[1] == 'semiexact_mapping':
                Config.semiexact[tokens[0]] = tokens[2]