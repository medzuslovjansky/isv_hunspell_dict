import os
from pathlib import Path
import re

AFFIX_FLAG_NAME_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


def clean_str(s):
    return ''.join(c for c in s if c.isprintable())


def determine_flag(number, flag_type='LONG'):
    if flag_type == 'LONG':
        letterIndex1 = number // len(AFFIX_FLAG_NAME_CHARACTERS)
        letterIndex2 = number % len(AFFIX_FLAG_NAME_CHARACTERS)
        if letterIndex1 >= len(AFFIX_FLAG_NAME_CHARACTERS):
            raise RuntimeError('Ran out of possible affix flags')
        return AFFIX_FLAG_NAME_CHARACTERS[letterIndex1] + AFFIX_FLAG_NAME_CHARACTERS[letterIndex2]
    if flag_type == 'NORMAL' or flag_type == 'UTF-8':
        return chr(number)
    if flag_type == 'NUM':
        return number


def get_flags_from_string(s, flag_type='LONG'):
    if flag_type == 'NORMAL' or flag_type == 'UTF-8':
        return [ord(c) for c in s]
    if flag_type == 'NUM':
        return [int(n) for n in s.split(',')]
    if flag_type == 'LONG':
        longStringFlags = re.findall('..?', s)
        return [ord(longStringFlag[0])*256 + ord(longStringFlag[1]) for longStringFlag in longStringFlags]


def open_with_dir_create(path, mode, encoding=None):
    path = path.replace('/', os.path.sep)
    *directories, fileName = path.split(os.path.sep)
    if not directories:
        return open(path, mode, encoding=encoding)
    if directories:
        dirpath = ''.join([os.path.sep + directory for directory in directories if directory])
        Path(os.getcwd()+dirpath).mkdir(parents=True, exist_ok=True)
        return open(path, mode, encoding=encoding)


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    return None
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
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
        # Print New Line on Complete
        if iteration == total:
            print()
    else:
        pass


def write_dic_file(dictionary_list, out_file, flag_type='LONG'):
    with open_with_dir_create(out_file + '.dic', 'w') as f:
        print(str(len(dictionary_list)), file=f)
        for entry in dictionary_list:
            combinedFlags = ''.join([determine_flag(flagNum, flag_type=flag_type) for flagNum in entry['flags']])
            if combinedFlags:
                combinedFlags = '/' + combinedFlags
            print(entry['word'] + combinedFlags, file=f)


def write_aff_file(afx_scheme_list, out_file, header_file=None, flag_type='LONG'):
    with open_with_dir_create(out_file + '.aff', 'w') as f:
        if header_file is not None:
            with open(header_file, 'r') as header:
                print(header.read(), file=f)
        for index, schemeIterate in enumerate(afx_scheme_list):
            print(schemeIterate['type'] + ' ' + determine_flag(index, flag_type=flag_type) + ' Y ' + str(len(schemeIterate['scheme'])), file=f)
            for instructionIterate in schemeIterate['scheme']:
                print(schemeIterate['type'] + ' ' + determine_flag(index, flag_type=flag_type) + ' ' + instructionIterate['delete'] + ' ' +
                      instructionIterate['add'] + ' ' + instructionIterate['condition'], file=f)
            print('', file=f)
