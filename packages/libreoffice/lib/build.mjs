#!/usr/bin/env zx

import 'zx/globals';

import { build, utils } from "@interslavic/hunspell-extension-builder";

const hunspellRoot = '../hunspell/output/dictionaries';
const buildVersion = process.env.BUILD_VERSION || '0.0.0';

async function zipIt({ id, outDir }) {
  await fs.ensureDir('dist');
  await utils.zipFolder(outDir, path.join('dist',  `interslavic-dict-${id}-${buildVersion}.oxt`));
}

const commonPayload = {
  buildVersion,
  BUILD_VERSION: buildVersion,
};

const commonIncludes = [
  {
    glob: '**/*.{xml,xcu,txt}',
    transform: utils.renderEJS,
  },
  { glob: '**' },
];

await build({
  id: 'libreoffice',
  outDir: '.temp/libreoffice',
  payload: {
    ...commonPayload,
    IS_ETYMOLOGICAL: false,
  },
  include: [
    ...commonIncludes,
    {
      cwd: hunspellRoot,
      glob: [
        'Medzuslovjansky_Kirilica.{aff,dic}',
        'Medzuslovjansky_LatinicaStandard.{aff,dic}'
      ]
    },
  ],
  postProcess: zipIt,
});

await build({
  id: 'libreoffice-etymological',
  outDir: '.temp/libreoffice-etymological',
  payload: {
    ...commonPayload,
    IS_ETYMOLOGICAL: true,
  },
  include: [
    ...commonIncludes,
    {
      to: '.',
      cwd: hunspellRoot,
      glob: [
        'Medzuslovjansky_Kirilica.{aff,dic}',
        'Medzuslovjansky_LatinicaEtimologicna.{aff,dic}'
      ]
    },
  ],
  postProcess: zipIt,
});
