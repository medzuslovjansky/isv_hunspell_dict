from utilities import *
import pickle
import time
from pprint import pprint

start_time = time.time()
'''# OPTIONS (DEFAULT: LAT+CYR)
OUTPUT_DICTIONARY_NAME = 'output/dictionaries/KOMBO_DEFAULT'
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_latcyr.txt'
PICKLE_FOLDER = 'cache/pickling/'
# possible types: PICKLE, AFFDIC(latter not currently implemented)
INPUT_DICTIONARIES = [
    {'file': 'output/dictionaries/Medzuslovjansky_Kirilica', 'type': 'PICKLE'},
    {'file': 'output/dictionaries/Medzuslovjansky_LatinicaStandard', 'type': 'PICKLE'}
]'''
# OPTIONS
OUTPUT_DICTIONARY_NAME = 'tests/test_out'
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_latcyr.txt'
PICKLE_FOLDER = 'cache/pickling/'
INPUT_DICTIONARIES = [
    {'file': 'tests/test_in', 'type': 'AFFDIC'},
]

# NEXT LINE WILL BE REPLACED WITH CONTENTS OF SETTINGS FILE IF RUN THROUGH RUN_INSTRUMENT.PY
#!!!


dictList = INPUT_DICTIONARIES
summedDictionary = []
summedAffixSchemes = []
summedAffMisc = []


def append_aff_instr(structured_aff, elem, val):
    searchInd = next((i for i, item in enumerate(structured_aff) if item["elementName"] == elem), None)
    if searchInd is None:
        structured_aff.append({'elementName': elem, 'value': [val]})
    else:
        structured_aff[searchInd]['value'].append(val)


def dic_from_dic_file(opened_dic_file, flag_type):
    returnDic = []
    dicFileLength = 0
    for lineIndex, line in enumerate(opened_dic_file):
        if lineIndex == 0:
            dicFileLength = int(line)
        else:
            strippedLine = clean_str(line)
            if strippedLine != '':
                splitLine = strippedLine.split('/')
                lineWord = splitLine[0]
                if len(splitLine) > 1:
                    lineFlags = get_flags_from_string(splitLine[1], flag_type=flag_type)
                else:
                    lineFlags = []
                returnDic.append({'word': lineWord, 'flags': lineFlags})
    if (len(returnDic) - dicFileLength) > 50 or (len(returnDic) - dicFileLength) < -50:
        print('Warning: non-matching length: ' + str(dicFileLength) + ' and actual length: ' + str(len(returnDic)))
        return returnDic
    else:
        return returnDic


