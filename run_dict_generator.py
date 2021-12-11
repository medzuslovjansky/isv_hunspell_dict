from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('settingfile', metavar='settings_lat.py', type=ascii, help='Settings file.')

args = parser.parse_args()
filename = args.settingfile.translate(str.maketrans('', '', '\'\"'))
script = ''
with open('main.py', "r") as text_file:
    script = script + (text_file.read())
    with open(filename, "r") as replace_file:
        script = script.replace('#!!!', replace_file.read())
exec(script)