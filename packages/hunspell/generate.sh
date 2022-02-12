#!/bin/bash

if [[ -z "$LAZY" ]] ||  [[ ! -d "output" ]]; then
  python3 run_instrument.py hunspell_dict_from_OCXML.py settings/generate_lat.py
  python3 run_instrument.py hunspell_dict_from_OCXML.py settings/generate_cyr.py
  python3 run_instrument.py hunspell_dict_from_OCXML.py settings/generate_etm.py
  python3 run_instrument.py combine_dicts.py settings/combine_latcyr.py
else
  echo "Skipping generation (lazy mode)..."
fi
