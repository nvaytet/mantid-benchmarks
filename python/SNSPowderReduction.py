import os
cwd = os.getcwd()

from mantid.simpleapi import SNSPowderReduction
from mantid import config, AnalysisDataService

# Set-up config
datadir = "/home/nvaytet/aaa_work/code/mantid/sources/clean/build/ExternalData/Testing/Data/SystemTest"
datadir += ";/media/nvaytet/30c9d25c-0aba-427f-b8ea-3079e881dfce/benchmarks_data/SNSPowderReduction_data"
config['datasearch.searcharchive'] = 'off'
config['datasearch.directories'] = datadir + "/data_fact016"# % i

# Adopted from SNSPowderRedux.PG3Analysis
run_file  = "PG3_77777_event.nxs"
ref_file  = "PG3_4844_reference.gsa"
cal_file  = "PG3_FERNS_d4832_2011_08_24.cal"
char_file = "PG3_characterization_2011_08_31-HR.txt"

# Run Powder reduction
SNSPowderReduction(Filename=run_file,
                   PreserveEvents=False,
                   CalibrationFile=cal_file,
                   CharacterizationRunsFile=char_file,
                   LowResRef=15000, RemovePromptPulseWidth=50,
                   Binning=-0.0004, BinInDspace=True, FilterBadPulses=95,
                   SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=cwd+'/results',
                   FinalDataUnits="dSpacing")
