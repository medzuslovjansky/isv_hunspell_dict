from argparse import ArgumentParser
from utilities import open_with_dir_create

parser = ArgumentParser()
parser.add_argument('scriptfile', metavar='main.py', type=ascii, help='Script to run.')
parser.add_argument('settingfile', metavar='settings_lat.py', type=ascii, help='Settings file.')

args = parser.parse_args()
scriptfile_name = args.scriptfile.translate(str.maketrans('', '', '\'\"'))
settingfile_name = args.settingfile.translate(str.maketrans('', '', '\'\"'))
script = ''
with open_with_dir_create(scriptfile_name, "r") as text_file:
    script = script + (text_file.read())
    with open_with_dir_create(settingfile_name, "r") as replace_file:
        script = script.replace('#!!!', replace_file.read())
exec(script)