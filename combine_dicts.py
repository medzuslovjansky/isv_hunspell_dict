from argparse import ArgumentParser
from utilities import open_with_dir_create
from utilities import determine_long_flag
from utilities import printProgressBar
import pickle
import time

start_time = time.time()
# OPTIONS (DEFAULT: LAT+CYR)
OUTPUT_DICTIONARY_NAME = 'output/dictionaries/KOMBO_DEFAULT'
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_latcyr.txt'
PICKLE_FOLDER = 'cache/pickling/'
# possible types: PICKLE, AFFDIC(latter not currently implemented)
INPUT_DICTIONARIES = [
    {'file': 'output/dictionaries/Medzuslovjansky_Kirilica', 'type': 'PICKLE'},
    {'file': 'output/dictionaries/Medzuslovjansky_LatinicaStandard', 'type': 'PICKLE'}
]


# NEXT LINE WILL BE REPLACED WITH CONTENTS OF SETTINGS FILE IF RUN THROUGH RUN_INSTRUMENT.PY
#!!!


dictList = INPUT_DICTIONARIES
summedDictionary = []
summedSuffixSchemes = []
# process each dictionary, adding only words and suffix schemes not added before
print('\nGenerating combined dictionary ' + OUTPUT_DICTIONARY_NAME)
for dicIndex, dic in enumerate(dictList):
    if dic['type'] == 'PICKLE':
        with open_with_dir_create(PICKLE_FOLDER + dic['file'] + '_aff.pic', 'rb') as f:
            dicSuffixScheme = pickle.load(f)
        with open_with_dir_create(PICKLE_FOLDER + dic['file'] + '_dic.pic', 'rb') as f:
            print('Processing dictionary \"' + dic['file'] + '\" (' + str(dicIndex+1) + '/' + str(len(dictList)) + ')')
            dicFile = pickle.load(f)
    elif dic['type'] == 'AFFDIC':
        raise NotImplementedError('Analysing of non-pickled dictionaries not available yet.')
    else:
        raise TypeError('File of invalid type.')
    dicLen = len(dicFile)
    for wordIndex, word in enumerate(dicFile):
        printProgressBar(wordIndex + 1, dicLen, prefix='Progress:', length=40)
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
print('Combined dictionary length: ' + str(len(summedDictionary)) + ' | Combined suffix library length: ' + str(len(summedSuffixSchemes)))
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

print('Writing output files...Done, finished in %.2f seconds' % (time.time()-start_time))
