#!/usr/bin/env zx

for (const f of await globby('dictionary-isv-*.tgz')) {
  const altName = f.replace('dictionary-isv', 'interslavic-dict-npm');
  await fs.move(f, altName, { overwrite: true });
  console.log('Renamed:', f, '->', altName);
}
