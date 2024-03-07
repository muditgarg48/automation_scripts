def in_bold(message):
    return '\033[1m' + message + '\033[0m'

def in_italics(message):
    return '\033[3m' + message + '\033[0m'

def underline_this(message):
    return '\033[4m' + message + '\033[0m'

def in_red(message):
    return '\033[31m' + message + '\033[0m'

def in_green(message):
    return '\033[32m' + message + '\033[0m'

def in_yellow(message):
    return '\033[33m' + message + '\033[0m'