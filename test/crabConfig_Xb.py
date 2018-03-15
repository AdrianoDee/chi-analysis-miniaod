from WMCore.Configuration import Configuration
config = Configuration()

datasetnames = [
'/MuOnia/Run2017B-PromptReco-v1/MINIAOD', # 0
'/MuOnia/Run2017B-PromptReco-v2/MINIAOD', # 1
'/MuOnia/Run2017C-PromptReco-v1/MINIAOD', # 2
'/MuOnia/Run2017C-PromptReco-v2/MINIAOD', # 3
'/MuOnia/Run2017C-PromptReco-v3/MINIAOD', # 4
'/MuOnia/Run2017D-PromptReco-v1/MINIAOD', # 5
'/MuOnia/Run2017E-PromptReco-v1/MINIAOD', # 6
'/MuOnia/Run2017F-PromptReco-v1/MINIAOD' # 7
]

runNumber = [
'',
'297620,297656',
'299420'
]

jsonfile = [
'',
'/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON_MuonPhys.txt'
]

eventsPerJob = [
10,
20
]

datasetName = datasetnames[7]
runNum = runNumber[0]
lumi = jsonfile[1]
epj = eventsPerJob[0]

import datetime
timestamp = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

dataset = filter(None, datasetName.split('/'))

config.section_('General')
config.General.transferOutputs  = True
config.General.workArea         = 'ChiB_v1'
config.General.requestName      = dataset[0]+'_'+dataset[1]+'_'+dataset[2]+'_'+runNum+timestamp
config.General.transferLogs     = False

config.section_('JobType')
config.JobType.psetName         = 'run-chib-miniaod.py'
config.JobType.pluginName       = 'Analysis'
config.JobType.maxMemoryMB      = 2500
config.JobType.maxJobRuntimeMin = 2750
#config.JobType.numCores         = 4
#config.JobType.outputFiles      = ['hltbits.root']

config.section_('Data')
config.Data.inputDataset        = datasetName
config.Data.inputDBS            = 'global'
config.Data.totalUnits          = -1
config.Data.unitsPerJob         = epj
config.Data.splitting           = 'LumiBased'
config.Data.runRange            = runNum
config.Data.lumiMask            = lumi
config.Data.outLFNDirBase       = '/store/user/slezki/ChiB_v1'
config.Data.publication         = False
#config.Data.ignoreLocality      = True

config.section_('Site')
config.Site.storageSite         = 'T2_IT_Bari'
#config.Site.blacklist           = ['T2_TW_NCHC', 'T2_US_Vanderbilt']
#config.Site.blacklist           = ['T1*', 'T2_BR_SPRACE', 'T2_US_Wisconsin', 'T1_RU_JINR', 'T2_RU_JINR', 'T2_EE_Estonia']
#config.Site.whitelist		= ['T1*', 'T2*']
