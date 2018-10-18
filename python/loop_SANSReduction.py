import os
import tree_walk
cwd = os.getcwd()

import mantid  # noqa
from mantid.api import AlgorithmManager
from sans.user_file.state_director import StateDirectorISIS
from sans.state.data import get_data_builder
from sans.common.enums import (SANSFacility, ISISReductionMode, ReductionDimensionality, FitModeForMerge)
from sans.common.constants import EMPTY_NAME
from sans.common.general_functions import create_unmanaged_algorithm
from sans.common.file_information import SANSFileInformationFactory

datadir = "/home/nvaytet/aaa_work/code/mantid/sources/clean/build/ExternalData/Testing/Data/SystemTest"
# datadir += ";/media/nvaytet/30c9d25c-0aba-427f-b8ea-3079e881dfce/benchmarks_data/SNSPowderReduction_data"
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

        # SANS reduction start =================================================

        # Build the data information
        file_information_factory = SANSFileInformationFactory()
        file_information = file_information_factory.create_sans_file_information("SANS2D00034484")
        data_builder = get_data_builder(SANSFacility.ISIS, file_information)
        data_builder.set_sample_scatter("SANS2D00034484")
        data_builder.set_sample_transmission("SANS2D00034505")
        data_builder.set_sample_direct("SANS2D00034461")
        data_builder.set_can_scatter("SANS2D00034481")
        data_builder.set_can_transmission("SANS2D00034502")
        data_builder.set_can_direct("SANS2D00034461")

        data_builder.set_calibration("TUBE_SANS2D_BOTH_31681_25Sept15.nxs")
        data_info = data_builder.build()

        # Get the rest of the state from the user file
        user_file_director = StateDirectorISIS(data_info, file_information)
        user_file_director.set_user_file("USER_SANS2D_154E_2p4_4m_M3_Xpress_8mm_SampleChanger.txt")
        # Set the reduction mode to LAB
        user_file_director.set_reduction_builder_reduction_mode(ISISReductionMode.LAB)
        user_file_director.set_compatibility_builder_use_compatibility_mode(True)
        state = user_file_director.construct()
        state.adjustment.show_transmission = True

        # Load the sample workspaces
        load_alg = AlgorithmManager.createUnmanaged("SANSLoad")
        load_alg.setChild(True)
        load_alg.initialize()

        state_dict = state.property_manager
        load_alg.setProperty("SANSState", state_dict)
        load_alg.setProperty("PublishToCache", False)
        load_alg.setProperty("UseCached", False)
        load_alg.setProperty("MoveWorkspace", False)

        load_alg.setProperty("SampleScatterWorkspace", EMPTY_NAME)
        load_alg.setProperty("SampleScatterMonitorWorkspace", EMPTY_NAME)
        load_alg.setProperty("SampleTransmissionWorkspace", EMPTY_NAME)
        load_alg.setProperty("SampleDirectWorkspace", EMPTY_NAME)

        load_alg.setProperty("CanScatterWorkspace", EMPTY_NAME)
        load_alg.setProperty("CanScatterMonitorWorkspace", EMPTY_NAME)
        load_alg.setProperty("CanTransmissionWorkspace", EMPTY_NAME)
        load_alg.setProperty("CanDirectWorkspace", EMPTY_NAME)

        # Act
        load_alg.execute()
        sample = load_alg.getProperty("SampleScatterWorkspace").value
        sample_monitor = load_alg.getProperty("SampleScatterMonitorWorkspace").value
        transmission_workspace = load_alg.getProperty("SampleTransmissionWorkspace").value
        direct_workspace = load_alg.getProperty("SampleDirectWorkspace").value

        can = load_alg.getProperty("CanScatterWorkspace").value
        can_monitor = load_alg.getProperty("CanScatterMonitorWorkspace").value
        can_transmission = load_alg.getProperty("CanTransmissionWorkspace").value
        can_direct = load_alg.getProperty("CanDirectWorkspace").value

        # Act
        output_settings = {"OutputWorkspaceLAB": EMPTY_NAME}
        single_reduction_name = "SANSSingleReduction"
        single_reduction_options = {"SANSState": state_dict,
                                    "SampleScatterWorkspace": sample,
                                    "SampleScatterMonitorWorkspace": sample_monitor,
                                    "UseOptimizations": False}
        if transmission_workspace:
            single_reduction_options.update({"SampleTransmissionWorkspace": transmission_workspace})

        if direct_workspace:
            single_reduction_options.update({"SampleDirectWorkspace": direct_workspace})

        if can:
            single_reduction_options.update({"CanScatterWorkspace": can})

        if can_monitor:
            single_reduction_options.update({"CanScatterMonitorWorkspace": can_monitor})

        if can_transmission:
            single_reduction_options.update({"CanTransmissionWorkspace": can_transmission})

        if can_direct:
            single_reduction_options.update({"CanDirectWorkspace": can_direct})

        if output_settings:
            single_reduction_options.update(output_settings)

        single_reduction_alg = create_unmanaged_algorithm(single_reduction_name, **single_reduction_options)

        # Act
        single_reduction_alg.execute()

        # SANS reduction end ===================================================

        # Gather history and write it to file
        # names = mantid.api.AnalysisDataService.getObjectNames()
        # w = mantid.api.AnalysisDataService['OutputWorkspaceLAB']
        w = single_reduction_alg.getProperty("OutputWorkspaceLAB").value
        h = w.getHistory()
        ah = h.getAlgorithmHistories()
        fname = "fact_%03d-nthreads_%03d"%(i,j)
        for k in ah:
            t = tree_walk.Tree(k)
            t.view(fname)
