#!/usr/bin/env zx

import 'zx/globals';

import { build, utils } from "@interslavic/hunspell-extension-builder";

const buildVersion = process.env.BUILD_VERSION || '0.0.0';
const hunspellRoot = '../hunspell/output/dictionaries';

await build({
  id: 'firefox',
  include: [
    {
      cwd: hunspellRoot,
      glob: 'Medzuslovjansky_KomboLatinicaKirilica.{aff,dic}',
      mapPath: p => path.join('dictionaries', p),
    },
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
  postProcess: process.env.IS_RELEASE === '1' ? sign : compress,
});

async function sign({ outDir }) {
  if (!process.env.MOZILLA_API_KEY || !process.env.MOZILLA_API_SECRET) {
    console.warn(chalk.yellow`Cannot sign the extension without the secrets.`);
    process.exit(1);
  }

  if (buildVersion === '0.0.0') {
    console.warn(chalk.yellow`Please set BUILD_VERSION to sign the extension.`);
    process.exit(1);
  }

  await fs.ensureDir('dist');
  await $`npx web-ext sign --api-key "$MOZILLA_API_KEY" --api-secret "$MOZILLA_API_SECRET"`;
  await enforceNaming();
}

async function compress({ outDir }) {
  await fs.ensureDir('dist');
  await $`npx web-ext build`;
  await enforceNaming();
}

async function enforceNaming() {
  for (const f of await globby('dist/*')) {
    const altName = f.replace('interslavic_spellcheck_dictionary', 'interslavic-dict-firefox');
    if (altName !== f) {
      await fs.move(f, altName);
      console.log('Renamed:', f, '->', altName);
    }
  }
}
