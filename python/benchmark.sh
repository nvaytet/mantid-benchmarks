#!/bin/bash

SCRIPT="run_SNSPowderReduction.py";
NTHREADS=( 1 2 4 8 12 16 20 24 );
# NTHREADS=( 1 );


for ((i=0; i<${#NTHREADS[@]}; i++ )); do

  # Modify the config file with number of threads
  CONFIG=~/.mantid/Mantid.user.properties;
  cp $CONFIG $CONFIG.backup;
  echo "MultiThreaded.MaxCores=${NTHREADS[i]}" >> $CONFIG;

  python ${SCRIPT} ${NTHREADS[i]} & python psrecord.py --log activity.txt --interval 0.01 --include-children --absolute $!
  mv algotimeregister.out algotimeregister_${NTHREADS[i]}.out;
  mv activity.txt activity_${NTHREADS[i]}.txt;
  python3 plot_cpu_memory_usage.py activity_${NTHREADS[i]}.txt algotimeregister_${NTHREADS[i]}.out;
  mv graph.pdf ${SCRIPT/.py/}_${NTHREADS[i]}.pdf;

  # Restore config file
  cp ${CONFIG}.backup $CONFIG;

done
