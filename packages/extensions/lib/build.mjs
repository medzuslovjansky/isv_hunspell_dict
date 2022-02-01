#!/usr/bin/env zx

import 'zx/globals';
import _ from 'lodash';

import render from './utils/render.mjs';
import { recreateDirectory, copyFile } from './utils/fs.mjs';
import { zipFolder } from './utils/zip.mjs';

const buildVersion = process.env.BUILD_VERSION || '0.0.0';

const hunspellRoot = path.join(process.cwd(), '../hunspell/output/dictionaries');
const bdicRoot = path.join(process.cwd(), '../bdic/output');

const presets = [
  {
    id: 'libreoffice',
    template: 'libreoffice',
    isEtymological: false,
    include: [
      { to: '.', from: path.join(hunspellRoot, 'Medzuslovjansky_Kirilica.{aff,dic}') },
      { to: '.', from: path.join(hunspellRoot, 'Medzuslovjansky_LatinicaStandard.{aff,dic}') },
    ],
    postProcess: ({ workingDir }) =>
      zipFolder(workingDir, path.join('dist',  `interslavic-dict-libreoffice-${buildVersion}.oxt`)),
  },
  {
    id: 'libreoffice-etymological',
    template: 'libreoffice',
    isEtymological: true,
    include: [
      { to: '.', from: path.join(hunspellRoot, 'Medzuslovjansky_Kirilica.{aff,dic}') },
      { to: '.', from: path.join(hunspellRoot, 'Medzuslovjansky_LatinicaStandard.{aff,dic}') },
    ],
    postProcess: ({ workingDir }) =>
      zipFolder(workingDir, path.join('dist',  `interslavic-dict-libreoffice-etymological-${buildVersion}.oxt`)),
  },
  {
    id: 'chrome',
    template: 'chrome',
    artifactName: `interslavic-dict-chrome-${buildVersion}.crx`,
    isEtymological: false,
    include: [
      { to: '.', from: path.join(bdicRoot, 'Medzuslovjansky_KomboLatinicaKirilica.bdic') },
    ],
    postProcess: () => {},
  },
  {
    id: 'firefox',
    template: 'firefox',
    isEtymological: false,
    include: [
      { to: 'dictionaries', from: path.join(hunspellRoot, 'Medzuslovjansky_KomboLatinicaKirilica.{aff,dic}') },
    ],
    postProcess: ({ workingDir }) =>
      $`npx web-ext sign --api-key "$MOZILLA_API_KEY" --api-secret "$MOZILLA_API_SECRET" -s "${workingDir}" -a dist`,
  },
  {
    id: 'macos',
    template: 'macos',
    include: [
      { to: 'root/Spelling', from: path.join(hunspellRoot, '*.{aff,dic}') },
    ],
    postProcess: ({ workingDir }) =>
      zipFolder(workingDir, path.join('dist',  `InterslavicSpellingDictionaries-${buildVersion}.pkg`)),
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
      buildVersion,
      installKBytes: 999,
      numberOfFiles: 10,
    });
  }

  for (const inc of p.include) {
    const files = await globby(inc.from);
    for (const f of files) {
      const filename = path.basename(f);
      await copyFile(f, path.join(outDir, inc.to, filename));
    }
  }
  
  await p.postProcess({ workingDir: outDir });
}
