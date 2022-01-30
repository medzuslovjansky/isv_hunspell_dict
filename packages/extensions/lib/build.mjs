#!/usr/bin/env zx

import 'zx/globals';
import _ from 'lodash';

import render from './utils/render.mjs';
import { recreateDirectory, copyFile } from './utils/fs.mjs';
import { zipFolder } from './utils/zip.mjs';

const buildVersion = process.env.BUILD_VERSION || '0.0.0';
const presets = [
  {
    id: 'libreoffice',
    template: 'libreoffice',
    artifactName: `interslavic-libreoffice-${buildVersion}.oxt`,
    isEtymological: false,
    includeDicts: [
      'Medzuslovjansky_Kirilica',
      'Medzuslovjansky_LatinicaStandard',
    ],
  },
  {
    id: 'libreoffice-etymological',
    template: 'libreoffice',
    artifactName: `interslavic-libreoffice-etymological-${buildVersion}.oxt`,
    isEtymological: true,
    includeDicts: [
      'Medzuslovjansky_Kirilica',
      'Medzuslovjansky_LatinicaEtimologicna',
    ],
  },
  {
    id: 'chrome',
    template: 'chrome',
    artifactName: `interslavic-chrome-${buildVersion}.crx`,
    isEtymological: false,
    includeDicts: ['Medzuslovjansky_KomboLatinicaKirilica'],
  },
  {
    id: 'firefox',
    template: 'firefox',
    artifactName: `interslavic-firefox-${buildVersion}.webext`,
    isEtymological: false,
    includeDicts: ['Medzuslovjansky_KomboLatinicaKirilica'],
  },
];

for (const p of presets) {
  console.log(`\
-----------------------------
Creating ${chalk.green(p.id)} extension:
-----------------------------`);

  const outDir = `.temp/${p.id}`;
  await recreateDirectory(outDir)

  const templateDir = path.join('templates', p.template);
  const templateFiles = await globby('**', { cwd: templateDir });
  for (const f of templateFiles) {
    await render(templateDir, outDir, f, {
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
  
  await zipFolder(outDir, path.join('dist', p.artifactName));
}
