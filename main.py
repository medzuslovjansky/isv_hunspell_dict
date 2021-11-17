import xml.etree.ElementTree as ET

flagsLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def determineLongFlag(number):
    letterIndex1 = 0
    letterIndex2 = 0
    while (letterIndex1 * len(flagsLetters) + letterIndex2) < number:
        letterIndex2 += 1
        if letterIndex2 >= len(flagsLetters):
            letterIndex1 += 1
            letterIndex2 = 0
        if letterIndex1 >= len(flagsLetters):
            raise RuntimeError('Ran out of flags')
    return flagsLetters[letterIndex1] + flagsLetters[letterIndex2]

DICTIONARY_NAME = 'isv_lat_hunspell_dict'
XML_FILE_NAME = 'out_isv_lat.xml'
with open(XML_FILE_NAME, 'r') as xml_file:
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
        reducedForms = []
        dictionaryEntry = {'word': '', 'flags': []}
        additionalDictionaryEntries = []
        suffixScheme = []
        for form in lemma:
            formString = form.attrib['t']  # read form
            formString = ''.join(char for char in formString if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYčČžŽěĚšŠabcdefghijklmnopqrstuvwxy ')
            if reducedForms.count(formString) == 0 and not formString == '':
                reducedForms.append(formString)
        baseForm = ''
        if len(reducedForms) > 0:  # if any form
            baseForm = reducedForms[0]
            dictionaryEntry['word'] += baseForm
        if len(reducedForms) > 1:  # if more than 1 form
            for index, formString in enumerate(reducedForms):
                if not index == 0:
                    if not formString[0] == baseForm[0]:
                        additionalDictionaryEntries.append(formString)
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
                            if suffixInstruction['delete'] == '':
                                suffixInstruction['delete'] = '0'
                            suffixScheme.append(suffixInstruction)
            if suffixScheme not in suffixSchemeLibrary and not suffixScheme == []:
                suffixSchemeLibrary.append(suffixScheme)
            if suffixScheme in suffixSchemeLibrary:
                dictionaryEntry['flags'].append(suffixSchemeLibrary.index(suffixScheme))
            if len(additionalDictionaryEntries) > 0:  # more than 1 form, but couldn't build a suffix scheme
                if ('o ' + additionalDictionaryEntries[0]) in dictionaryEntry['word']:
                    splitWords = dictionaryEntry['word'].split()
                    additionalDictionaryEntries.append(splitWords[0])
                    dictionaryEntry['word'] = splitWords[1]
                    try:
                        additionalDictionaryEntries.remove(dictionaryEntry['word'])
                    except ValueError:
                        pass
                if 'ne ' in dictionaryEntry['word']:
                    additionalDictionaryEntries = []
            dictionary.append(dictionaryEntry)
            for additionalEntry in additionalDictionaryEntries:
                dictionary.append({'word': additionalEntry, 'flags': []})
    print(str(len(suffixSchemeLibrary)) + ' suffix schemes')
    print(str(len(dictionary)) + ' dictionary entries')
    with open(DICTIONARY_NAME + '.dic', 'w') as f:
        print(str(len(dictionary)), file=f)
        for x in range(len(dictionary)):
            entry = dictionary[x]
            combinedFlags = ''
            flags = entry['flags']
            for y in range(len(flags)):
                flagNum = flags[y]
                combinedFlags += determineLongFlag(flagNum)
            if not combinedFlags == '':
                combinedFlags = '/' + combinedFlags
            print(entry['word'] + combinedFlags, file=f)
    with open(DICTIONARY_NAME + '.aff', 'w') as f:
        with open('affix_file_header.txt', 'r') as header:
            print(header.read(), file=f)
            for index, schemeIterate in enumerate(suffixSchemeLibrary):
                print('SFX ' + determineLongFlag(index) + ' Y ' + str(len(schemeIterate)), file=f)
                for instructionIterate in schemeIterate:
                    print('SFX ' + determineLongFlag(index) + ' ' + instructionIterate['delete'] + ' ' + instructionIterate['add'] + ' ' + instructionIterate['condition'], file=f)
                print('', file=f)




