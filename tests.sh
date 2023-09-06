#!/bin/bash

SUBS_ALG=("R" "F" "L")

for str in ${SUBS_ALG[@]}
do
    python src/cache_simulator.py 256 4 1 $str 1 resources/bin_100.bin
    python src/cache_simulator.py 128 2 4 $str 1 resources/bin_1000.bin
    python src/cache_simulator.py 16 2 8 $str 1 resources/bin_10000.bin
    python src/cache_simulator.py 512 8 2 $str 1 resources/vortex.in.sem.persons.bin
    python src/cache_simulator.py 1 4 32 $str 1 resources/vortex.in.sem.persons.bin
done