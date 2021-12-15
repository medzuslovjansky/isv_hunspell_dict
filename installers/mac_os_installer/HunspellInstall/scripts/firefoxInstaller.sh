#!/bin/sh
cd "${HOME}/Library/Application Support/Firefox/Profiles"
for d in *
do
  cd "$d"
  /bin/cp -rf prefs.js{,.isvbackup}
  if ! grep -q spellchecker.dictionary_path prefs.js ; then
    echo 'user_pref("spellchecker.dictionary_path", "~/Library/Spelling");' >> prefs.js
  else
    sed -i '' '/spellchecker.dictionary_path/s/.*/user_pref("spellchecker.dictionary_path", "~\/Library\/Spelling");/' prefs.js 
  fi
done
exit 0