def aff_from_aff_file(opened_aff_file):
    structuredAffMisc = []
    suffixSchemeLibWithFlags = []
    prefixSchemeLibWithFlags = []
    fileFlagType = 'NORMAL'
    lineList = opened_aff_file.readlines()
    for line in lineList:
        # determine file encoding
        if line[:3] == 'SET':
            if line[4:9] != 'UTF-8':
                raise RuntimeError('Unsupported dictionary encoding: ' + line[4:len(line)-1])
    for line in lineList:
        # determine flag type
        if line[:4] == 'FLAG':
            if line[5:9] == 'long':
                fileFlagType = 'LONG'
            elif line[5:8] == 'num':
                fileFlagType = 'NUM'
            elif line[5:10] == 'UTF-8':
                fileFlagType = 'UTF-8'
        # determine misc instructions (not prefixes or suffixes)
        for checkElement in ['TRY', 'WORDCHARS']:
            if line[:len(checkElement)] == checkElement:
                structuredAffMisc.append({'elementName': checkElement, 'value': clean_str(
                    line[len(checkElement) + 1:])})
        for checkElement in ['BREAK', 'COMPOUNDRULE', 'MAP']:
            if line[:len(checkElement)] == checkElement:
                if not clean_str(line[len(checkElement) + 1:]).isnumeric():
                    append_aff_instr(structuredAffMisc, checkElement, clean_str(line[len(checkElement) + 1:]))
        for checkElement in ['REP', 'ICONV', 'OCONV']:
            if line[:len(checkElement)] == checkElement:
                if not clean_str(line).split(' ')[1].isnumeric():
                    append_aff_instr(structuredAffMisc, checkElement, [clean_str(line).split(' ')[1], clean_str(
                            line).split(' ')[2]])
        for checkElement in ['NOSPLITSUGS']:
            if line[:len(checkElement)] == checkElement:
                structuredAffMisc.append({'elementName': checkElement, 'value': True})
        for checkElement in ['NOSUGGEST', 'ONLYINCOMPOUND', 'COMPOUNDBEGIN', 'COMPOUNDEND', 'COMPOUNDPERMITFLAG']:
            if line[:len(checkElement)] == checkElement:
                structuredAffMisc.append({'elementName': checkElement, 'value': clean_str(line).split(' ')[1]})
        for checkElement in ['COMPOUNDMIN']:
            if line[:len(checkElement)] == checkElement:
                structuredAffMisc.append({'elementName': checkElement, 'value': int(clean_str(line).split(' ')[1])})
        # determine prefix and suffix schemes
        for checkElement in ['SFX', 'PFX']:
            if line[:len(checkElement)] == checkElement:
                splitLine = list(filter(None, clean_str(line).split(' ')))
                if len(splitLine) == 5:
                    elementFlag, instrDelete, instrAdd, instrCond = splitLine[1:]
                    instruction = {'delete': instrDelete, 'add': instrAdd, 'condition': instrCond}
                    if checkElement == 'SFX':
                        append_aff_instr(suffixSchemeLibWithFlags, elementFlag, instruction)
                    if checkElement == 'PFX':
                        append_aff_instr(prefixSchemeLibWithFlags, elementFlag, instruction)

    pprint(structuredAffMisc)
    for lib in [suffixSchemeLibWithFlags, prefixSchemeLibWithFlags]:
        for instrScheme in lib:
            instrScheme['elementFlag'] = get_flags_from_string(instrScheme['elementName'], flag_type=fileFlagType)[0]
    suffixSchemeLibWithFlags = sorted(suffixSchemeLibWithFlags, key=lambda i: i['elementFlag'])
    prefixSchemeLibWithFlags = sorted(prefixSchemeLibWithFlags, key=lambda i: i['elementFlag'])
    # 1:SFX 2:PFX
    processedLibs = [[], []]
    for libIndex, lib in enumerate([suffixSchemeLibWithFlags, prefixSchemeLibWithFlags]):
        for padIndex in range(lib[-1]['elementFlag']+1):
            if not any(libElem['elementFlag'] == padIndex for libElem in lib):
                processedLibs[libIndex].append([])
            else:
                processedLibs[libIndex].append(next(item['value'] for item in lib if item['elementFlag'] == padIndex))
    #pprint(processedLibs)
    return fileFlagType, structuredAffMisc, processedLibs[0], processedLibs[1]


def add_misc_aff(source, target):
    for srcElem in source:
        if not any(trgElem['elementName'] == srcElem['elementName'] for trgElem in target):
            target.append(srcElem)
        else:
            if srcElem['elementName'] in ['TRY', 'WORDCHARS']:
                trgIndex = next(i for i, trgElement in enumerate(target) if trgElement['elementName'] == srcElem['elementName'])
                combStr = target[trgIndex]['value'] + srcElem['value']
                combStr = ''.join(set(combStr))
                target[trgIndex]['value'] = combStr
    return target


