#!/bin/bash

for i in 1 2 3 
do
	for j in 0 4 
	do
		echo "Running test $i$j"
		cp mirror_at_each_element_tests/output/Config_$i$j.py Modules/Config.py
		#ln -sfn ../mirror_at_each_element_tests/output/Config_$i$j.py Modules/Config.py
		#grep -E "(name =|image_loc =)" Modules/Config.py
		python3 pyOTR.py
		sleep 5
	done
done
