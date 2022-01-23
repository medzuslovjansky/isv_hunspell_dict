#!/usr/bin/env bash

if ! command -v plot &> /dev/null
then
  alias plot=gnuplot
fi

gnuplot scripts/bar.plot
