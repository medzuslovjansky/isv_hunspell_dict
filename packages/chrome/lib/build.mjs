#!/usr/bin/env zx

import 'zx/globals';

import { build, utils } from "@interslavic/hunspell-extension-builder";

const buildVersion = process.env.BUILD_VERSION || '0.0.0';

await build({
  id: 'chrome',
  outDir: '.temp/extension',
  artifactName: `interslavic-dict-chrome-${buildVersion}.crx`,
  include: [
    { cwd: '.temp/bdic', glob: 'Medzuslovjansky_KomboLatinicaKirilica.bdic' },
    {
      glob: '**/*.{json,xml}',
      transform: utils.renderEJS,
    },
    { glob: '**' },
  ],
  payload: {
    buildVersion,
    BUILD_VERSION: buildVersion,
  },
  preProcess: async () => $`LAZY=1 scripts/generate_bdic.sh`,
  postProcess: () => { console.log('\nTODO\n'); },
});
