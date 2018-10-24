import sys
sys.path.append("../tools")
import workflow_config as wfc
sys.path.extend(wfc.sys_path_ext)
import os
cwd = os.getcwd()

from mantid.simpleapi import SNSPowderReduction
from mantid import config, AnalysisDataService

config['datasearch.searcharchive'] = 'off'
config.setDataSearchDirs(wfc.datadirs["SNSPowderReduction"])

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
                   SaveAs="gsas and fullprof and pdfgetn", OutputDirectory=cwd,
                   FinalDataUnits="dSpacing")
