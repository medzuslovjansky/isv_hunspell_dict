import lxml.etree as ET
import json

# --OPTIONS--
# MAIN
OUTPUT_DICTIONARY_NAME = 'isv_lat_hunspell_dict'
OPENCORPORAXML_FILE_NAME = 'out_isv_lat.xml'
ACCEPTABLE_WORD_CHARS = '-ABCDEFGHIJKLMNOPQRSTUVWXYZčČžŽěĚšŠabcdefghijklmnopqrstuvwxyz '
AFFIX_FLAG_NAME_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
AFFIX_FILE_HEADER_NAME = 'affix_file_header_standardlatin.txt'
# WORD FORM GENERATION
GENERATE_ADDITIONAL_ISV_DERIVATIVE_WORD_FORMS = True
MODIFY_SUFFIXES = True
ADDITIONAL_ISV_FORMS_FILE_NAMES = 'isv_lat_additional'
# EXCEPTIONS
REMOVE_FINAL_SPACES_IN_WORDS = True
SPECIAL_HANDLING_OF_ISV_REFLEXIVE_VERBS = True
SPECIAL_HANDLING_OF_ISV_NEGATIVE_VERBS = True
SPECIAL_HANDLING_OF_ISV_ADJECTIVES_WITH_ADVERBS = True
CORRECT_INDIVIDUAL_ERROR_WORDS = True
SPLIT_MISC_SPACED_WORDS = True
# COMPOUNDING
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_END_OF_COMPOUNDS = True  # napr. hladnokrovny
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_START_OF_COMPOUNDS = True
ISV_COMPARATIVE_ADJF_SUFFIX = 'ši'
ISV_COMPARATIVE_ADVB_SUFFIX = 'je'
SPECIAL_ISV_ALLOW_NOUNS_AT_START_OF_COMPOUNDS = True
SPECIAL_ISV_ALLOW_NOUNS_AT_END_OF_COMPOUNDS = True
ISV_NOUN_CONNECTING_CHARACTER_HARD = 'o'
ISV_NOUN_CONNECTING_CHARACTER_SOFT = 'e'
ISV_SOFT_CONSONANTS = 'šžčcj'
ISV_VOWELS = 'aeiouyě'

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

suffixCompoundModificationTable = []
suffixCompoundModificationTable.append({'partOfSpeech': 'VERB', 'addFormContains': 'nje', 'modifiedAddForm': 'nje/xPxE'})

individualWordCorrectionTable = []
individualWordCorrectionTable.append({'word': 'hektar ha', 'correctWord': 'hektar'})


with open(ADDITIONAL_ISV_FORMS_FILE_NAMES + '_derivative_forms.json', 'w', encoding='utf8') as f:
    print(json.dumps(addSuffixTableList, indent=1, ensure_ascii=False), file=f)

with open(ADDITIONAL_ISV_FORMS_FILE_NAMES + '_modified_suffixes.json', 'w', encoding='utf8') as f:
    print(json.dumps(suffixModificationTable, indent=1, ensure_ascii=False), file=f)

with open(ADDITIONAL_ISV_FORMS_FILE_NAMES + '_modified_suffixes_compound.json', 'w', encoding='utf8') as f:
    print(json.dumps(suffixCompoundModificationTable, indent=1, ensure_ascii=False), file=f)

with open(ADDITIONAL_ISV_FORMS_FILE_NAMES + '_word_corrections.json', 'w', encoding='utf8') as f:
    print(json.dumps(individualWordCorrectionTable, indent=1, ensure_ascii=False), file=f)

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


dictionary = []
suffixSchemeLibrary = []
lemmasMovedToEnd = []

with open('isv_lat_add_words.txt', 'r') as f:
    lines = f.readlines()
    lines = [line.rstrip() for line in lines]
    for line in lines:
        dictionary.append({'word': line, 'flags': []})

with open(OPENCORPORAXML_FILE_NAME, 'r') as xml_file:
    tree = ET.parse(xml_file)
root = tree.getroot()
lemmata = root[1]
if not lemmata.tag == 'lemmata':
    print('XML Structure error')
