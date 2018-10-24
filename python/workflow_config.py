# Set-up config
sys_path_ext = ['/home/igudich/work/MyMantid/mantid/python3Build/bin']
datadirs = {}
datadir = "/home/igudich/work/mantid/cmake-build-release-gcc/ExternalData/Testing/Data/SystemTest"
datadir += ";/media/igudich/2ecb279f-1d34-4ab5-8a8a-224220f5d50f/SNSReductionFiles"
datadirs.update({"SNSPowderReduction": datadir})

datadir = "/home/igudich/work/mantid/cmake-build-release-gcc/ExternalData/Testing/Data/SystemTest"
datadir += ";/media/igudich/2ecb279f-1d34-4ab5-8a8a-224220f5d50f/Diffraction_WorkflowFiles"
datadirs.update({"Diffraction_WorkflowFiles": datadir})
