#!/usr/bin/env zx

import _ from 'lodash';
import cp from 'child_process';

const rootDir = path.join(__dirname, '..');

const dictionaryLocations = {
  'art-x-interslv': ['dict', 'art-x-interslv'],
  'art-Latn-x-interslv': ['dict', 'art-Latn-x-interslv'],
  'art-Latn-x-interslv-etymolog': ['dict', 'art-Latn-x-interslv-etymolog'],
  'art-Cyrl-x-interslv': ['dict', 'art-Cyrl-x-interslv'],
  'cs': ['node_modules/dictionary-cs', 'index'],
  'fr': ['node_modules/dictionary-fr', 'index'],
  'pl': ['node_modules/dictionary-pl', 'index'],
  'ru': ['node_modules/dictionary-ru', 'index'],
};

const langNames = {
  'art-x-interslv': '/combined',
  'art-Latn-x-interslv': '/latin',
  'art-Latn-x-interslv-etymolog': '/etymological',
  'art-Cyrl-x-interslv': '/cyrillic',
  'cs': 'dictionary-cs',
  'fr': 'dictionary-fr',
  'pl': 'dictionary-pl',
  'ru': 'dictionary-ru',
};

function isWhitespace(c) {
    return c === ' '
        || c === '\n'
        || c === '\t'
        || c === '\r'
        || c === '\f'
        || c === '\v'
        || c === '\u00a0'
        || c === '\u1680'
        || c === '\u2000'
        || c === '\u200a'
        || c === '\u2028'
        || c === '\u2029'
        || c === '\u202f'
        || c === '\u205f'
        || c === '\u3000'
        || c === '\ufeff'
}

function countNonWhitespace(str) {
  let i, n = str.length, r = 0;

  for (i = 0; i < n; i++) {
    if (!isWhitespace(str[i])) {
      r++;
    }
  }

  return r;
}

function benchmarkText(lang, textId = 'le-petite-prince') {
  const DICPATH = path.join(rootDir, dictionaryLocations[lang][0]);
  const dictionaryName = dictionaryLocations[lang][1];
  const textFile = path.join(__dirname, `samples/${textId}/${lang}.txt`);

  const a = process.hrtime.bigint();
  cp.execSync(`hunspell -d ${dictionaryName} -l ${textFile}`, {
    stdio: 'ignore',
    env: {
      ...process.env,
      DICPATH,
    },
  });
  const b = process.hrtime.bigint();

  const time = 1E-9 * Number(b - a);
  const nws = countNonWhitespace(fs.readFileSync(textFile, 'utf8'))

  return Math.floor(nws / time);
}

console.log('Language\tSpeed');
for (const lang of Object.keys(langNames)) {
  console.log(langNames[lang] + '\t' + benchmarkText(lang));
}
