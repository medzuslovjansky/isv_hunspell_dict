#!/usr/bin/env zx

import { spawn } from 'child_process';
import { parse as csvParse } from 'csv-parse/sync';
import which from 'which';
import bar from 'ervy/lib/bar.js';
import ervyUtils from 'ervy/lib/utils.js';

async function getBenchmarkData() {
  return csvParse(await fs.readFile(argv.i, 'utf8'), {
    columns: true,
    delimiter: '\t',
  });
}

async function gnuPlot() {
  return new Promise((resolve, reject) => {
    spawn('gnuplot').stdin.end([
      `set term png`,
      `set output "${argv.o}"`,
      `set title "Spellchecking speed\\n(more means better)"`,
      `set ylabel "characters per second"`,
      `set auto x`,
      `set yrange [0:*]`,
      `set style data histogram`,
      `set style histogram cluster gap 1`,
      `set style fill solid border -1`,
      `set boxwidth 0.9`,
      `set xtic scale 0`,
      `set xtics rotate by -45`,
      `plot '${argv.i}' using 2:xtic(1) ti col fc rgb "#99ffff"`,
    ].join('\n'), 'utf8', (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

async function cliPlot() {
  const { bg } = ervyUtils;
  console.log('------------------------------------------')
  console.log('1,000 non-whitespace characters per second')
  console.log('------------------------------------------\n')

  const benchmarkData = await getBenchmarkData();
  const barData = benchmarkData.map(({Language, Speed}) => ( 
    {
      key: Language,
      value: Math.floor(1E-3 * Speed),
      style: Language.startsWith('art-') ? bg('red') : bg('blue'),
    }
  ));

  console.log(bar(barData, { barWidth: 5, padding: 9, height: 12 }))
}


if (!argv.i || !argv.o) {
  console.log(chalk.red('Please specify -i <input> and -o <output>, e.g.: -i out/bench.dat -o out/bench.png'));
} else {
  if (!argv.cli && await which('gnuplot').catch(() => {})) {
    await gnuPlot();
  } else {
    console.log(chalk.yellow('Warning: gnuplot was not found, falling back to ASCII art...'));
    await cliPlot();
  }
}
