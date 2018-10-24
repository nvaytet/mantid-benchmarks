import sys
sys.path.append("../tools")
import workflow_config as wfc
sys.path.extend(wfc.sys_path_ext)

from mantid import config
import sans.command_interface.ISISCommandInterface as ci

# Set-up config
config['datasearch.searcharchive'] = 'off'
config.setDataSearchDirs(wfc.datadirs["SANSReduction1"])

# Run SANS reduction
ci.Clean()
ci.UseCompatibilityMode()
ci.SANS2D()
ci.MaskFile('MaskSANS2DReductionGUI_LimitEventsTime.txt')
ci.AssignSample('22048')
ci.WavRangeReduction()
