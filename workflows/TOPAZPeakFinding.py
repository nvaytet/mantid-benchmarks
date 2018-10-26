# Mantid Repository : https://github.com/mantidproject/mantid
#
# Copyright &copy; 2018 ISIS Rutherford Appleton Laboratory UKRI,
#     NScD Oak Ridge National Laboratory, European Spallation Source
#     & Institut Laue - Langevin
# SPDX - License - Identifier: GPL - 3.0 +
#pylint: disable=no-init,invalid-name
"""
System test that loads TOPAZ single-crystal data,
converts to Q space, finds peaks and indexes
them.
"""
import sys
sys.path.append("../tools")
import workflow_config as wfc
sys.path.extend(wfc.sys_path_ext)
import os
cwd = os.getcwd()
import numpy

from mantid import config, AnalysisDataService
from mantid.simpleapi import *

config['datasearch.searcharchive'] = 'off'
config.setDataSearchDirs(wfc.datadirs["TOPAZPeakFinding"])


## Load then convert to Q in the lab frame
LoadEventNexus(Filename=r'TOPAZ_3132_event.nxs',OutputWorkspace='topaz_3132')
ConvertToDiffractionMDWorkspace(InputWorkspace='topaz_3132',OutputWorkspace='topaz_3132_MD',
                                LorentzCorrection='1',SplitInto='2',SplitThreshold='150',OneEventPerBin='0')

# Find peaks and UB matrix
FindPeaksMD(InputWorkspace='topaz_3132_MD',PeakDistanceThreshold='0.12',MaxPeaks='200',OutputWorkspace='peaks')
FindUBUsingFFT(PeaksWorkspace='peaks',MinD='2',MaxD='16')

# Index the peaks and check
results = IndexPeaks(PeaksWorkspace='peaks')
indexed = results[0]
if indexed < 199:
    raise Exception("Expected at least 199 of 200 peaks to be indexed. Only indexed %d!" % indexed)

# Check the oriented lattice
CopySample(InputWorkspace='peaks',OutputWorkspace='topaz_3132',CopyName='0',CopyMaterial='0',CopyEnvironment='0',CopyShape='0')
originalUB = numpy.array(mtd["topaz_3132"].sample().getOrientedLattice().getUB())
w = mtd["topaz_3132"]
s = w.sample()
ol = s.getOrientedLattice()


# Go to HKL
ConvertToDiffractionMDWorkspace(InputWorkspace='topaz_3132',OutputWorkspace='topaz_3132_HKL',
                                OutputDimensions='HKL',LorentzCorrection='1',SplitInto='2',SplitThreshold='150')

# Bin to a line (H=0 to 6, L=3, K=3)
BinMD(InputWorkspace='topaz_3132_HKL',AxisAligned='0',
      BasisVector0='X,units,1,0,0',BasisVector1='Y,units,6.12323e-17,1,0',BasisVector2='2,units,-0,0,1',
      Translation='-0,3,6',OutputExtents='0,6, -0.1,0.1, -0.1,0.1',OutputBins='60,1,1',
      OutputWorkspace='topaz_3132_HKL_line')

# Now check the integrated bin and the peaks
w = mtd["topaz_3132_HKL_line"]
# Now do the same peak finding with Q in the sample frame
ConvertToDiffractionMDWorkspace(InputWorkspace='topaz_3132',OutputWorkspace='topaz_3132_QSample',
                                OutputDimensions='Q (sample frame)',LorentzCorrection='1',SplitInto='2',SplitThreshold='150')
FindPeaksMD(InputWorkspace='topaz_3132_QSample',PeakDistanceThreshold='0.12',MaxPeaks='200',OutputWorkspace='peaks_QSample')
FindUBUsingFFT(PeaksWorkspace='peaks_QSample',MinD='2',MaxD='16')
CopySample(InputWorkspace='peaks_QSample',OutputWorkspace='topaz_3132',CopyName='0',CopyMaterial='0',
           CopyEnvironment='0',CopyShape='0')

# Index the peaks and check
results = IndexPeaks(PeaksWorkspace='peaks_QSample')
indexed = results[0]
if indexed < 199:
    raise Exception("Expected at least 199 of 200 peaks to be indexed. Only indexed %d!" % indexed)


