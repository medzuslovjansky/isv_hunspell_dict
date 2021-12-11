from argparse import ArgumentParser
from main import open_with_dir_create
from main import determine_long_flag
import pickle

# OPTIONS
OUTPUT_DICTIONARY_NAME = 'dictionaries/isv_latcyr_hunspell_dict'
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_latcyr.txt'


# parse dictionary names
parser = ArgumentParser()
parser.add_argument('dicts', nargs='+', type=ascii, help='Dictionary names to combine.')
dictList = [dic.translate(str.maketrans('', '', '\'\"')) for dic in parser.parse_args().dicts]
summedDictionary = []
summedSuffixSchemes = []
# process each dictionary, adding only words and suffix schemes not added before
for dic in dictList:
    with open_with_dir_create('pickling/' + dic + '_aff.pic', 'rb') as f:
        dicSuffixScheme = pickle.load(f)
    with open_with_dir_create('pickling/' + dic + '_dic.pic', 'rb') as f:
        for word in pickle.load(f):
            add = True
            for alreadyAddedWord in summedDictionary:
                if alreadyAddedWord['word'] == word['word']:
                    if word['flags'] and alreadyAddedWord['flags']:
                        if dicSuffixScheme[word['flags'][0]] == summedSuffixSchemes[alreadyAddedWord['flags'][0]]:
                            add = False
                            break
                    else:
                        if not alreadyAddedWord['flags']:
                            add = False
                            break
            if add is True:
                if word['flags']:
                    if dicSuffixScheme[word['flags'][0]] not in summedSuffixSchemes:
                        summedSuffixSchemes.append(dicSuffixScheme[word['flags'][0]])
                    word['flags'][0] = summedSuffixSchemes.index(dicSuffixScheme[word['flags'][0]])
                    summedDictionary.append(word)
                else:
                    summedDictionary.append(word)
                print(word)

print(len(summedDictionary))
print(len(summedSuffixSchemes))

with open_with_dir_create(OUTPUT_DICTIONARY_NAME + '.dic', 'w') as f:
    print(str(len(summedDictionary)), file=f)
    for entry in summedDictionary:
        combinedFlags = ''.join([determine_long_flag(flagNum) for flagNum in entry['flags']])
        if combinedFlags:
            combinedFlags = '/' + combinedFlags
        print(entry['word'] + combinedFlags, file=f)
with open_with_dir_create(OUTPUT_DICTIONARY_NAME + '.aff', 'w') as f:
    with open(AFFIX_FILE_HEADER_NAME, 'r') as header:
        print(header.read(), file=f)
        for index, schemeIterate in enumerate(summedSuffixSchemes):
            print('SFX ' + determine_long_flag(index) + ' Y ' + str(len(schemeIterate)), file=f)
            for instructionIterate in schemeIterate:
                print('SFX ' + determine_long_flag(index) + ' ' + instructionIterate['delete'] + ' ' +
                    instructionIterate['add'] + ' ' + instructionIterate['condition'], file=f)
            print('', file=f)

# delete duplicate words
