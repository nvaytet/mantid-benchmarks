import sys
sys.path.append("../tools")
import workflow_config as wfc
sys.path.extend(wfc.sys_path_ext)

from mantid.simpleapi import *

# Set-up config
config['datasearch.searcharchive'] = 'off'
config.setDataSearchDirs(wfc.datadirs["DGSReduction"])
config['default.facility'] = "SNS"

# Run DGS Reduction
ws = Load("CNCS_7860_event.nxs", LoadMonitors=True)
monitor = ws[1]
valC3 = ws[0].getRun()['Phase3'].getStatistics().median
ws = FilterByLogValue(ws[0], LogName="Phase3", MinimumValue=valC3-0.3,
                      MaximumValue=valC3+0.3)
# Although CNCS doesn't use its monitors, this is how instruments that do need
# to call the algorithm.
ws = DgsReduction(SampleInputWorkspace=ws, SampleInputMonitorWorkspace=monitor,
                  IncidentBeamNormalisation="ByCurrent", SofPhiEIsDistribution=False)
w = ws[0]
print("Workspace type = {}".format(w.id()))
print("Number of events = {}".format(w.getNumberEvents()))
