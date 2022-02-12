#!/usr/bin/env zx

import _ from 'lodash';

import * as utils from './utils/index.mjs';

export { utils }

export async function build(options = {}) {
  const {
    id,
    outDir = '.temp',
    rootDir = 'template',
    payload = {},
    include = [],
    preProcess = _.noop,
    postProcess = _.noop,
  } = options;

  console.log(`\
-----------------------------
Creating ${chalk.green(id)} extension:
-----------------------------`);

  await utils.recreateDirectory(outDir)
  await preProcess({ id, outDir, rootDir, payload });

  console.log('Recreated directory: ' + chalk.yellow(outDir));

  const processedFiles = new Set();
  for (const entry of include) {
    const {
      glob,
      cwd = rootDir,
      transform = utils.copyFile,
      mapPath = _.identity
    } = entry;

    const files = await globby(glob, { cwd });

    for (const f of files) {
      if (processedFiles.has(f))
        continue;

      const sourceFile = path.join(cwd, f);
      const outFile = path.join(outDir, mapPath(f));
      await transform({
        sourceFile,
        outFile,
        payload: {
          ...payload,
          ...entry.payload,
        },
      });

      processedFiles.add(f);
      console.log('Transformed: ' + chalk.yellow(outFile));
    }
  }

  await postProcess({ id, outDir, rootDir, payload });
}
