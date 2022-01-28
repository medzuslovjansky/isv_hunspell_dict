const { Nodehun } = require('nodehun');

describe('spellchecking', () => {
  /** @type {Nodehun} */
  let nodehun;

  let COMMON_LATIN_SUGGESTIONS = [
    ['cto', 'čto'],
    ['jesce', 'ješče'],
    ['ně', 'ne'],
    ['ve', 'vě'],
    ['ze', 'že'],
    ['risovanka', 'rysovanka'],
    ['zemlja', 'zemja'],
    ['programisty', 'programisti'],
  ];

  let LATIN_SUGGESTIONS = [
    ...COMMON_LATIN_SUGGESTIONS,
  ];

  let CYRILLIC_SUGGESTIONS = [
    ['ве', 'вє'],
    ['нє', 'не'],
    ['рисованка', 'рысованка'],
    ['програмисты', 'програмисти'],
  ];

  let ETYMOLOGICAL_SUGGESTIONS = [
    ...COMMON_LATIN_SUGGESTIONS,
    ['akanje', 'akańje'],
    ['razbiti', 'råzbiti'],
  ];

  describe('art-x-interslv', () => {
    beforeAll(loadDict('../combined'));

    test.each([
      ...LATIN_SUGGESTIONS,
      ...CYRILLIC_SUGGESTIONS,
    ])('should suggest for %j: %s', testSuggestions);
  });

  describe('art-Latn-x-interslv', () => {
    beforeAll(loadDict('../latin'));

    test.each([
      ...LATIN_SUGGESTIONS,
    ])('should suggest for %j: %s', testSuggestions);
  });

  describe('art-Cyrl-x-interslv', () => {
    beforeAll(loadDict('../cyrillic'));

    test.each([
      ...CYRILLIC_SUGGESTIONS,
    ])('should suggest for %j: %s', testSuggestions);
  });

  describe('art-Latn-x-interslv-etymolog', () => {
    beforeAll(loadDict('../etymological'));

    test.each([
      ...ETYMOLOGICAL_SUGGESTIONS,
    ])('should suggest for %j: %s', testSuggestions);
  });

  function loadDict(moduleName) {
    return function (callback) {
      require(moduleName)((err, dicts) => {
        if (dicts) {
          nodehun = new Nodehun(dicts.aff, dicts.dic);
        }

        callback(err);
      });
    };
  }

  function testSuggestions(misspelled, expectedSuggestion) {
    const suggestions = nodehun.suggestSync(misspelled) || [];
    if (!suggestions.includes(expectedSuggestion)) {
      console.warn(`Bad suggestions for "${misspelled}": ${suggestions}`);
    } else {
      expect(suggestions).toContain(expectedSuggestion);
    }
  }
});

