#!/usr/bin/env bash

declare -a langs=("art-Latn-x-interslv" "art-Cyrl-x-interslv" "cs" "fr" "pl" "ru")

function count_non_whitespace() {
  echo `tr -d '[:space:] ' < "$1" | wc -cm`
}

function spell_check() {
  hunspell -d $1 -l "$2" >/dev/null
}

function benchmark_spell_check() {
  local TIMEFORMAT="%R"
  (time spell_check "$@") 2>&1
}

function calc_speed() {
  local CHAR_COUNT=`count_non_whitespace $2`
  local SPELL_TIME=`benchmark_spell_check $1 $2`
  bc <<< "scale=0; $CHAR_COUNT/$SPELL_TIME"
}

function benchmark() {
  export DICPATH=$PWD/dicts

  local CORRECT_FILE="samples/le-petite-prince/correct/$lang.txt"
  local ERROR_FILE="samples/le-petite-prince/errors-20pct/$lang.txt"
  local CORRECT_SPEED=`calc_speed $lang $CORRECT_FILE`
  local ERROR_SPEED=`calc_speed $lang $ERROR_FILE`

  printf "$lang\t$CORRECT_SPEED\t$ERROR_SPEED\n"
}

function run_benchmark() {
  printf "Language\tCorrect\tMisspelled\n"
  for lang in "${langs[@]}"
  do
    benchmark "$lang"
  done
}

run_benchmark > out/bench.dat
cat out/bench.dat
