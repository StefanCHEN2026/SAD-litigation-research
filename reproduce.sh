#!/usr/bin/env bash
# Reproduce the simulation outputs in this repository.
# The core model uses only the Python standard library.
set -euo pipefail

python code/sad_abm_v2.py        > data/synthetic/sad_abm_v2_results.csv
python code/oos_validate.py      > data/synthetic/oos_results.csv
python code/behavior_validate.py > data/synthetic/behavior_results.csv

echo "done: synthetic outputs written to data/synthetic/"
