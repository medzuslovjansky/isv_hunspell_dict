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

if [ "$machine" = "Linux" ]; then
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

  mkdir -p output
  mv $DICT_FOLDER/dictionaries/*.bdic output
  echo "Successfully moved .bdic file." 
else
  echo "Skipping bdic_convert because this machine is running $machine, not Linux..."
fi
