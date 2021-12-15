import os
from pathlib import Path

AFFIX_FLAG_NAME_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def determine_long_flag(number):
    letterIndex1 = number // len(AFFIX_FLAG_NAME_CHARACTERS)
    letterIndex2 = number % len(AFFIX_FLAG_NAME_CHARACTERS)
    if letterIndex1 >= len(AFFIX_FLAG_NAME_CHARACTERS):
        raise RuntimeError('Ran out of possible affix flags')
    return AFFIX_FLAG_NAME_CHARACTERS[letterIndex1] + AFFIX_FLAG_NAME_CHARACTERS[letterIndex2]


def open_with_dir_create(path, mode, encoding=None):
    path = path.replace('/', os.path.sep)
    *directories, fileName = path.split(os.path.sep)
    if not directories:
        return open(path, mode, encoding=encoding)
    if directories:
        dirpath = ''.join([os.path.sep + directory for directory in directories if directory])
        Path(os.getcwd()+dirpath).mkdir(parents=True, exist_ok=True)
        return open(path, mode, encoding=encoding)


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    if iteration <= total:
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print()
    else:
        pass
