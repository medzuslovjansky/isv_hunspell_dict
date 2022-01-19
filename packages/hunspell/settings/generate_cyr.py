
# --OPTIONS--
# MAIN
OUTPUT_DICTIONARY_NAME = 'output/dictionaries/Medzuslovjansky_Kirilica'
OPENCORPORAXML_FILE_NAME = 'input/opencorporaxml/out_isv_cyr.xml'
ACCEPTABLE_WORD_CHARS = '-ЈјЦцУуКкЕеНнГгШшЗзХхФфЫыВвАаПпРрОоЛлДдЖжЄєЧчСсМмИиТтЬьБбЊњЉљ '
AFFIX_FILE_HEADER_NAME = 'input/affixheaders/affix_file_header_cyrillic.txt'
# WORD FORM GENERATION
ADDITIONAL_ISV_FORMS_FILE_NAMES = 'output/json_additional/cyr/isv_cyr_additional'
# EXCEPTIONS
REFLEXIVE_PARTICLE = ' се'
NEGATIVE_PARTICLE = 'не '
ADVERB_ENDING = 'о '
ADD_WORDS_FILE_NAME = 'input/addwordlists/isv_cyr_add_words.txt'
# COMPOUNDING
ISV_COMPARATIVE_ADJF_SUFFIX = 'ши'
ISV_COMPARATIVE_ADVB_SUFFIX = 'је'
ISV_COMPOUND_CHARACTER_HARD = 'о'
ISV_COMPOUND_CHARACTER_SOFT = 'е'
ISV_SOFT_CONSONANTS = 'шжчцјьњљ'
ISV_VOWELS = 'аеиоуыє'
ISV_ADJECTIVE_FALSE_COMPOUND_SUFFIX = 'ого'
# DICTIONARY COMBINING


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
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'ши', 'modifiedAddForm': 'ши/zx'})
suffixModificationTable.append({'partOfSpeech': 'ADJF', 'addFormContains': 'је', 'modifiedAddForm': 'је/zx'})

suffixCompoundModificationTable = []
suffixCompoundModificationTable.append({'partOfSpeech': 'VERB', 'addFormContains': 'нје', 'modifiedAddForm': 'нје/xPxE'})

individualWordCorrectionTable = []
individualWordCorrectionTable.append({'word': 'хектар ха', 'correctWord': 'хектар'})

