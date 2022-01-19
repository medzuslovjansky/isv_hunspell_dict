#!/bin/bash

python3 run_instrument.py hunspell_dict_from_OCXML.py input/settings/generate_lat.py
python3 run_instrument.py hunspell_dict_from_OCXML.py input/settings/generate_cyr.py
python3 run_instrument.py hunspell_dict_from_OCXML.py input/settings/generate_etm.py
python3 run_instrument.py combine_dicts.py input/settings/combine_latcyr.py