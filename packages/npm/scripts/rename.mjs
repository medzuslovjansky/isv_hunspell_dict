#!/usr/bin/env zx

for (const f of await globby('interslavic-hunspell-dictionary-*.tgz')) {
  const altName = f.replace('hunspell-dictionary', 'dict-npm');
  await fs.move(f, altName, { overwrite: true });
  console.log('Renamed:', f, '->', altName);
}
