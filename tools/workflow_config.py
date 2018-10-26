# Set-up config

# Igor
# sys_path_ext = ['/home/igudich/work/MyMantid/mantid/python3Build/bin']
# datadirs = {}
# datadir = "/home/igudich/work/mantid/cmake-build-release-gcc/ExternalData/Testing/Data/SystemTest"
# datadir += ";/media/igudich/2ecb279f-1d34-4ab5-8a8a-224220f5d50f/SNSReductionFiles"
# datadirs.update({"SNSPowderReduction": datadir})
#
# datadir = "/home/igudich/work/mantid/cmake-build-release-gcc/ExternalData/Testing/Data/SystemTest"
# datadir += ";/media/igudich/2ecb279f-1d34-4ab5-8a8a-224220f5d50f/Diffraction_WorkflowFiles"
# datadirs.update({"Diffraction_WorkflowFiles": datadir})

# Neil
sys_path_ext = ['/home/igudich/work/MyMantid/mantid/python3Build/bin']

systemTestDir = "/home/igudich/work/mantid/cmake-build-release-gcc/ExternalData/Testing/Data/SystemTest"
datadirs = {}

# SNSPowderReduction
datadir = "/media/igudich/2ecb279f-1d34-4ab5-8a8a-224220f5d50f/SNSReductionFiles/data_fact016"
datadirs.update({"SNSPowderReduction": datadir + ";" + systemTestDir})

# SANSReduction1
datadir = "/media/nvaytet/30c9d25c-0aba-427f-b8ea-3079e881dfce/benchmarks_data/SANS2D_data/data_fact10000"
datadirs.update({"SANSReduction1": datadir + ";" + systemTestDir + "/SANS2D"})

# SANSReduction2
datadir = ""
datadirs.update({"SANSReduction2": systemTestDir + "/SANS2D"})

# DGSReduction
datadir = "/media/nvaytet/30c9d25c-0aba-427f-b8ea-3079e881dfce/benchmarks_data/DGSReduction_data"
datadirs.update({"DGSReduction": datadir + ";" + systemTestDir})

# Diffraction_Workflow
datadir = "/media/igudich/2ecb279f-1d34-4ab5-8a8a-224220f5d50f/Diffraction_WorkflowFiles/data_fact010"
datadirs.update({"Diffraction_WorkflowFiles": datadir + ";" + systemTestDir})

# SXD_NaCl
datadir = ""
datadirs.update({"SXD_NaCl": datadir + ";" + systemTestDir})
