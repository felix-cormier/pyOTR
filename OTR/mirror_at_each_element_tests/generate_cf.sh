#!/bin/bash
for i in 1 2 3
do
	for j in 0 4 #can change to accomodate any trace set
	do
		echo "inputs = 'data/f$i""_{}.npy'" > Config2.py
		echo "name = 'mirror_at_each_element_tests/trace_through_system/files_npy/f$i""_$j'" >> Config2.py
		echo "image_loc = $j #0,1,2,3,4 or something else" >> Config2.py
		cat Config1.py Config2.py Config3.py > output/Config_$i$j.py 
	done
done
