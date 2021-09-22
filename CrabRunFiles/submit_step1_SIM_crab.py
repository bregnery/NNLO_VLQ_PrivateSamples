from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.requestName = 'NLO_step1_VLQ_SIM'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'NNLO_VLQ_custom_python_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.section_('Data')
#config.Data.userInputFiles = ['run_generic_tarball_cvmfs.sh']
config.Data.outputPrimaryDataset = 'MinBias'
config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = 10
NJOBS = 100  # This is not a configuration parameter, but an auxiliary variable that we use in the next line.
config.Data.totalUnits = config.Data.unitsPerJob * NJOBS
config.Data.outLFNDirBase = '/store/user/bregnery/' 
config.Data.publication = True
config.Data.outputDatasetTag = 'NLO_step1_VLQ_SIM'

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'

