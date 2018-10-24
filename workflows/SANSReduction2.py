from __future__ import (absolute_import, division, print_function)

import sys
sys.path.append("../tools")
import workflow_config as wfc
sys.path.extend(wfc.sys_path_ext)

import mantid  # noqa
from mantid.api import AlgorithmManager
from sans.user_file.state_director import StateDirectorISIS
from sans.state.data import get_data_builder
from sans.common.enums import (SANSFacility, ISISReductionMode, ReductionDimensionality, FitModeForMerge)
from sans.common.constants import EMPTY_NAME
from sans.common.general_functions import create_unmanaged_algorithm
from sans.common.file_information import SANSFileInformationFactory


# Set-up config
config['datasearch.searcharchive'] = 'off'
config.setDataSearchDirs(wfc.datadirs["SANSReduction2"])


def _load_workspace(state):
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
    # assertTrue(load_alg.isExecuted())
    sample_scatter = load_alg.getProperty("SampleScatterWorkspace").value
    sample_scatter_monitor_workspace = load_alg.getProperty("SampleScatterMonitorWorkspace").value
    transmission_workspace = load_alg.getProperty("SampleTransmissionWorkspace").value
    direct_workspace = load_alg.getProperty("SampleDirectWorkspace").value

    can_scatter_workspace = load_alg.getProperty("CanScatterWorkspace").value
    can_scatter_monitor_workspace = load_alg.getProperty("CanScatterMonitorWorkspace").value
    can_transmission_workspace = load_alg.getProperty("CanTransmissionWorkspace").value
    can_direct_workspace = load_alg.getProperty("CanDirectWorkspace").value

    return sample_scatter, sample_scatter_monitor_workspace, transmission_workspace, direct_workspace, \
           can_scatter_workspace, can_scatter_monitor_workspace, can_transmission_workspace, can_direct_workspace  # noqa

def _run_single_reduction(state, sample_scatter, sample_monitor, sample_transmission=None, sample_direct=None,
                          can_scatter=None, can_monitor=None, can_transmission=None, can_direct=None,
                          output_settings=None):
    single_reduction_name = "SANSSingleReduction"
    state_dict = state.property_manager

    single_reduction_options = {"SANSState": state_dict,
                                "SampleScatterWorkspace": sample_scatter,
                                "SampleScatterMonitorWorkspace": sample_monitor,
                                "UseOptimizations": False}
    if sample_transmission:
        single_reduction_options.update({"SampleTransmissionWorkspace": sample_transmission})

    if sample_direct:
        single_reduction_options.update({"SampleDirectWorkspace": sample_direct})

    if can_scatter:
        single_reduction_options.update({"CanScatterWorkspace": can_scatter})

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
    # assertTrue(single_reduction_alg.isExecuted())
    return single_reduction_alg

def _compare_workspace(workspace, reference_file_name, check_spectra_map=True):
    # Load the reference file
    load_name = "LoadNexusProcessed"
    load_options = {"Filename": reference_file_name,
                    "OutputWorkspace": EMPTY_NAME}
    load_alg = create_unmanaged_algorithm(load_name, **load_options)
    load_alg.execute()
    reference_workspace = load_alg.getProperty("OutputWorkspace").value

    # Compare reference file with the output_workspace
    # We need to disable the instrument comparison, it takes way too long
    # We need to disable the sample -- Not clear why yet
    # operation how many entries can be found in the sample logs
    compare_name = "CompareWorkspaces"
    compare_options = {"Workspace1": workspace,
                       "Workspace2": reference_workspace,
                       "Tolerance": 1e-6,
                       "CheckInstrument": False,
                       "CheckSample": False,
                       "ToleranceRelErr": True,
                       "CheckAllData": True,
                       "CheckMasking": True,
                       "CheckType": True,
                       "CheckAxes": True,
                       "CheckSpectraMap": check_spectra_map}
    compare_alg = create_unmanaged_algorithm(compare_name, **compare_options)
    compare_alg.setChild(False)
    compare_alg.execute()
    result = compare_alg.getProperty("Result").value
    # self.assertTrue(result)

# Arrange
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

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# COMPATIBILITY BEGIN -- Remove when appropriate
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Since we are dealing with event based data but we want to compare it with histogram data from the
# old reduction system we need to enable the compatibility mode
user_file_director.set_compatibility_builder_use_compatibility_mode(True)
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# COMPATIBILITY END
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
state = user_file_director.construct()
state.adjustment.show_transmission = True

# Load the sample workspaces
sample, sample_monitor, transmission_workspace, direct_workspace, can, can_monitor, \
can_transmission, can_direct = _load_workspace(state)  # noqa

# Act
output_settings = {"OutputWorkspaceLAB": EMPTY_NAME}
single_reduction_alg = _run_single_reduction(state, sample_scatter=sample,
                                                  sample_transmission=transmission_workspace,
                                                  sample_direct=direct_workspace,
                                                  sample_monitor=sample_monitor,
                                                  can_scatter=can,
                                                  can_monitor=can_monitor,
                                                  can_transmission=can_transmission,
                                                  can_direct=can_direct,
                                                  output_settings=output_settings)
