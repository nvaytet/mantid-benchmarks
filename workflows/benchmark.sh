#!/bin/bash

BASEDIR="$(pwd)/..";
TOOLDIR="${BASEDIR}/tools";
RESULTSDIR="${BASEDIR}/results";
PY='python3';

SCRIPT=$1;

if [ ${#SCRIPT} -eq 0 ] ; then

  echo "No script specified! Please give script file as argument."

else

  NTHREADS=( 12 );

  for ((i=0; i<${#NTHREADS[@]}; i++ )); do

    # Modify the config file with number of threads
    CONFIG=~/.mantid/Mantid.user.properties;
    cp $CONFIG.bk $CONFIG;
    echo "MultiThreaded.MaxCores=${NTHREADS[i]}" >> $CONFIG;

    ${PY} ${SCRIPT} ${NTHREADS[i]} & ${PY} ${TOOLDIR}/psrecord.py --log ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]}.cpu --include-children --absolute $!;
    mv algotimeregister.out ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]}.out;
    ${PY} ${TOOLDIR}/plot_cpu_memory_usage.py ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]}.cpu ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]}.out ${RESULTSDIR}/${SCRIPT/.py/}_${NTHREADS[i]}.pdf;

  done

  ${PY} ${TOOLDIR}/plot_scaling.py ${RESULTSDIR}/${SCRIPT/.py/};

  # Restore config file
  cp ${CONFIG}.bk $CONFIG;

fi
