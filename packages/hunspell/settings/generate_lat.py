
# --OPTIONS--
# MAIN
OUTPUT_DICTIONARY_NAME = 'output/dictionaries/Medzuslovjansky_LatinicaStandard'
OPENCORPORAXML_FILE_NAME = 'input/opencorporaxml/out_isv_lat.xml'
ACCEPTABLE_WORD_CHARS = '-ABCDEFGHIJKLMNOPQRSTUVWXYZčČžŽěĚšŠabcdefghijklmnopqrstuvwxyz '
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_standardlatin.txt'
# WORD FORM GENERATION
ADDITIONAL_ISV_FORMS_FILE_NAMES = 'output/json_additional/lat/isv_lat_additional'
# EXCEPTIONS
REFLEXIVE_PARTICLE = ' se'
NEGATIVE_PARTICLE = 'ne '
ADVERB_ENDING = 'o '
ADD_WORDS_FILE_NAME = 'input/addwordlists/isv_lat_add_words.txt'
# COMPOUNDING
ISV_COMPARATIVE_ADJF_SUFFIX = 'ši'
ISV_COMPARATIVE_ADVB_SUFFIX = 'je'
ISV_COMPOUND_CHARACTER_HARD = 'o'
ISV_COMPOUND_CHARACTER_SOFT = 'e'
ISV_SOFT_CONSONANTS = 'šžčcj'
ISV_VOWELS = 'aeiouyě'
ISV_ADJECTIVE_FALSE_COMPOUND_SUFFIX = 'ogo'
# DICTIONARY COMBINING


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