# process each dictionary, adding only words and suffix schemes not added before
print('\nGenerating combined dictionary ' + OUTPUT_DICTIONARY_NAME)
for dicIndex, dic in enumerate(dictList):
    if dic['type'] == 'PICKLE':
        with open_with_dir_create(PICKLE_FOLDER + dic['file'] + '_aff.pic', 'rb') as f:
            dicSuffixScheme = pickle.load(f)
            dicPrefixScheme = []
            dicAffMisc = []
        with open_with_dir_create(PICKLE_FOLDER + dic['file'] + '_dic.pic', 'rb') as f:
            print('Processing dictionary \"' + dic['file'] + '\" (' + str(dicIndex+1) + '/' + str(len(dictList)) + ')')
            dicFile = pickle.load(f)
    elif dic['type'] == 'AFFDIC':
        with open_with_dir_create(dic['file'] + '.aff', 'r') as f_aff:
            flagType, dicAffMisc, dicSuffixScheme, dicPrefixScheme = aff_from_aff_file(f_aff)
            with open_with_dir_create(dic['file'] + '.dic', 'r') as f_dic:
                # dicFile = -.-
                dicFile = dic_from_dic_file(f_dic, flag_type=flagType)
    else:
        raise TypeError('File of invalid type.')
    if dicIndex == 0 and not summedDictionary and not summedAffixSchemes and dic['type'] == 'PICKLE':
        # add affix header if type AFFDIC
        summedDictionary = dicFile
        summedAffixSchemes = [{'type': 'SFX', 'scheme': sc} for sc in dicSuffixScheme]
        summedAffMisc = add_misc_aff(source=dicAffMisc, target=summedAffMisc)
        print_progress_bar(100, 100, prefix='Progress:', length=40)
        continue
    else:
        toAddDictionary = []
        dicLen = len(dicFile)
        for wordIndex, word in enumerate(dicFile):
            print_progress_bar(wordIndex + 1, dicLen, prefix='Progress:', length=40)
            add = True
            for alreadyAddedWord in summedDictionary:
                if alreadyAddedWord['word'] == word['word']:
                    if word['flags'] and alreadyAddedWord['flags']:
                        if dicSuffixScheme[word['flags']] == summedAffixSchemes[alreadyAddedWord['flags']]['scheme']:
                            add = False
                            break
                    else:
                        if not alreadyAddedWord['flags']:
                            add = False
                            break
            if add is True:
                if word['flags']:
                    for flagIndex, wordFlag in enumerate(word['flags']):
                        if wordFlag < len(dicSuffixScheme) and dicSuffixScheme[wordFlag] != []:
                            if not any(d['scheme'] == dicSuffixScheme[wordFlag] and d['type'] == 'SFX' for d in summedAffixSchemes):
                                summedAffixSchemes.append({'type': 'SFX', 'scheme': dicSuffixScheme[wordFlag]})
                            word['flags'][flagIndex] = next(i for i, item in enumerate(summedAffixSchemes) if item['scheme'] == dicSuffixScheme[wordFlag] and item['type'] == 'SFX')
                        if wordFlag < len(dicPrefixScheme) and dicPrefixScheme[wordFlag] != []:
                            if not any(d['scheme'] == dicPrefixScheme[wordFlag] and d['type'] == 'PFX' for d in summedAffixSchemes):
                                summedAffixSchemes.append({'type': 'PFX', 'scheme': dicPrefixScheme[wordFlag]})
                            word['flags'][flagIndex] = next(i for i, item in enumerate(summedAffixSchemes) if item['scheme'] == dicPrefixScheme[wordFlag] and item['type'] == 'PFX')
                    toAddDictionary.append(word)
                else:
                    toAddDictionary.append(word)
        summedDictionary.extend(toAddDictionary)
        summedAffMisc = add_misc_aff(source=dicAffMisc, target=summedAffMisc)
print('Combined dictionary length: ' + str(len(summedDictionary)) + ' | Combined affix library length: ' + str(len(summedAffixSchemes)))
write_dic_file(dictionary_list=summedDictionary, out_file=OUTPUT_DICTIONARY_NAME, flag_type='LONG')
write_aff_file(afx_scheme_list=summedAffixSchemes, out_file=OUTPUT_DICTIONARY_NAME, header_file=AFFIX_FILE_HEADER_NAME,
               flag_type='LONG')
print('Writing output files...Done, finished in %.2f seconds' % (time.time()-start_time))
