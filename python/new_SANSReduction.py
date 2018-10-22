# from sans.command_interface.ISISCommandInterface import *
import mantid  # noqa
import sans.command_interface.ISISCommandInterface as ci
import tree_walk

datadir = "/home/nvaytet/aaa_work/code/mantid/sources/clean/build/ExternalData/Testing/Data/SystemTest"
mantid.config['datasearch.searcharchive'] = 'off'

# filesize_list = [1,2,4,8,16]
# nthreads_list = [1,2,4,8,12,16,20,24]
filesize_list = [1]
nthreads_list = [1]

for i in filesize_list:
    for j in nthreads_list:

        # Start fresh
        mantid.AnalysisDataService.clear()
        # Set-up config
        mantid.config['datasearch.directories'] = datadir + "/SANS2D"
        mantid.config['MultiThreaded.MaxCores'] = str(j)

        ci.Clean()
        ci.UseCompatibilityMode()
        ci.SANS2D()
        ci.MaskFile('MaskSANS2DReductionGUI_LimitEventsTime.txt')
        ci.AssignSample('22048')
        ci.WavRangeReduction()

        # Gather history and write it to file
        # names = AnalysisDataService.getObjectNames()
        w = mantid.AnalysisDataService['22048rear_1D_1.5_12.5']
        h = w.getHistory()
        ah = h.getAlgorithmHistories()
        fname = "SANSReduction_fact_%03d-nthreads_%03d"%(i,j)
        for k in ah:
            t = tree_walk.Tree(k)
            t.view(fname)
