import 'zx/globals';

import _ from 'lodash';
import ejs from 'ejs';

const BINARY_EXTS = ['.png'];

function isBinary(filename) {
  return BINARY_EXTS.includes(path.extname(filename));
}

export default async function render(outDir, srcFile, opts) {
  const outPath = path.join(outDir, ...srcFile.split(path.sep).slice(1));
  await fs.ensureDir(path.dirname(outPath));

  const content = isBinary(srcFile)
    ? await fs.readFile(srcFile)
    : await ejs.renderFile(srcFile, opts, {
        legacyInclude: false,
      });

  await fs.writeFile(outPath, content);
  console.log('Rendered: ' + chalk.yellow(outPath));
}
