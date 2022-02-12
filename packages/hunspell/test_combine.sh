#!/bin/bash

python3 run_instrument.py combine_dicts.py tests/combine_test.py
# && { cmp --silent tests/test_in.dic tests/test_out.dic && echo "yay! .dic files match!" || echo ".dic files not same" ;}
