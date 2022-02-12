#!/usr/bin/env zx

import { mutate } from './utils/_mutate.mjs';

const fin = argv.i;
const fout = argv.o;
const probability = Number(argv.p);

function validateArgs() {
  let valid = true;

  if (!fin) {
    console.warn(chalk.yellow('Please specify -i <input> file!'));
    valid = false;
  }

  if (!fout) {
    console.warn(chalk.yellow('Please specify -o <output> file!'));
    valid = false;
  }

  if (Number.isNaN(probability)) {
    console.warn(chalk.yellow('Please specify -p <probability> fractional number (0..1] !'));
    valid = false;
  }

  if (!(probability > 0 && probability <= 1)) {
    console.warn(chalk.yellow('Invalid -p <probability> number, should be between 0 and 1: ' + probability));
    valid = false;
  }

  return valid;
}

if (Object.keys(argv).length <= 1) {
  console.log(chalk.bold`${path.basename(__filename)} - the CLI tool to introduce spelling errors`);
  console.log(`\nArguments:`);
  console.log(`-i <input text file>, path to file`);
  console.log(`-o <output text file>, path to file`);
  console.log(`-p <probability>, probability of a spelling error, number between 0 and 1, e.g.: 0.2`);
  console.log(`\nPlease specify all the listed above arguments.`);
}

if (validateArgs()) {
  const text = await fs.readFile(fin, 'utf8');
  const newText = text.replace(/\p{Letter}+/ug, (match) => {
    return Math.random() < probability ? mutate(match) : match;
  });

  await fs.writeFile(fout, newText);
} else {
  process.exit(1);
}
