#!/bin/bash


echo "name = 'run_f1f2f3/sim_output/f1'" > Config2.py
#echo "name = '../OTR/data/f1'" > Config2.py
echo "	'F1' : True," > Config4.py
echo "	'F2' : False," >> Config4.py
echo "	'F3' : False" >> Config4.py
cat Config1.py Config2.py Config3.py Config4.py Config5.py > cf/Config_1.py


echo "name = 'run_f1f2f3/sim_output/f2'" > Config2.py
#echo "name = '../OTR/data/f2'" > Config2.py
echo "	'F1' : False," > Config4.py
echo "	'F2' : True," >> Config4.py
echo "	'F3' : False" >> Config4.py
cat Config1.py Config2.py Config3.py Config4.py Config5.py > cf/Config_2.py

echo "name = 'run_f1f2f3/sim_output/f3'" > Config2.py
#echo "name = '../OTR/data/f3'" > Config2.py
echo "	'F1' : False," > Config4.py
echo "	'F2' : False," >> Config4.py
echo "	'F3' : True" >> Config4.py
cat Config1.py Config2.py Config3.py Config4.py Config5.py > cf/Config_3.py
