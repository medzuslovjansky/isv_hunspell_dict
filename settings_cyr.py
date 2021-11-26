
# --OPTIONS-- (DEFAULT VALUES)
# MAIN
OUTPUT_DICTIONARY_NAME = 'dictionaries/isv_cyr_hunspell_dict'
OPENCORPORAXML_FILE_NAME = 'input/opencorporaxml/out_isv_cyr.xml'
ACCEPTABLE_WORD_CHARS = '-ЈјЦцУуКкЕеНнГгШшЗзХхФфЫыВвАаПпРрОоЛлДдЖжЄєЧчСсМмИиТтЬьБбЊњЉљ '
AFFIX_FLAG_NAME_CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_cyrillic.txt'
# WORD FORM GENERATION
GENERATE_ADDITIONAL_ISV_DERIVATIVE_WORD_FORMS = True
MODIFY_SUFFIXES = True
ADDITIONAL_ISV_FORMS_FILE_NAMES = 'json_additional/cyr/isv_cyr_additional'
# EXCEPTIONS
REMOVE_FINAL_SPACES_IN_WORDS = True
SPECIAL_HANDLING_OF_ISV_REFLEXIVE_VERBS = True
REFLEXIVE_PARTICLE = ' се'
SPECIAL_HANDLING_OF_ISV_NEGATIVE_VERBS = True
NEGATIVE_PARTICLE = 'не '
SPECIAL_HANDLING_OF_ISV_ADJECTIVES_WITH_ADVERBS = True
ADVERB_ENDING = 'о '
CORRECT_INDIVIDUAL_ERROR_WORDS = True
SPLIT_MISC_SPACED_WORDS = True
ADD_WORDS_FROM_FILE = True
ADD_WORDS_FILE_NAME = 'input/addwordlists/isv_cyr_add_words.txt'
# COMPOUNDING
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_END_OF_COMPOUNDS = True  # napr. hladnokrovny
SPECIAL_ISV_ALLOW_ADJECTIVES_AT_START_OF_COMPOUNDS = True
ISV_COMPARATIVE_ADJF_SUFFIX = 'ши'
ISV_COMPARATIVE_ADVB_SUFFIX = 'је'
SPECIAL_ISV_ALLOW_NOUNS_AT_START_OF_COMPOUNDS = True
SPECIAL_ISV_ALLOW_NOUNS_AT_END_OF_COMPOUNDS = True
ISV_COMPOUND_CHARACTER_HARD = 'о'
ISV_COMPOUND_CHARACTER_SOFT = 'е'
ISV_SOFT_CONSONANTS = 'шжчцјьњљ'
ISV_VOWELS = 'аеиоуыє'
ISV_ADJECTIVE_FALSE_COMPOUND_SUFFIX = 'ого'

addSuffixTableList = []
addSuffixTableVerb = {'partOfSpeech': 'VERB', 'list': []}
addSuffixTableVerb['list'].append({'baseSuffix': 'нје', 'addSuffixes': ['нја', 'нју', 'нјем', 'ниј', 'нјам', 'нјами', 'нјах']})
addSuffixTableVerb['list'].append({'baseSuffix': 'учи',
                       'addSuffixes': ['учего', 'учему', 'учим', 'учем', 'учих', 'учими']})
addSuffixTableVerb['list'].append({'baseSuffix': 'уча',
                       'addSuffixes': ['учу', 'учеј', 'учеју']})
addSuffixTableVerb['list'].append({'baseSuffix': 'мы',
                       'addSuffixes': ['мого', 'мому', 'мым', 'мом', 'мо']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ма',
                       'addSuffixes': ['му', 'мој', 'моју', 'ми', 'ме', 'мых', 'мым', 'мыми']})
addSuffixTableVerb['list'].append({'baseSuffix': 'вши',
                       'addSuffixes': ['вшего', 'вшему', 'вшим', 'вшем', 'вших', 'вшими']})
addSuffixTableVerb['list'].append({'baseSuffix': 'вша',
                       'addSuffixes': ['вшу', 'вшеј', 'вшеју']})
addSuffixTableVerb['list'].append({'baseSuffix': 'ны',
                       'addSuffixes': ['ного', 'ному', 'ным', 'ном', 'ни', 'не', 'ных', 'ными']})
addSuffixTableVerb['list'].append({'baseSuffix': 'на',
                       'addSuffixes': ['ну', 'ној', 'ноју']})


addSuffixTableAdjective = {'partOfSpeech': 'ADJF', 'list': []}
addSuffixTableAdjective['list'].append({'baseSuffix': 'ши',
                       'addSuffixes': ['шего', 'шему', 'шим', 'шем', 'ше', 'ша', 'шу', 'шеј', 'шеју', 'ших', 'шим', 'шими']})

addSuffixTableList.append(addSuffixTableVerb)
addSuffixTableList.append(addSuffixTableAdjective)

suffixModificationTable = []
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'ши', 'modifiedAddForm': 'ши/zz'})
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'је', 'modifiedAddForm': 'је/zz'})

suffixCompoundModificationTable = []
suffixCompoundModificationTable.append({'partOfSpeech': 'VERB', 'addFormContains': 'нје', 'modifiedAddForm': 'нје/xPxE'})

individualWordCorrectionTable = []
individualWordCorrectionTable.append({'word': 'хектар ха', 'correctWord': 'хектар'})

