#!/bin/bash

################################################################################
# Usage:
#
# ./benchmark.sh SNSPowderReduction.py
#
# If you want to only run a single number of threads (say 12), use
# ./benchmark.sh SNSPowderReduction.py 12
################################################################################

BASEDIR="$(pwd)/..";
TOOLDIR="${BASEDIR}/tools";
RESULTSDIR="${BASEDIR}/results";
PY='python3';

SCRIPT=$1;

if [ ${#SCRIPT} -eq 0 ] ; then

  echo "No script specified! Please give script file as argument."

else

  if [ ${#2} -gt 0 ] ; then
    NTHREADS=( $2 );
  else
    NTHREADS=( 1 2 4 8 12 16 20 24 );
  fi

  for ((i=0; i<${#NTHREADS[@]}; i++ )); do

    # Modify the config file with number of threads
    CONFIG=~/.mantid/Mantid.user.properties;
    cp $CONFIG.bk $CONFIG;
    echo "MultiThreaded.MaxCores=${NTHREADS[i]}" >> $CONFIG;

    ${PY} ${SCRIPT} ${NTHREADS[i]} & ${PY} ${TOOLDIR}/psrecord.py --log ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]}.cpu --include-children --absolute $!;
    mv algotimeregister.out ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]}.out;
    ${PY} ${TOOLDIR}/plot_cpu_memory_usage.py ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]};

  done

  ${PY} ${TOOLDIR}/plot_scaling.py ${RESULTSDIR}/${SCRIPT/.py/};

  # Restore config file
  cp ${CONFIG}.bk $CONFIG;

fi
