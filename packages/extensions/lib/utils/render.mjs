import 'zx/globals';

import _ from 'lodash';
import ejs from 'ejs';

const BINARY_EXTS = ['.png'];

function isBinary(filename) {
  return BINARY_EXTS.includes(path.extname(filename));
}

export default async function render(rootDir, outDir, filename, opts) {
  const srcPath = path.join(rootDir, filename);
  const outPath = path.join(outDir, filename);

  await fs.ensureDir(path.dirname(outPath));
  const content = isBinary(srcPath)
    ? await fs.readFile(srcPath)
    : await ejs.renderFile(srcPath, opts, {
        legacyInclude: false,
      });

  await fs.writeFile(outPath, content);
  console.log('Rendered: ' + chalk.yellow(outPath));
}
