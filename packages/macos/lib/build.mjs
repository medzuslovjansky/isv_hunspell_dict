#!/usr/bin/env zx

import 'zx/globals';

import { build, utils } from "@interslavic/hunspell-extension-builder";

const buildVersion = process.env.BUILD_VERSION || '0.0.0';
const hunspellRoot = '../hunspell/output/dictionaries';

await build({
  id: 'macos',
  include: [
    {
      cwd: hunspellRoot,
      glob: '*.{aff,dic}',
      mapPath: f => path.join('root/Spelling', f),
    },
    {
      glob: [
        'flat/Distribution',
        'flat/base.pkg/PackageInfo',
      ],
      transform: utils.renderEJS,
    },
    {
      glob: '**/{License,ReadMe,Welcome}'
    },
    {
      glob: '**'
    },
  ],
  payload: {
    buildVersion,
    BUILD_VERSION: buildVersion,
    installKBytes: 0,
    numberOfFiles: 0,
  },
  postProcess: async ({ outDir }) => {
    await fs.ensureDir('dist');
    await utils.zipFolder(outDir, path.join('dist',  `InterslavicSpellingDictionaries-${buildVersion}.pkg`));
  },
});
