#!/bin/bash

# exit if using undeclared variables
set -o nounset
set -o errtrace
set -o xtrace

# for each profile in firefox
cd "${HOME}/Library/Application Support/Firefox/Profiles" \
&& for d in *
do
  { cd "$d" \
    && /bin/cp -rf prefs.js{,.isvbackup} ;} \
  && { [ -f prefs.js ] \
    && if ! grep -q spellchecker.dictionary_path prefs.js ; then
      echo 'user_pref("spellchecker.dictionary_path", "~/Library/Spelling");' >> prefs.js
    else
      sed -i '' '/spellchecker.dictionary_path/s/.*/user_pref("spellchecker.dictionary_path", "~\/Library\/Spelling");/' prefs.js 
    fi \
    || { /bin/cp -rf prefs.js.isvbackup prefs.js ; exit 666 ;} ;}
done
exit 0
