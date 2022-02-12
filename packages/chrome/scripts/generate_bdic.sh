#!/usr/bin/env bash

set -e

unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     machine=Linux;;
    Darwin*)    machine=Mac;;
    CYGWIN*)    machine=Cygwin;;
    MINGW*)     machine=MinGw;;
    *)          machine="UNKNOWN:${unameOut}"
esac

if [ "$machine" != "Linux" ]; then
  echo "Aborting BDIC generation because this machine is running $machine, not Linux..."
  exit 1
fi

if [[ -z "$LAZY" ]] ||  [[ ! -d ".temp/bdic" ]]; then
  if [ -d "bdic_convert" ]; then
    echo "Updating bdic_convert..."
    cd bdic_convert && git pull && cd -
  else
    git clone --depth=1 --branch=master https://github.com/medzuslovjansky/convert-dict-tool-from-chromium.git bdic_convert
  fi

  DICT_FOLDER=../hunspell/output/dictionaries

  touch "$DICT_FOLDER/Medzuslovjansky_Kirilica.dic_delta"
  bdic_convert/convert_dict "$DICT_FOLDER/Medzuslovjansky_Kirilica"

  touch "$DICT_FOLDER/Medzuslovjansky_KomboLatinicaKirilica.dic_delta"
  bdic_convert/convert_dict "$DICT_FOLDER/Medzuslovjansky_KomboLatinicaKirilica"

  touch "$DICT_FOLDER/Medzuslovjansky_LatinicaEtimologicna.dic_delta"
  bdic_convert/convert_dict "$DICT_FOLDER/Medzuslovjansky_LatinicaEtimologicna"

  touch "$DICT_FOLDER/Medzuslovjansky_LatinicaStandard.dic_delta"
  bdic_convert/convert_dict "$DICT_FOLDER/Medzuslovjansky_LatinicaStandard"

  echo "Successfully generated .bdic file."

  mkdir -p .temp/bdic
  mv $DICT_FOLDER/*.bdic .temp/bdic
  echo "Successfully moved *.bdic files."
else
  echo "Skipping generation (lazy mode)..."
fi
