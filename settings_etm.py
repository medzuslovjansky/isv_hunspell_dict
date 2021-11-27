
# --OPTIONS-- (DEFAULT VALUES)
# MAIN
OUTPUT_DICTIONARY_NAME = 'dictionaries/isv_etm_hunspell_dict'
OPENCORPORAXML_FILE_NAME = 'input/opencorporaxml/out_isv_etm.xml'
ACCEPTABLE_WORD_CHARS = '-ABCDEFGHIJKLMNOPQRSTUVWXYZčČžŽěĚšŠabcdefghijklmnopqrstuvwxyzđĐśŚęĘŕŔřŘťŤųŲåÅďĎľĽźŹćĆńŃȯȮėĖòÒèÈ '
AFFIX_FLAG_NAME_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_etymologicallatin.txt'
# WORD FORM GENERATION
GENERATE_ADDITIONAL_ISV_DERIVATIVE_WORD_FORMS = True
MODIFY_SUFFIXES = True
ADDITIONAL_ISV_FORMS_FILE_NAMES = 'json_additional/etm/isv_etm_additional'
# EXCEPTIONS
REMOVE_FINAL_SPACES_IN_WORDS = True
SPECIAL_HANDLING_OF_ISV_REFLEXIVE_VERBS = True
REFLEXIVE_PARTICLE = ' sę'
SPECIAL_HANDLING_OF_ISV_NEGATIVE_VERBS = True
NEGATIVE_PARTICLE = 'ne '
SPECIAL_HANDLING_OF_ISV_ADJECTIVES_WITH_ADVERBS = True
ADVERB_ENDING = 'o '
CORRECT_INDIVIDUAL_ERROR_WORDS = True
SPLIT_MISC_SPACED_WORDS = True
ADD_WORDS_FROM_FILE = True
ADD_WORDS_FILE_NAME = 'input/addwordlists/isv_etm_add_words.txt'
# COMPOUNDING
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_END_OF_COMPOUNDS = True  # napr. hladnokrovny
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_START_OF_COMPOUNDS = True
ISV_COMPARATIVE_ADJF_SUFFIX = 'ši'
ISV_COMPARATIVE_ADVB_SUFFIX = 'je'
SPECIAL_ISV_ALLOW_NOUNS_AT_START_OF_COMPOUNDS = True
SPECIAL_ISV_ALLOW_NOUNS_AT_END_OF_COMPOUNDS = True
ISV_COMPOUND_CHARACTER_HARD = 'o'
ISV_COMPOUND_CHARACTER_SOFT = 'e'
ISV_SOFT_CONSONANTS = 'šžčcjćđ'
ISV_VOWELS = 'aeiouyěęųȯėåòè'
ISV_ADJECTIVE_FALSE_COMPOUND_SUFFIX = 'ogo'

addSuffixTableList = []
addSuffixTableVerb = {'partOfSpeech': 'VERB', 'list': []}
addSuffixTableVerb['list'].append({'baseSuffix': 'ńje', 'addSuffixes': ['ńja', 'ńju', 'ńjem', 'nij', 'ńjam', 'ńjami', 'ńjah']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ųći',
                       'addSuffixes': ['ųćego', 'ųćemu', 'ųćim', 'ųćem', 'ųćih', 'ųćimi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ųča',
                       'addSuffixes': ['ųčų', 'ųčej', 'ųčejų']})
addSuffixTableVerb['list'].append({'baseSuffix': 'my',
                       'addSuffixes': ['mogo', 'momu', 'mym', 'mom', 'mo']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ma',
                       'addSuffixes': ['mų', 'moj', 'mojų', 'mi', 'me', 'myh', 'mym', 'mymi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'vši',
                       'addSuffixes': ['všego', 'všemu', 'všim', 'všem', 'vših', 'všimi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'vša',
                       'addSuffixes': ['všų', 'všej', 'všejų']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ny',
                       'addSuffixes': ['nogo', 'nomu', 'nym', 'nom', 'ni', 'ne', 'nyh', 'nymi']})
addSuffixTableVerb['list'].append({'baseSuffix': 'na',
                       'addSuffixes': ['nų', 'noj', 'nojų']})


addSuffixTableAdjective = {'partOfSpeech': 'ADJF', 'list': []}
addSuffixTableAdjective['list'].append({'baseSuffix': 'ši',
                       'addSuffixes': ['šego', 'šemu', 'šim', 'šem', 'še', 'ša', 'šų', 'šej', 'šejų', 'ših', 'šim', 'šimi']})

addSuffixTableList.append(addSuffixTableVerb)
addSuffixTableList.append(addSuffixTableAdjective)

suffixModificationTable = []
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'ši', 'modifiedAddForm': 'ši/zz'})
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'je', 'modifiedAddForm': 'je/zz'})

suffixCompoundModificationTable = []
suffixCompoundModificationTable.append({'partOfSpeech': 'VERB', 'addFormContains': 'ńje', 'modifiedAddForm': 'ńje/xPxE'})

individualWordCorrectionTable = []
individualWordCorrectionTable.append({'word': 'hektar ha', 'correctWord': 'hektar'})

