# NNLO_VLQ_PrivateSamples

First off, I apologize for the name of this repository. These samples are actually NLO.

## Running locally

These are the instructions to run directly in CMSSW to make small statistics samples (~100 events).

```
# Make sure to have the appropriate CMSSW release
cd CMSSW_10_6_19/src
git clone

# Copy the appropriate python fragments
cp -r NNLO_VLQ_PrivateSamples/Configuration .

# Set up the environment
cmsenv
scram b

# get a grid proxy

# First run through MadGraph and Pythia
cmsRun NNLO_VLQ_custom_python_cfg.py

# Now run the detector simulation
cmsRun NLO_VLQ_custom_SIM_cfg.py

# Create the Digis
cmsRun NLO_VLQ_custom_DIGIPremix_cfg.py

# Now the HLT is needed, but this requires a different version of CMSSW
cd ../../
cmsrel CMSSW_8_0_33_UL
cd CMSSW_8_0_33_UL/src
cmsenv
cd ../../CMSSW_10_6_19/NNLO_VLQ_PrivateSamples

cmsRun NLO_VLQ_custom_HLT_cfg.py

# Now return to the new CMSSW and run the reconstruction
cmsenv
cmsRun NLO_VLQ_custom_RECO_cfg.py

# Finally, run the MiniAOD
cmsRun NLO_VLQ_custom_MiniAOD_cfg.py

```

## Running with CRAB

Please note that it is very important to use the adapted Generic tarball script in order for the crab jobs to succeed properly.

```
# Make sure to have the appropriate CMSSW release
cd CMSSW_10_6_19/src
git clone

# Copy the appropriate python fragments
cp -r NNLO_VLQ_PrivateSamples/Configuration .

# Set up the environment
cmsenv
scram b
cd CrabRunFiles

# get a grid proxy

# First run through MadGraph and Pythia
crab submit submit_step1_SIM_crab.py

# Now run the detector simulation
crab submit submit_step2_SIM_crab.py

# Create the Digis
crab submit submit_step3_DIGIPremix_crab.py

# Now the HLT is needed, but this requires a different version of CMSSW
cd ../../
cmsrel CMSSW_8_0_33_UL
cd CMSSW_8_0_33_UL/src
cmsenv
cd ../../CMSSW_10_6_19/NNLO_VLQ_PrivateSamples

crab submit submit_step4_HLT_crab.py

# Now return to the new CMSSW and run the reconstruction 
cmsenv
crab submit submit_step5_RECO_crab.py

# Finally, run the MiniAOD
crab submit submit_step6_MiniAOD_crab.py

```
## Common Errors

IMPORTANT: The `run_generic_tarball.sh` script automatically included in CMSSW does not have the ability to access files on EOS, so I had to adapt this script to access such files. If the first step of crab submission fails with an error saying `tar: <filepath>` and `permission denied` it is likely due to the incorrect `run_generic_tarball.sh`


## Creation of the CMS Configuration Files

```
cd CMSSW_10_6_19/src
git clone
cp -r NNLO_VLQ_PrivateSamples/Configuration .
cd NNLO_VLQ_PrivateSamples

cmsenv
# get a grid proxy

cmsDriver.py Configuration/GenProduction/python/NNLO_VLQ_custom_python_fragment.py --python_filename NNLO_VLQ_custom_python_cfg.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN,LHE --fileout file:NNLO_VLQ_custom.root --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step LHE,GEN --geometry DB:Extended --era Run2_2016 --no_exec --mc -n 1000

cmsRun NNLO_VLQ_custom_python_cfg.py
# This file had to be modified for use with crab an on an EOS space. Specifically the "genericTarball" script had to be altered. To see the final version, look under CrabRunScripts

cmsDriver.py  --python_filename NLO_VLQ_custom_SIM_cfg.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --fileout file:NLO_VLQ_custom_SIM.root --conditions 106X_mcRun2_asymptotic_v13 --beamspot Realistic25ns13TeV2016Collision --step SIM --geometry DB:Extended --filein file:NNLO_VLQ_custom.root --era Run2_2016 --runUnscheduled --no_exec --mc -n 100

cmsRun NLO_VLQ_custom_SIM_cfg.py

cmsDriver.py  --python_filename NLO_VLQ_custom_DIGIPremix_cfg.py --eventcontent PREMIXRAW --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-DIGI --fileout file:NLO_VLQ_custom_DIGIPremix.root --pileup_input "dbs:/Neutrino_E-10_gun/RunIISummer20ULPrePremix-UL16_106X_mcRun2_asymptotic_v13-v1/PREMIX" --conditions 106X_mcRun2_asymptotic_v13 --step DIGI,DATAMIX,L1,DIGI2RAW --procModifiers premix_stage2 --geometry DB:Extended --filein file:NLO_VLQ_custom_SIM.root --datamix PreMix --era Run2_2016 --runUnscheduled --no_exec --mc -n 100

cmsRun NLO_VLQ_custom_DIGIPremix_cfg.py

cd ../../
cmsrel CMSSW_8_0_33_UL
cd CMSSW_8_0_33_UL/src
cmsenv

cmsDriver.py  --python_filename NLO_VLQ_custom_HLT_cfg.py --eventcontent RAWSIM --outputCommand "keep *_mix_*_*,keep *_genPUProtons_*_*" --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM-RAW --inputCommands "keep *","drop *_*_BMTF_*","drop *PixelFEDChannel*_*_*_*" --fileout file:NLO_VLQ_custom_HLT.root --conditions 80X_mcRun2_asymptotic_2016_TrancheIV_v6 --customise_commands 'process.source.bypassVersionCheck = cms.untracked.bool(True)' --step HLT:25ns15e33_v4 --geometry DB:Extended --filein file:NLO_VLQ_custom_DIGIPremix.root --era Run2_2016 --no_exec --mc -n 100

cd ../../CMSSW_10_6_19/src/NNLO_VLQ_PrivateSamples

cmsDriver.py  --python_filename NLO_VLQ_custom_RECO_cfg.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:NLO_VLQ_custom_RECO.root --conditions 106X_mcRun2_asymptotic_v13 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:NLO_VLQ_custom_HLT.root --era Run2_2016 --runUnscheduled --no_exec --mc -n 100

cmsRun NLO_VLQ_custom_RECO_cfg.py

cmsDriver.py  --python_filename NLO_VLQ_custom_MiniAOD_cfg.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:NLO_VLQ_custom_MiniAOD.root --conditions 106X_mcRun2_asymptotic_v13 --step PAT --geometry DB:Extended --filein file:NLO_VLQ_custom_RECO.root --era Run2_2016 --runUnscheduled --no_exec --mc -n 100

cmsRun NLO_VLQ_custom_MiniAOD_cfg.py


```