else:
    for lemma in lemmata:
        partOfSpeech = ''
        numeralIsOrd = False
        # part of speech attributes are capitalised in OpenCorporaXML format, no others are
        for baseFormAttribContainer in lemma[0]:
            attribute = baseFormAttribContainer.attrib['v']
            if attribute.isupper():
                partOfSpeech = attribute
            if attribute == 'ord':
                numeralIsOrd = True
        reducedForms = []
        dictionaryEntry = {'word': '', 'flags': []}
        additionalDictionaryEntries = []
        suffixScheme = []
        rememberBadAdjectiveAdverbCombination = ''
        for form in lemma:
            formString = form.attrib['t']  # read form
            formString = ''.join(
                char for char in formString if char in ACCEPTABLE_WORD_CHARS)
            if REMOVE_FINAL_SPACES_IN_WORDS is True and not formString == '':
                while formString[len(formString)-1] == ' ':
                    formString = formString[0:len(formString)-1]
            if CORRECT_INDIVIDUAL_ERROR_WORDS is True:
                for errorWord in individualWordCorrectionTable:
                    if formString == errorWord['word']:
                        formString = errorWord['correctWord']
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
            if SPLIT_MISC_SPACED_WORDS is True and ' ' in baseForm:
                if lemma not in lemmasMovedToEnd:
                    lemmata.append(lemma)
                    lemmasMovedToEnd.append(lemma)
                    continue
                if lemma in lemmasMovedToEnd:
                    splitBaseForm = baseForm.split()
                    foundForms = [False] * len(splitBaseForm)
                    for index, individualWord in enumerate(splitBaseForm):
                        for iterateDictionaryEntry in dictionary:
                            if individualWord == iterateDictionaryEntry['word']:
                                foundForms[index] = True
                    if foundForms == [True] * len(splitBaseForm):
                        continue
                    else:
                        for index, individualWord in enumerate(splitBaseForm):
                            if foundForms[index] == False:
                                dictionary.append({'word': individualWord, 'flags': []})
                        continue
        if len(reducedForms) > 1:  # if more than 1 form
            for index, formString in enumerate(reducedForms):
                if not index == 0:  # if not base form -> try to generate suffix
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
                            if SPECIAL_ISV_ALLOW_ADJECTIVES_AT_START_OF_COMPOUNDS:
                                if partOfSpeech == 'ADJF' or (partOfSpeech == 'NUMR' and numeralIsOrd is True):
                                    if ISV_COMPARATIVE_ADVB_SUFFIX not in suffixInstruction['add'] and ISV_COMPARATIVE_ADJF_SUFFIX not in suffixInstruction['add']:
                                        if suffixInstruction['add'][len(suffixInstruction['add']) - 1] == 'o' and 'ogo' not in suffixInstruction['add']:
                                            if '/' not in suffixInstruction['add']:
                                                suffixInstruction['add'] = suffixInstruction['add'] + '/xB'
                                            else:
                                                suffixInstruction['add'] = suffixInstruction['add'] + 'xB'
                                        #if suffixInstruction['add'][len(suffixInstruction['add']) - 1] == 'e':
                                            #checkFor = baseForm[0:lengthBaseForm-len(suffixInstruction['delete'])]
                                            #modifiedCheckForSuffix = add[0:len(add)-1] + 'o'
                                            #checkFor = checkFor + modifiedCheckForSuffix
                                            #if checkFor not in reducedForms:
                                                #print(formString)
                                add = suffixInstruction['add']
                            if SPECIAL_ISV_ALLOW_ADJECTIVES_AT_END_OF_COMPOUNDS:
                                if partOfSpeech == 'ADJF' or (partOfSpeech == 'NUMR' and numeralIsOrd is True):
                                    if ISV_COMPARATIVE_ADVB_SUFFIX not in suffixInstruction['add'] and ISV_COMPARATIVE_ADJF_SUFFIX not in suffixInstruction['add']:
                                        if '/' not in suffixInstruction['add']:
                                            suffixInstruction['add'] = suffixInstruction['add'] + '/xPxE'
                                        else:
                                            suffixInstruction['add'] = suffixInstruction['add'] + 'xPxE'
                                add = suffixInstruction['add']
                            if SPECIAL_ISV_ALLOW_NOUNS_AT_END_OF_COMPOUNDS:
                                if partOfSpeech == 'NOUN':
                                    if '/' not in suffixInstruction['add']:
                                        suffixInstruction['add'] = suffixInstruction['add'] + '/xPxE'
                                    else:
                                        suffixInstruction['add'] = suffixInstruction['add'] + 'xPxE'
                                add = suffixInstruction['add']
                            if MODIFY_SUFFIXES is True:
                                for sufMod in suffixModificationTable:
                                    if partOfSpeech == sufMod['partOfSpeech'] and sufMod['addFormContains'] in suffixInstruction['add']:
                                        suffixInstruction['add'] = suffixInstruction['add'].replace(sufMod['addFormContains'], sufMod['modifiedAddForm'])
                                        add = suffixInstruction['add']
                                if SPECIAL_ISV_ALLOW_NOUNS_AT_END_OF_COMPOUNDS:
                                    for sufMod in suffixCompoundModificationTable:
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
                else:
                    if SPECIAL_ISV_ALLOW_ADJECTIVES_AT_END_OF_COMPOUNDS and partOfSpeech == 'ADJF':
                        suffixInstruction = {'delete': '0', 'add': '0/xPxE', 'condition': '.'}
                        suffixScheme.append(suffixInstruction)
                    if SPECIAL_ISV_ALLOW_NOUNS_AT_END_OF_COMPOUNDS and partOfSpeech == 'NOUN':
                        suffixInstruction = {'delete': '0', 'add': '0/xPxE', 'condition': '.'}
                        suffixScheme.append(suffixInstruction)
                    if SPECIAL_ISV_ALLOW_NOUNS_AT_START_OF_COMPOUNDS and partOfSpeech == 'NOUN':
                        if formString[len(formString)-1] not in ISV_SOFT_CONSONANTS and formString[len(formString)-1] not in ISV_VOWELS:
                            suffixInstruction = {'delete': '0', 'add': 'o/xPxBxO', 'condition': '.'}
                            suffixScheme.append(suffixInstruction)
                        if formString[len(formString) - 1] in ISV_SOFT_CONSONANTS and formString[len(formString) - 1] not in ISV_VOWELS:
                            suffixInstruction = {'delete': '0', 'add': 'e/xPxBxO', 'condition': '.'}
                            suffixScheme.append(suffixInstruction)
                        if formString[len(formString) - 1] in ISV_VOWELS:
                            lastChar = formString[len(formString) - 1]
                            if formString[len(formString) - 2] not in ISV_SOFT_CONSONANTS and formString[len(formString) - 2] not in ISV_VOWELS:
                                suffixInstruction = {'delete': lastChar, 'add': 'o/xPxBxO', 'condition': '.'}
                                suffixScheme.append(suffixInstruction)
                            if formString[len(formString) - 2] in ISV_SOFT_CONSONANTS and formString[len(formString) - 2] not in ISV_VOWELS:
                                suffixInstruction = {'delete': lastChar, 'add': 'e/xPxBxO', 'condition': '.'}
                                suffixScheme.append(suffixInstruction)
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
