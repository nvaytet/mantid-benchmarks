import os
import tree_walk
cwd = os.getcwd()

from mantid.simpleapi import SNSPowderReduction
import mantid

datadir = "/home/nvaytet/aaa_work/code/mantid/sources/clean/build/ExternalData/Testing/Data/SystemTest"
datadir += ";/media/nvaytet/30c9d25c-0aba-427f-b8ea-3079e881dfce/benchmarks_data/SNSPowderReduction_data"
mantid.config['datasearch.searcharchive'] = 'off'

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

        # from mantid import config
        mantid.config['datasearch.directories'] = datadir + "/data_fact%03d" % i
        mantid.config['MultiThreaded.MaxCores'] = str(j)

        SNSPowderReduction(Filename=run_file,
                           PreserveEvents=False,
                           CalibrationFile=cal_file,
                           CharacterizationRunsFile=char_file,
                           LowResRef=15000, RemovePromptPulseWidth=50,
                           Binning=-0.0004, BinInDspace=True, FilterBadPulses=95,
                           SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=cwd+'/results',
                           FinalDataUnits="dSpacing")

        names = mantid.api.AnalysisDataService.getObjectNames()

        w = mantid.api.AnalysisDataService['PG3_77777']
        h = w.getHistory()
        ah = h.getAlgorithmHistories()
        fname = "fact_%03d-nthreads_%03d"%(i,j)
        for i in ah:
            t = tree_walk.Tree(i)
            t.view(fname)
