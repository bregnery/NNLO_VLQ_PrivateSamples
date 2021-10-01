from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.requestName = 'NLO_step4_VLQ_HLT'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'NLO_VLQ_custom_HLT_cfg.py'
#config.JobType.numCores = 4
config.JobType.maxMemoryMB = 5000

config.section_('Data')
config.Data.inputDataset = '/MinBias/bregnery-NLO_step3_VLQ_SIM-dc83d1937f4e2e47e7fbf2afb7ff79b9/USER'
config.Data.inputDBS = 'phys03'
config.Data.allowNonValidInputDataset = True
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/bregnery/' 
config.Data.publication = True
config.Data.outputDatasetTag = 'NLO_step4_VLQ_HLT'

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
