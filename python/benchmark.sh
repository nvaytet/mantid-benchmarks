#!/bin/bash

SCRIPT="SNSPowderReduction.py";
# SCRIPT="SANSReduction.py";

NTHREADS=( 1 2 4 8 12 16 20 24 );

for ((i=0; i<${#NTHREADS[@]}; i++ )); do

  # Modify the config file with number of threads
  CONFIG=~/.mantid/Mantid.user.properties;
  cp $CONFIG.bk $CONFIG;
  echo "MultiThreaded.MaxCores=${NTHREADS[i]}" >> $CONFIG;

  python3 ${SCRIPT} ${NTHREADS[i]} & python3 psrecord.py --log ${SCRIPT/.py/}_${NTHREADS[i]}.cpu --interval 0.01 --include-children --absolute $!;
  mv algotimeregister.out ${SCRIPT/.py/}_${NTHREADS[i]}.out;
  python3 plot_cpu_memory_usage.py ${SCRIPT/.py/}_${NTHREADS[i]}.cpu ${SCRIPT/.py/}_${NTHREADS[i]}.out ${SCRIPT/.py/}_${NTHREADS[i]}.pdf;

done

python3 plot_scaling.py ${SCRIPT/.py/};

# Restore config file
  cp ${CONFIG}.bk $CONFIG;

exit;
