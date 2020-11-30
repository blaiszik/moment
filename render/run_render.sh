#! /bin/bash

# This script just runs through all of the files in the proper order

# If we get too many files, we should probably create a file containing
#  names of notebooks and the order in which they should be executed
for n in `seq 0 0`; do
    python ${n}_*py
done

