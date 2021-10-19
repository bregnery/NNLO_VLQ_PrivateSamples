from WMCore.Configuration import Configuration
config = Configuration()

config.section_('General')
config.General.requestName = 'NLO_step6_VLQ_MiniAOD'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'NLO_VLQ_custom_MiniAOD_cfg.py'
#config.JobType.numCores = 4
config.JobType.maxMemoryMB = 2500

config.section_('Data')
config.Data.inputDataset = '/MinBias/bregnery-NLO_step5_VLQ_RECO-7c769ea03680f752cd212ca9a9c09012/USER'
config.Data.inputDBS = 'phys03'
config.Data.allowNonValidInputDataset = True
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/bregnery/' 
config.Data.publication = True
config.Data.outputDatasetTag = 'NLO_step6_VLQ_MiniAOD'

config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'
