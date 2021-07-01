import subprocess
import shlex
import os
import numpy as np

def run_cmd(cmd):
  process = subprocess.Popen(cmd.split(), stdout = subprocess.PIPE)
  #process.communicate()
  stdout = process.communicate()[0]
  print ('STDOUT:{}'.format(stdout))
  process.stdout.close()
  return " "

# x = np.arange(-580,5,5)
# x = np.arange(-5,6,1)
x = np.arange(-10,11,1)
# x = np.arange(-50,60,5)
# x = x*0.1
for i in range(len(x)):
    # run_cmd("alias python='/usr/bin/python3.8'");
    # run_cmd("/usr/bin/python3.8 -V");
    run_cmd("python pyOTR.py %d"  % (x[i]));
    run_cmd("/usr/bin/python3.8 FindHoleCentre.py");
    run_cmd("python pyOTR.py %d"  % (x[i]));
    run_cmd("/usr/bin/python3.8 FindHoleCentre.py");
    run_cmd("python pyOTR.py %d"  % (x[i]));
    run_cmd("/usr/bin/python3.8 FindHoleCentre.py");
    run_cmd("python pyOTR.py %d"  % (x[i]));
    run_cmd("/usr/bin/python3.8 FindHoleCentre.py");
    run_cmd("python pyOTR.py %d"  % (x[i]));
    run_cmd("/usr/bin/python3.8 FindHoleCentre.py");
