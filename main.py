import lxml.etree as ET
import json

# OPTIONS:
OUTPUT_DICTIONARY_NAME = 'isv_lat_hunspell_dict'
OPENCORPORAXML_FILE_NAME = 'out_isv_lat.xml'
ACCEPTABLE_WORD_CHARS = '-ABCDEFGHIJKLMNOPQRSTUVWXYZčČžŽěĚšŠabcdefghijklmnopqrstuvwxyz '
GENERATE_ADDITIONAL_ISV_DERIVATIVE_WORD_FORMS = True
MODIFY_SUFFIXES = True
ADDITIONAL_ISV_FORMS_FILE_NAMES = 'isv_lat_additional'
AFFIX_FLAG_NAME_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
AFFIX_FILE_HEADER_NAME = 'affix_file_header.txt'
SPECIAL_HANDLING_OF_ISV_REFLEXIVE_VERBS = True
SPECIAL_HANDLING_OF_ISV_NEGATIVE_VERBS = True
SPECIAL_HANDLING_OF_ISV_ADJECTIVES_WITH_ADVERBS = True

addSuffixTableList = []
addSuffixTableVerb = {'partOfSpeech': 'VERB', 'list': []}
addSuffixTableVerb['list'].append({'baseSuffix': 'nje', 'addSuffixes': ['nja', 'nju', 'njem', 'nij', 'njam', 'njami', 'njah']})
addSuffixTableVerb['list'].append({'baseSuffix': 'uči',
                       'addSuffixes': ['učego', 'učemu', 'učim', 'učem', 'učih', 'učimi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'uča',
                       'addSuffixes': ['uču', 'učej', 'učeju']})
addSuffixTableVerb['list'].append({'baseSuffix': 'my',
                       'addSuffixes': ['mogo', 'momu', 'mym', 'mom', 'mo']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ma',
                       'addSuffixes': ['mu', 'moj', 'moju', 'mi', 'me', 'myh', 'mym', 'mymi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'vši',
                       'addSuffixes': ['všego', 'všemu', 'všim', 'všem', 'vših', 'všimi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'vša',
                       'addSuffixes': ['všu', 'všej', 'všeju']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ny',
                       'addSuffixes': ['nogo', 'nomu', 'nym', 'nom', 'ni', 'ne', 'nyh', 'nymi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'na',
                       'addSuffixes': ['nu', 'noj', 'noju']})


addSuffixTableAdjective = {'partOfSpeech': 'ADJF', 'list': []}
addSuffixTableAdjective['list'].append({'baseSuffix': 'ši',
                       'addSuffixes': ['šego', 'šemu', 'šim', 'šem', 'še', 'ša', 'šu', 'šej', 'šeju', 'ših', 'šim', 'šimi']})

addSuffixTableList.append(addSuffixTableVerb)
addSuffixTableList.append(addSuffixTableAdjective)

suffixModificationTable = []
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'ši', 'modifiedAddForm': 'ši/zz'})
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'je', 'modifiedAddForm': 'je/zz'})


with open(ADDITIONAL_ISV_FORMS_FILE_NAMES + '_derivative_forms.json', 'w', encoding='utf8') as f:
    print(json.dumps(addSuffixTableList, indent=1, ensure_ascii=False), file=f)

with open(ADDITIONAL_ISV_FORMS_FILE_NAMES + '_modified_suffixes.json', 'w', encoding='utf8') as f:
    print(json.dumps(suffixModificationTable, indent=1, ensure_ascii=False), file=f)

def determine_long_flag(number):
    letterIndex1 = 0
    letterIndex2 = 0
    while (letterIndex1 * len(AFFIX_FLAG_NAME_CHARACTERS) + letterIndex2) < number:
        letterIndex2 += 1
        if letterIndex2 >= len(AFFIX_FLAG_NAME_CHARACTERS):
            letterIndex1 += 1
            letterIndex2 = 0
        if letterIndex1 >= len(AFFIX_FLAG_NAME_CHARACTERS):
            raise RuntimeError('Ran out of flags')
    return AFFIX_FLAG_NAME_CHARACTERS[letterIndex1] + AFFIX_FLAG_NAME_CHARACTERS[letterIndex2]


