#!/usr/bin/env zx

import 'zx/globals';
import _ from 'lodash';

import render from './utils/render.mjs';
import { recreateDirectory, copyFile } from './utils/fs.mjs';
import { zipFolder } from './utils/zip.mjs';

const buildVersion = process.env.BUILD_VERSION || '0.0.0';
const templateFiles = await globby(['template/**'])
const presets = [
  {
    isEtymological: false,
    includeDicts: [
      'Medzuslovjansky_Kirilica',
      'Medzuslovjansky_LatinicaStandard',
    ],
  },
  {
    name: 'etymological',
    isEtymological: true,
    includeDicts: [
      'Medzuslovjansky_Kirilica',
      'Medzuslovjansky_LatinicaEtimologicna',
    ],
  },
];

console.log(chalk.bold`LibreOffice extension builder`);
for (const p of presets) {
  console.log(`\
-----------------------------
Creating ${chalk.green(p.name)} dictionary:
-----------------------------`);

  const outDir = `.temp/${p.name || 'default'}`;
  await recreateDirectory(outDir)
  for (const f of templateFiles) {
    await render(outDir, f, {
      BUILD_VERSION: buildVersion,
      IS_ETYMOLOGICAL: p.isEtymological,
    });
  }

  for (const dict of p.includeDicts) {
    for (const ext of ['aff', 'dic']) {
      const dictFile = `${dict}.${ext}`;
      await copyFile(
        path.join('../hunspell/output/dictionaries', dictFile),
        path.join(outDir, dictFile)
      );
    }
  }
  
  const extensionName = ['interslavic', 'spell', 'checker', p.name].filter(Boolean).join('-');
  await zipFolder(outDir, `dist/${extensionName}-${buildVersion}.oxt`);
}
