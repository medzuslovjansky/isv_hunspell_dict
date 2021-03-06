#!/usr/bin/env zx

import which from 'which';
import gnuplot from './utils/_gnuplot.mjs';
import cliplot from './utils/_cliplot.mjs';

if (Object.keys(argv).length <= 1) {
  console.log(chalk.bold`${path.basename(__filename)} - the CLI tool to draw bar chart for the benchmark`);
  console.log(`\nArguments:`);
  console.log(`-i <input text file>, path to tab-separated values generated by the benchmark`);
  console.log(`-o <output graphics file>, file path`);
  console.log(`--cli, optional override to use pseudo-graphics for rendering`);
  console.log(`\nPlease specify the arguments listed above.`);
  process.exit(1);
}

const isCLI = argv.cli;
const fin = argv.i;
const fout = argv.o || (isCLI ? '/dev/stdout' : undefined);

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

  if (isCLI !== undefined && typeof isCLI !== 'boolean') {
    console.warn(chalk.yellow('Invalid use of --cli. Use either: --cli, --no-cli, --cli=true|false'));
    valid = false;
  }

  return valid;
}

if (validateArgs()) {
  if (isCLI) {
    await cliplot({ input: fin, output: fout });
  } else {
    const hasGnuplot = await which('gnuplot').catch(() => {});

    if (!hasGnuplot) {
      console.error(chalk.red`Warning: gnuplot was not found in $PATH!`);
      process.exit(2);
    }

    await gnuplot({ input: fin, output: fout });
  }
} else {
  process.exit(1);
}
