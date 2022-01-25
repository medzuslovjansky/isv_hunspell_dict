#!/usr/bin/env zx

async function copyDictionaries(originalFolder, originalName, targetName) {
  const dictionariesPath = path.join(process.cwd(), originalFolder);

  for (const ext of ['aff', 'dic']) {
    await fs.copyFile(
      path.join(dictionariesPath, `${originalName}.${ext}`),
      path.join('dict', `${targetName}.${ext}`)
    );
  }
}

const copyGeneratedDictionary = (src, dest) => copyDictionaries('../hunspell/output/dictionaries', src, dest);
const copyNpmDictionary = (lang) => copyDictionaries(`node_modules/dictionary-${lang}`, 'index', lang);

await fs.ensureDir('dict');
await Promise.all([
  copyGeneratedDictionary('Medzuslovjansky_KomboLatinicaKirilica', 'art-x-interslv'),
  copyGeneratedDictionary('Medzuslovjansky_Kirilica', 'art-Cyrl-x-interslv'),
  copyGeneratedDictionary('Medzuslovjansky_LatinicaStandard', 'art-Latn-x-interslv'),
  copyGeneratedDictionary('Medzuslovjansky_LatinicaEtimologicna', 'art-Latn-x-interslv-etymolog'),
  // copyNpmDictionary('cs'),
  // copyNpmDictionary('fr'),
  // copyNpmDictionary('pl'),
  // copyNpmDictionary('ru'),
]);
