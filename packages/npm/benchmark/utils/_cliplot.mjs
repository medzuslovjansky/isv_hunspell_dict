import { parse as csvParse } from 'csv-parse/sync';
import bar from 'ervy/lib/bar.js';
import ervyUtils from 'ervy/lib/utils.js';

const { bg } = ervyUtils;

async function getBenchmarkData(input) {
  return csvParse(await fs.readFile(input, 'utf8'), {
    columns: true,
    delimiter: '\t',
  });
}

export default async function cliPlot({ input, output }) {
  const benchmarkData = await getBenchmarkData(input);
  const barData = benchmarkData.map(({Language, Speed}) => ( 
    {
      key: Language,
      value: Math.floor(1E-3 * Speed),
      style: Language.startsWith('dictionary-') ? '░' : '▓',
    }
  ));

  const plot = bar(barData, { barWidth: 5, padding: 9, height: 12 });

  await fs.writeFile(output, [
    '------------------------------------------',
    '1,000 non-whitespace characters per second',
    '         (the more is the better)         ',
    '------------------------------------------',
    '',
    plot,
    '',
  ].join('\n'));
}
