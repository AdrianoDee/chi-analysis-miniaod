#input_filename = '/store/data/Run2017B/MuOnia/MINIAOD/PromptReco-v1/000/297/723/00000/9040368C-DE5E-E711-ACFF-02163E0134FF.root'
ouput_filename = 'rootuple.root'

import FWCore.ParameterSet.Config as cms
process = cms.Process("Rootuple")

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '92X_dataRun2_Prompt_v9', '')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10000))

process.source = cms.Source("PoolSource",fileNames = cms.untracked.vstring(
#'/store/data/Run2017C/MuOnia/MINIAOD/PromptReco-v1/000/299/368/00000/FA04E254-876D-E711-A303-02163E0128D1.root',
#'/store/data/Run2017D/MuOnia/MINIAOD/PromptReco-v1/000/302/031/00000/0E919B66-3B8F-E711-B6B4-02163E0144E5.root',
'/store/data/Run2017E/MuOnia/MINIAOD/PromptReco-v1/000/303/817/00000/F24D6405-8EA2-E711-9303-02163E01A28F.root',
#'/store/data/Run2017F/MuOnia/MINIAOD/PromptReco-v1/000/305/040/00000/26C723C4-25B2-E711-A70D-02163E01A64C.root',
	)
)
process.TFileService = cms.Service("TFileService",fileName = cms.string(ouput_filename))
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))

process.load("Ponia.OniaPhoton.slimmedMuonsTriggerMatcher2017_cfi")

# In MiniAOD, the PATMuons are already present. We just need to run Onia2MuMu, with a selection of muons.
process.oniaSelectedMuons = cms.EDFilter('PATMuonSelector',
   src = cms.InputTag('slimmedMuonsWithTrigger'),
   cut = cms.string('muonID(\"TMOneStationTight\")'
                    ' && abs(innerTrack.dxy) < 0.3'
                    ' && abs(innerTrack.dz)  < 20.'
                    ' && innerTrack.hitPattern.trackerLayersWithMeasurement > 5'
                    ' && innerTrack.hitPattern.pixelLayersWithMeasurement > 0'
                    ' && innerTrack.quality(\"highPurity\")'
                    ' && (pt > 4.)'
                    #' && (abs(eta) <= 1.4 && pt > 4.)'
   ),
   filter = cms.bool(True)
)

process.load("HeavyFlavorAnalysis.Onia2MuMu.onia2MuMuPAT_cfi")
process.onia2MuMuPAT.muons=cms.InputTag('oniaSelectedMuons')
process.onia2MuMuPAT.primaryVertexTag=cms.InputTag('offlineSlimmedPrimaryVertices')
process.onia2MuMuPAT.beamSpotTag=cms.InputTag('offlineBeamSpot')
process.onia2MuMuPAT.higherPuritySelection=cms.string("")
process.onia2MuMuPAT.lowerPuritySelection=cms.string("")
process.onia2MuMuPAT.dimuonSelection=cms.string("8.5 < mass && mass < 11.5")
process.onia2MuMuPAT.addMCTruth = cms.bool(False)

process.triggerSelection = cms.EDFilter("TriggerResultsFilter",
                                        triggerConditions = cms.vstring('HLT_Dimuon10_Upsilon_Barrel_Seagulls_v*',
                                                                        'HLT_Dimuon12_Upsilon_eta1p5_v*',
                                                                        'HLT_Dimuon24_Upsilon_noCorrL1_v*'
                                                                       ),
                                        hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
                                        l1tResults = cms.InputTag( "" ),
                                        throw = cms.bool(False)
                                        )

process.Onia2MuMuFiltered = cms.EDProducer('DiMuonFilter',
      OniaTag             = cms.InputTag("onia2MuMuPAT"),
      singlemuonSelection = cms.string(""),
      #dimuonSelection     = cms.string("8.6 < mass && mass < 11.4 && pt > 10. && abs(y) < 1.2 && charge==0 && userFloat('vProb') > 0.01"),
      dimuonSelection     = cms.string("8.6 < mass && mass < 11.4 && pt > 10. && charge==0 && userFloat('vProb') > 0.01"),
      do_trigger_match    = cms.bool(True),
      HLTFilters          = cms.vstring(
                'hltDisplacedmumuFilterDimuon10UpsilonBarrelnoCow',
                'hltDisplacedmumuFilterDimuon12Upsilons',
                'hltDisplacedmumuFilterDimuon24UpsilonsNoCorrL1'
                          ),
)

process.DiMuonCounter = cms.EDFilter('CandViewCountFilter',
    src       = cms.InputTag("Onia2MuMuFiltered"),
    minNumber = cms.uint32(1),
    filter    = cms.bool(True)
)

process.chiProducer = cms.EDProducer('OniaPhotonProducer',
    conversions     = cms.InputTag("oniaPhotonCandidates","conversions"),
    dimuons         = cms.InputTag("Onia2MuMuFiltered"),
    pi0OnlineSwitch = cms.bool(False),
    deltaMass       = cms.vdouble(0.0,2.0),
    dzmax           = cms.double(0.5),
    triggerMatch    = cms.bool(False)  # trigger match is performed in Onia2MuMuFiltered
)

process.chiFitter1S = cms.EDProducer('OniaPhotonKinematicFit',
                          chi_cand = cms.InputTag("chiProducer"),
                          upsilon_mass = cms.double(9.46030), # GeV   1S = 9.46030   2S = 10.02326    3S = 10.35520  J/psi=3.0969
                          product_name = cms.string("y1S")
                         )

process.chiFitter2S = cms.EDProducer('OniaPhotonKinematicFit',
                          chi_cand = cms.InputTag("chiProducer"),
                          upsilon_mass = cms.double(10.02326), # GeV   1S = 9.46030   2S = 10.02326    3S = 10.35520  J/psi=3.0969
                          product_name = cms.string("y2S")
                         )

process.chiFitter3S = cms.EDProducer('OniaPhotonKinematicFit',
                          chi_cand = cms.InputTag("chiProducer"),
                          upsilon_mass = cms.double(10.35520), # GeV   1S = 9.46030   2S = 10.02326    3S = 10.35520  J/psi=3.0969
                          product_name = cms.string("y3S")
                         )

process.chiSequence = cms.Sequence(
                                   process.triggerSelection *
				   process.slimmedMuonsWithTriggerSequence *
				   process.oniaSelectedMuons *
				   process.onia2MuMuPAT *
				   process.Onia2MuMuFiltered *
		                   process.DiMuonCounter *
				   process.chiProducer *
				   process.chiFitter1S *
                                   process.chiFitter2S *
                                   process.chiFitter3S
				   )

process.rootuple = cms.EDAnalyzer('chibRootupler',
                          chi_cand = cms.InputTag("chiProducer"),
			  ups_cand = cms.InputTag("Onia2MuMuFiltered"),
                          refit1S  = cms.InputTag("chiFitter1S","y1S"),
			  refit2S  = cms.InputTag("chiFitter2S","y2S"),
			  refit3S  = cms.InputTag("chiFitter3S","y3S"),
                          primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices"),
                          TriggerResults  = cms.InputTag("TriggerResults", "", "HLT"),
                          isMC = cms.bool(False)
                         )

process.p = cms.Path(process.chiSequence*process.rootuple)
