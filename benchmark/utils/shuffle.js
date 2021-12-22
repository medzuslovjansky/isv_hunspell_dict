const _ = require('lodash');
const fs = require('fs');

const fin = process.argv[2];
const fout = process.argv[3];

const text = fs.readFileSync(fin, 'utf8');

const add_letter = (word) => {
  const char = _.sample(word.split(''));
  const index = _.random(word.length);
  return [word.slice(0, index), char, word.slice(index)].join('');
};

const remove_letter = (word) => {
  const index = _.random(word.length - 1);
  return [word.slice(0, index - 1), word.slice(index)].join('');
};

const swap_letters = (word) => {
  if (word.length < 2) {
    return word;
  }

  let idx1 = _.random(word.length - 1);
  let idx2;
  do {
    idx2 = _.random(word.length - 1);
  } while (idx1 === idx2);

  if (idx2 < idx1) {
    [idx1, idx2] = [idx2, idx1];
  }

  return word.substr(0, idx1)
    + word[idx2]
    + word.substring(idx1 + 1, idx2)
    + word[idx1]
    + word.substr(idx2 + 1);
};

const mutate = (word) => _.sample([
  add_letter,
  remove_letter,
  swap_letters,
])(word);

const newText = text.replace(/\p{Letter}+/ug, match => {
  return Math.random() < 0.2 ? mutate(match) : match;
});

fs.writeFileSync(fout, newText);
