import { spawn } from 'child_process';

export default async function gnuPlot({ input, output }) {
  return new Promise((resolve, reject) => {
    spawn('gnuplot').stdin.end([
      `set term png`,
      `set output "${output}"`,
      `set title "Spellchecking speed\\n(more means better)"`,
      `set ylabel "characters per second"`,
      `set auto x`,
      `set yrange [0:*]`,
      `set nokey`,
      `set style data histogram`,
      `set style histogram cluster gap 1`,
      `set style fill solid border -1`,
      `set boxwidth 0.9`,
      `set xtic scale 0`,
      `set xtics rotate by -45`,
      `plot '${input}' using 2:xtic(1) ti col fc rgb "#99ffff"`,
    ].join('\n'), 'utf8', (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}
