import sys
import time as tm
import numpy as np
import pickle as pk
import os
import subprocess as sp
# sys.path.append('/home/igudich/work/mantid/python3Build/bin')
from mantid.simpleapi import *
import mantid

# mantid.config.appendDataSearchDir('./cmake-build-release-gcc/ExternalData/Testing/Data/SystemTest')
mantid.config.appendDataSearchDir('/home/nvaytet/aaa_work/code/mantid/sources/clean/build/ExternalData/Testing/Data/SystemTest')

filename = "PG3_4844"
cal_file  = "PG3_FERNS_d4832_2011_08_24.cal"
char_file = "PG3_characterization_2011_08_31-HR.txt"

# SNSPowderReduction(Filename=filename,
#                            PreserveEvents=True,
#                            CalibrationFile=cal_file,
#                            CharacterizationRunsFile=char_file,
#                            LowResRef=15000, RemovePromptPulseWidth=50,
#                            Binning=-0.0004, BinInDspace=True, FilterBadPulses=95,
#                            SaveAs="gsas and fullprof and pdfgetn", OutputDirectory="/home/nvaytet/aaa_work/code/mantid/mantid-benchmarks",
#                            FinalDataUnits="dSpacing")
#
# def runBenchmark(script, threads):
#     cmd = ['python3', script, str(threads)]
#     proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
#     output, err = proc.communicate()
#     proc_status = proc.wait()
#     print(output)
#     return {d[0] : float(d[1]) for d in [x.split()[1:5:3] for x in err.decode('utf-8').split('\\n') if 'successful' in x]}
#
# duration1 = runBenchmark('/home/igudich/work/ReductionBenchmarks/Benchmark_SNSPowderReduction.py', 1)
# duration2 = runBenchmark('/home/igudich/work/ReductionBenchmarks/Benchmark_SNSPowderReduction.py', 2)
# duration4 = runBenchmark('/home/igudich/work/ReductionBenchmarks/Benchmark_SNSPowderReduction.py', 4)
# duration12 = runBenchmark('/home/igudich/work/ReductionBenchmarks/Benchmark_SNSPowderReduction.py', 12)
# duration24 = runBenchmark('/home/igudich/work/ReductionBenchmarks/Benchmark_SNSPowderReduction.py', 24)
#
# duration_ = {i : runBenchmark('/home/igudich/work/ReductionBenchmarks/Benchmark_Rebin.py', i) for i in [1,2,3,4,5,6,7,8,12,18,24]}
#
# for i in [1,2,4,12,24]:
#     print(duration_[i])
#
# # duration[2]

SNSPowderReduction(Filename=filename,
                   PreserveEvents=True,
                   CalibrationFile=cal_file,
                   CharacterizationRunsFile=char_file,
                   LowResRef=15000, RemovePromptPulseWidth=50,
                   Binning=-0.0004, BinInDspace=True, FilterBadPulses=95,
                   SaveAs="gsas and fullprof and pdfgetn", OutputDirectory="/home/nvaytet/aaa_work/code/mantid/mantid-benchmarks",
                   FinalDataUnits="dSpacing")

names = mantid.api.AnalysisDataService.getObjectNames()

w = mantid.api.AnalysisDataService['PG3_4844']
h = w.getHistory()
print(dir(h))
ah = h.getAlgorithmHistories()
print(dir(ah))

for i in ah:
    print(i)

# len(h.getAlgorithmHistories())
