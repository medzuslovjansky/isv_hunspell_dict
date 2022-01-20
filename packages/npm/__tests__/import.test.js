const fs = require('fs');

describe('@interslavic/dictionary', () => {
  test.each([
    ['.'],
    ['combined'],
    ['etymological'],
    ['latin'],
    ['cyrillic'],
  ])('should export: /%s', (modulePath, done) => {
    const fn = require('../' + modulePath);

    fn((err, { aff, dic }) => {
      expect(aff).toBeInstanceOf(Buffer);
      expect(dic).toBeInstanceOf(Buffer);
      done();
    });
  });

  test.each([
    ['art-x-interslv'],
    ['art-Latn-x-interslv'],
    ['art-Latn-x-interslv-etymolog'],
    ['art-Cyrl-x-interslv'],
  ])('should have DIC and AFF for "%s" BCP 47 code', (lang) => {
    expect(fs.existsSync(`${lang}.dic`)).toBe(true);
    expect(fs.existsSync(`${lang}.aff`)).toBe(true);
  });
});
