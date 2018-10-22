import os
import tree_walk
cwd = os.getcwd()
import yep

from mantid.simpleapi import SNSPowderReduction
from mantid import config, AnalysisDataService

datadir = "/home/nvaytet/aaa_work/code/mantid/sources/clean/build/ExternalData/Testing/Data/SystemTest"
datadir += ";/media/nvaytet/30c9d25c-0aba-427f-b8ea-3079e881dfce/benchmarks_data/SNSPowderReduction_data"
config['datasearch.searcharchive'] = 'off'

# Adopted from SNSPowderRedux.PG3Analysis
run_file  = "PG3_77777_event.nxs"
ref_file  = "PG3_4844_reference.gsa"
cal_file  = "PG3_FERNS_d4832_2011_08_24.cal"
char_file = "PG3_characterization_2011_08_31-HR.txt"

# filesize_list = [1,2,4,8,16]
# nthreads_list = [1,2,4,8,12,16,20,24]
filesize_list = [1]
nthreads_list = [1]

for i in filesize_list:
    for j in nthreads_list:

        # Start fresh
        AnalysisDataService.clear()
        # Set-up config
        config['datasearch.directories'] = datadir + "/data_fact%03d" % i
        config['MultiThreaded.MaxCores'] = str(j)

        # Run Powder reduction
        yep.start('outname')
        SNSPowderReduction(Filename=run_file,
                           PreserveEvents=True,
                           CalibrationFile=cal_file,
                           CharacterizationRunsFile=char_file,
                           LowResRef=15000, RemovePromptPulseWidth=50,
                           Binning=-0.0004, BinInDspace=True, FilterBadPulses=95,
                           SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=cwd+'/results',
                           FinalDataUnits="dSpacing")
        yep.stop()

        # Gather history and write it to file
        # names = AnalysisDataService.getObjectNames()
        w = AnalysisDataService['PG3_77777']
        h = w.getHistory()
        ah = h.getAlgorithmHistories()
        fname = "fact_%03d-nthreads_%03d"%(i,j)
        for k in ah:
            t = tree_walk.Tree(k)
            t.view(fname)
