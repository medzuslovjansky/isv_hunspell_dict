#!/usr/bin/env bash

if [[ -z "${BUILD_VERSION}" ]]; then
  printf 'No $BUILD_VERSION environment variable is defined, exiting...\n' >&2
  exit 1
fi

rm -rf dist
mkdir -p dist
cp -r lib dist

pushd>/dev/null dist/lib
ln -s ../../../../output/dictionaries/Medzuslovjansky_Kirilica.aff art-Cyrl-x-interslv.aff
ln -s ../../../../output/dictionaries/Medzuslovjansky_Kirilica.dic art-Cyrl-x-interslv.dic
ln -s ../../../../output/dictionaries/Medzuslovjansky_LatinicaStandard.aff art-Latn-x-interslv.aff
ln -s ../../../../output/dictionaries/Medzuslovjansky_LatinicaStandard.dic art-Latn-x-interslv.dic
sed -i'' -e "s/\(<version value=\"\)[^\"]*/\1$BUILD_VERSION/" description.xml
zip -r ../interslavic-spell-checker-$BUILD_VERSION.oxt .
popd>/dev/null
rm -rf dist/lib
ls dist/*
