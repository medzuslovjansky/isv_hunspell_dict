import ejs from 'ejs';
import fs from 'fs-extra';

export default async function renderEJS(args) {
  const {sourceFile, outFile, payload} = args;

  await fs.ensureDir(path.dirname(outFile));
  const content = await ejs.renderFile(sourceFile, payload, {
      legacyInclude: false,
  });

  await fs.writeFile(outFile, content);
}
