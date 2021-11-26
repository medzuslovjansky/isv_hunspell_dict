
# --OPTIONS-- (DEFAULT VALUES)
# MAIN
OUTPUT_DICTIONARY_NAME = 'dictionaries/isv_lat_hunspell_dict'
OPENCORPORAXML_FILE_NAME = 'input/opencorporaxml/out_isv_lat.xml'
ACCEPTABLE_WORD_CHARS = '-ABCDEFGHIJKLMNOPQRSTUVWXYZčČžŽěĚšŠabcdefghijklmnopqrstuvwxyz '
AFFIX_FLAG_NAME_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_standardlatin.txt'
# WORD FORM GENERATION
GENERATE_ADDITIONAL_ISV_DERIVATIVE_WORD_FORMS = True
MODIFY_SUFFIXES = True
ADDITIONAL_ISV_FORMS_FILE_NAMES = 'json_additional/lat/isv_lat_additional'
# EXCEPTIONS
REMOVE_FINAL_SPACES_IN_WORDS = True
SPECIAL_HANDLING_OF_ISV_REFLEXIVE_VERBS = True
REFLEXIVE_PARTICLE = ' se'
SPECIAL_HANDLING_OF_ISV_NEGATIVE_VERBS = True
NEGATIVE_PARTICLE = 'ne '
SPECIAL_HANDLING_OF_ISV_ADJECTIVES_WITH_ADVERBS = True
ADVERB_ENDING = 'o '
CORRECT_INDIVIDUAL_ERROR_WORDS = True
SPLIT_MISC_SPACED_WORDS = True
ADD_WORDS_FROM_FILE = True
ADD_WORDS_FILE_NAME = 'input/addwordlists/isv_lat_add_words.txt'
# COMPOUNDING
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_END_OF_COMPOUNDS = True  # napr. hladnokrovny
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_START_OF_COMPOUNDS = True
ISV_COMPARATIVE_ADJF_SUFFIX = 'ši'
ISV_COMPARATIVE_ADVB_SUFFIX = 'je'
SPECIAL_ISV_ALLOW_NOUNS_AT_START_OF_COMPOUNDS = True
SPECIAL_ISV_ALLOW_NOUNS_AT_END_OF_COMPOUNDS = True
ISV_COMPOUND_CHARACTER_HARD = 'o'
ISV_COMPOUND_CHARACTER_SOFT = 'e'
ISV_SOFT_CONSONANTS = 'šžčcj'
ISV_VOWELS = 'aeiouyě'
ISV_ADJECTIVE_FALSE_COMPOUND_SUFFIX = 'ogo'

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