with open(OPENCORPORAXML_FILE_NAME, 'r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()
lemmata = root[1]
dictionary = []
suffixSchemeLibrary = []
if not lemmata.tag == 'lemmata':
    print('XML Structure error')
else:
    counter = 0
    for lemma in lemmata:
        partOfSpeech = ''
        # part of speech attributes are capitalised in OpenCorporaXML format, no others are
        for baseFormAttribContainer in lemma[0]:
            partOfSpeech = baseFormAttribContainer.attrib['v']
            if partOfSpeech.isupper():
                break
        reducedForms = []
        dictionaryEntry = {'word': '', 'flags': []}
        additionalDictionaryEntries = []
        suffixScheme = []
        rememberBadAdjectiveAdverbCombination = ''
        for form in lemma:
            formString = form.attrib['t']  # read form
            formString = ''.join(
                char for char in formString if char in ACCEPTABLE_WORD_CHARS)
            if SPECIAL_HANDLING_OF_ISV_REFLEXIVE_VERBS is True:
                if formString[len(formString)-3:len(formString)] == ' se' and partOfSpeech == 'VERB':
                    formString = formString[0:len(formString)-3]
            if SPECIAL_HANDLING_OF_ISV_NEGATIVE_VERBS is True:
                if 'ne ' == formString[0:3] and partOfSpeech == 'VERB':
                    formString = formString [3:len(formString)]
            if SPECIAL_HANDLING_OF_ISV_ADJECTIVES_WITH_ADVERBS is True:
                if len(reducedForms) > 0:
                    if ('o ' + formString) in reducedForms[0]:
                        rememberBadAdjectiveAdverbCombination = reducedForms[0]
                        splitWords = reducedForms[0].split()
                        if len(splitWords) == 2:
                            additionalDictionaryEntries.append(splitWords[0])
                            reducedForms[0] = splitWords [1]
                    if formString == rememberBadAdjectiveAdverbCombination:
                        formString = ''
            if reducedForms.count(formString) == 0 and not formString == '':
                reducedForms.append(formString)  # only add forms that haven't been added before
        baseForm = ''
        if len(reducedForms) > 0:  # if any form exists
            baseForm = reducedForms[0]  # baseForm will be the word form in the dictionary .dic file
            dictionaryEntry['word'] += baseForm
        if len(reducedForms) > 1:  # if more than 1 form
            for index, formString in enumerate(reducedForms):
                if not index == 0:
                    if not formString[0] == baseForm[0] and not partOfSpeech == 'ADJF':
                        additionalDictionaryEntries.append(formString)
                    elif formString in baseForm and not formString == baseForm:
                        suffixInstruction = {'delete': baseForm[len(formString):len(baseForm)], 'add': '0', 'condition': '.'}
                        suffixScheme.append(suffixInstruction)
                    else:
                        lengthBaseForm = len(baseForm)
                        delete = ''
                        add = ''
                        for charIndex in range(0, len(formString)):
                            if charIndex < lengthBaseForm:
                                if not formString[charIndex] == baseForm[charIndex]:
                                    delete = baseForm[charIndex:lengthBaseForm]
                                    add = formString[charIndex:len(formString)]
                                    break
                            else:
                                add = formString[charIndex:len(formString)]
                                break
                        suffixInstruction = {'delete': delete, 'add': add, 'condition': '.'}
                        if not (suffixInstruction['add'] == '' and suffixInstruction['delete'] == ''):
                            # in .aff format 'delete no characters' = delete 0
                            if suffixInstruction['delete'] == '':
                                suffixInstruction['delete'] = '0'
                                delete = suffixInstruction['delete']
                            # !! suffix modifications happen before generation of additional forms
                            if MODIFY_SUFFIXES is True:
                                for sufMod in suffixModificationTable:
                                    if partOfSpeech == sufMod['partOfSpeech'] and sufMod['addFormContains'] in suffixInstruction['add']:
                                        suffixInstruction['add'] = suffixInstruction['add'].replace(sufMod['addFormContains'], sufMod['modifiedAddForm'])
                                        add = suffixInstruction['add']
                            suffixScheme.append(suffixInstruction)
                            # add declination word forms for noun and participle forms of verbs and comparative forms of adjectives and adverbs
                            if GENERATE_ADDITIONAL_ISV_DERIVATIVE_WORD_FORMS is True:
                                for suffixTable in addSuffixTableList:
                                    if partOfSpeech == suffixTable['partOfSpeech']:
                                        for addSuffixRow in suffixTable['list']:
                                            if addSuffixRow['baseSuffix'] in suffixInstruction['add']:
                                                for additionalSuffix in addSuffixRow['addSuffixes']:
                                                    suffixScheme.append({'delete': delete, 'add': add.replace(addSuffixRow['baseSuffix'], additionalSuffix), 'condition': '.'})
            if suffixScheme not in suffixSchemeLibrary and not suffixScheme == []:
                suffixSchemeLibrary.append(suffixScheme)
            if suffixScheme in suffixSchemeLibrary:
                dictionaryEntry['flags'].append(suffixSchemeLibrary.index(suffixScheme))
            #if len(additionalDictionaryEntries) > 0:  # not suffixable -> create separate dictionary entries (on -> jego etc.)
            dictionary.append(dictionaryEntry)
            for additionalEntry in additionalDictionaryEntries:
                dictionary.append({'word': additionalEntry, 'flags': []})
        else:
            dictionary.append(dictionaryEntry)
    print(str(len(suffixSchemeLibrary)) + ' suffix schemes')
    print(str(len(dictionary)) + ' dictionary entries')
    # output do .dic file
    with open(OUTPUT_DICTIONARY_NAME + '.dic', 'w') as f:
        print(str(len(dictionary)), file=f)
        for x in range(len(dictionary)):
            entry = dictionary[x]
            combinedFlags = ''
            flags = entry['flags']
            for y in range(len(flags)):
                flagNum = flags[y]
                combinedFlags += determine_long_flag(flagNum)
            if not combinedFlags == '':
                combinedFlags = '/' + combinedFlags
            print(entry['word'] + combinedFlags, file=f)
    # output to .aff file
    with open(OUTPUT_DICTIONARY_NAME + '.aff', 'w') as f:
        with open(AFFIX_FILE_HEADER_NAME, 'r') as header:
            print(header.read(), file=f)
            for index, schemeIterate in enumerate(suffixSchemeLibrary):
                print('SFX ' + determine_long_flag(index) + ' Y ' + str(len(schemeIterate)), file=f)
                for instructionIterate in schemeIterate:
                    print('SFX ' + determine_long_flag(index) + ' ' + instructionIterate['delete'] + ' ' +
                          instructionIterate['add'] + ' ' + instructionIterate['condition'], file=f)
                print('', file=f)
