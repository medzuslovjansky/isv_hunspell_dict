#!/usr/bin/env zx

async function copyDictionaries(originalFolder, originalName, targetName) {
  const cwd = process.cwd();
  const dictionariesPath = path.join(cwd, originalFolder);

  for (const ext of ['aff', 'dic']) {
    await fs.copyFile(
      path.join(dictionariesPath, `${originalName}.${ext}`),
      path.join(cwd, `${targetName}.${ext}`)
    );
  }
}

const copyGeneratedDictionary = (src, dest) => copyDictionaries('../hunspell/output/dictionaries', src, dest);

await fs.ensureDir('dict');
await Promise.all([
  copyGeneratedDictionary('Medzuslovjansky_KomboLatinicaKirilica', 'index'),
  copyGeneratedDictionary('Medzuslovjansky_KomboLatinicaKirilica', 'dict/art-x-interslv'),
  copyGeneratedDictionary('Medzuslovjansky_Kirilica', 'dict/art-Cyrl-x-interslv'),
  copyGeneratedDictionary('Medzuslovjansky_LatinicaStandard', 'dict/art-Latn-x-interslv'),
  copyGeneratedDictionary('Medzuslovjansky_LatinicaEtimologicna', 'dict/art-Latn-x-interslv-etymolog'),
]);
