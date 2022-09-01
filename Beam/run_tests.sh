#!/bin/bash


for i in 1 2 3 
do
        echo "Running test $i"
        cp run_f1f2f3/cf/Config_$i.py Modules/Config.py
        python3 generate_OTR.py
done
~      
