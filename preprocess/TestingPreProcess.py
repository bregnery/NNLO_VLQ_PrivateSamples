import sys
import os
import math
import glob
import ROOT as root
from array import array
root.gROOT.SetBatch(True)

# load FWLite C++ libraries
root.gSystem.Load("libFWCoreFWLite.so");
root.gSystem.Load("libDataFormatsFWLite.so");
root.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

class Collections(object):
    '''
    Simple collection manager for FWLite
    '''

    def __init__(self):
        self.__collections = {}

    def add(self, name, cppType, label):
        self.__collections[name] = {'handle': Handle(cppType), 'label': label,}

    def get(self, name, event):
        label = self.__collections[name]['label']
        handle = self.__collections[name]['handle']
        event.getByLabel(label,handle)
        return handle.product()

def deltaPhi(phi0,phi1):
    result = phi0-phi1
    while result>root.TMath.Pi():
        result -= 2*root.TMath.Pi()
    while result<=-root.TMath.Pi():
        result += 2*root.TMath.Pi()
    return result

def deltaR(eta0,phi0,eta1,phi1):
    deta = eta0-eta1
    dphi = deltaPhi(phi0,phi1)
    return root.TMath.Sqrt(deta**2+dphi**2)


typeMap = {
    'I': int,
    'l': long,
    'F': float,
    'C': str,
}
arrayMap = {
    'I': 'i',
    'l': 'L',
    'F': 'f',
}

class AnalysisTree(object):
    def __init__(self):
        self.results = {}
        self.tree = root.TTree("AnalysisTree","AnalysisTree")
        self.results['run'] = array('i',[0])
        self.results['lumi'] = array('i',[0])
        self.results['event'] = array('L',[0])
        self.tree.Branch('run',self.results['run'],'run/I')
        self.tree.Branch('lumi',self.results['lumi'],'lumi/I')
        self.tree.Branch('event',self.results['event'],'event/l')

    def add(self,var,rootType):
        if var in self.results:
            logging.error('Attempting to add repeated variable "{0}"'.format(var))
            return
        if rootType in arrayMap:
            self.results[var] = array(arrayMap[rootType],[0])
            self.tree.Branch(var,self.results[var],'{0}/{1}'.format(var,rootType))
        else:
            self.results[var] = rootType
            self.tree.Branch(var,self.results[var])

    def set_run_lumi_event(self,run,lumi,event):
        self.results['run'][0] = run
        self.results['lumi'][0] = lumi
        #self.results['event'][0] = event

    def set(self,var,val):
        if var not in self.results:
            logging.error('No variable "{0}" in tree'.format(var))
            return
        if callable(val):
            val(self.results[var])
        else:
            self.results[var][0] = val

    def fill(self):
        self.tree.Fill()

    def clone(self):
        self.tree.CloneTree()
    
    def write(self):
        self.tree.Write()

    def reset(self):
        for var in self.results:
            self.results[var][0] = 0

def process(events,**kwargs):
    maxEvents = kwargs.pop('maxEvents',-1)
    reportEvery = kwargs.pop('reportEvery',1000)

    tree = kwargs.pop('tree',None)

    #==================================
    # Load Collections ////////////////
    #==================================

    collections = Collections()

    collections.add("generatorInfo", "GenEventInfoProduct", "generator")
    collections.add("genParticles", "std::vector<reco::GenParticle>", "prunedGenParticles")
    collections.add("jets", "std::vector<pat::Jet>", "slimmedJets")
    collections.add("jetsAK8", "std::vector<pat::Jet>", "slimmedJetsAK8")
    collections.add("primaryVertices", "std::vector<reco::Vertex>", "offlineSlimmedPrimaryVertices")

    numEvents = events.size()
    if maxEvents>=0: numEvents = min(numEvents,maxEvents)
    for i,event in enumerate(events):
        if maxEvents>=0 and i>=maxEvents: break
        if i%reportEvery==0: print 'Processing event {0}/{1}'.format(i+1,numEvents)

        tree.reset()       
 
        #=================================
        # Event Variables ////////////////
        #=================================
        aux = event.eventAuxiliary()
        run, lumi, evt = aux.run(), aux.luminosityBlock(), aux.event()
        evtkey = (run,lumi,evt)
        #print ':'.join([str(x) for x in [run,lumi,evt]])
        #print ''

        tree.set_run_lumi_event(run,lumi,event)

        #================================
        # Event Weights /////////////////
        #================================
        genInfo = collections.get('generatorInfo', event)

        tree.set('EventWeight', genInfo.weight() ) 

        #================================
        # Vertices //////////////////////
        #================================
        vertices = collections.get('primaryVertices', event)

        tree.set('nPrimaryVertices', len(vertices) )

        #================================
        # Gen Particles /////////////////
        #================================

        genParts = collections.get('genParticles')

        #================================
        # Jets //////////////////////////
        #================================
        jets = collections.get('jets', event)

        if len(jets) > 0:
            jetLead = jets[0]
            jetSublead = jets[0]
            for ijet,jet in enumerate(jets):
    
                if len(jets) > 1:
                    for jjet,jet in enumerate(jets):
                        if jets[jjet].pt() > jets[ijet].pt(): jetLead = jets[jjet]
                        if jetLead.pt() > jets[jjet].pt() >= jets[ijet].pt(): jetSublead = jets[jjet]
                    tree.set('LeadJet_pt', jetLead.pt() )
                    tree.set('LeadJet_eta', jetLead.eta() ) 
                    tree.set('LeadJet_mass', jetLead.mass() )
                    tree.set('LeadJet_phi', jetLead.phi() )
                    tree.set('SubLeadJet_pt', jetSublead.pt() )
                    tree.set('SubLeadJet_eta', jetSublead.eta() ) 
                    tree.set('SubLeadJet_mass', jetSublead.mass() )
                    tree.set('SubLeadJet_phi', jetSublead.phi() )
    
        #=================================
        # JetsAK8 ////////////////////////
        #=================================
        jetsAK8 = collections.get('jetsAK8', event)

        tree.set('nJetsAK8', len(jetsAK8) )

        if len(jetsAK8) > 0:
            jetAK8Lead = jetsAK8[0]
            jetAK8Sublead = jetsAK8[0]
            for ijet,jet in enumerate(jetsAK8):
             
                if len(jetsAK8) > 1:
                    for jjet,jet in enumerate(jetsAK8):
                        if jetsAK8[jjet].pt() > jetsAK8[ijet].pt(): jetAK8Lead = jetsAK8[jjet]
                        if jetAK8Lead.pt() > jetsAK8[jjet].pt() >= jetsAK8[ijet].pt(): jetAK8Sublead = jetsAK8[jjet]
                    tree.set('LeadAK8Jet_pt', jetAK8Lead.pt() )
                    tree.set('LeadAK8Jet_eta', jetAK8Lead.eta() ) 
                    tree.set('LeadAK8Jet_mass', jetAK8Lead.mass() )
                    #tree.set('LeadAK8Jet_softdrop_mass', jetAK8Lead.userFloat("ak8PFJetsCHSSoftDropMass") )
                    tree.set('LeadAK8Jet_phi', jetAK8Lead.phi() )
                    tree.set('SubLeadAK8Jet_pt', jetAK8Sublead.pt() )
                    tree.set('SubLeadAK8Jet_eta', jetAK8Sublead.eta() ) 
                    tree.set('SubLeadAK8Jet_mass', jetAK8Sublead.mass() )
                    #tree.set('SubLeadAK8Jet_softdrop_mass', jetAK8Sublead.userFloat("ak8PFJetsCHSSoftDropMass") )
                    tree.set('SubLeadAK8Jet_phi', jetAK8Sublead.phi() )

                    if len(jetsAK8) < 3: 
                        tree.set('Jet3AK8_pt', -999.9 )
                        tree.set('Jet3AK8_eta', -999.9 ) 
                        tree.set('Jet3AK8_mass', -999.9 )
                        tree.set('Jet3AK8_phi', -999.9 )
                    else:
                        tree.set('Jet3AK8_pt', jetsAK8[2].pt() )
                        tree.set('Jet3AK8_eta', jetsAK8[2].eta() ) 
                        tree.set('Jet3AK8_mass', jetsAK8[2].mass() )
                        tree.set('Jet3AK8_phi', jetsAK8[2].phi() )
                    if len(jetsAK8) < 4: 
                        tree.set('Jet4AK8_pt', -999.9 )
                        tree.set('Jet4AK8_eta', -999.9 ) 
                        tree.set('Jet4AK8_mass', -999.9 )
                        tree.set('Jet4AK8_phi', -999.9 )
                    else:
                        tree.set('Jet4AK8_pt', jetsAK8[3].pt() )
                        tree.set('Jet4AK8_eta', jetsAK8[3].eta() ) 
                        tree.set('Jet4AK8_mass', jetsAK8[3].mass() )
                        tree.set('Jet4AK8_phi', jetsAK8[3].phi() )
                    if len(jetsAK8) < 5: 
                        tree.set('Jet5AK8_pt', -999.9 )
                        tree.set('Jet5AK8_eta', -999.9 ) 
                        tree.set('Jet5AK8_mass', -999.9 )
                        tree.set('Jet5AK8_phi', -999.9 )
                    else:
                        tree.set('Jet5AK8_pt', jetsAK8[4].pt() )
                        tree.set('Jet5AK8_eta', jetsAK8[4].eta() ) 
                        tree.set('Jet5AK8_mass', jetsAK8[4].mass() )
                        tree.set('Jet5AK8_phi', jetsAK8[4].phi() )
                    if len(jetsAK8) < 6: 
                        tree.set('Jet6AK8_pt', -999.9 )
                        tree.set('Jet6AK8_eta', -999.9 ) 
                        tree.set('Jet6AK8_mass', -999.9 )
                        tree.set('Jet6AK8_phi', -999.9 )
                    else:
                        tree.set('Jet6AK8_pt', jetsAK8[5].pt() )
                        tree.set('Jet6AK8_eta', jetsAK8[5].eta() ) 
                        tree.set('Jet6AK8_mass', jetsAK8[5].mass() )
                        tree.set('Jet6AK8_phi', jetsAK8[5].phi() )
    
        #==================================
        # Fill Tree ///////////////////////
        #==================================
        tree.fill() 
       

#redirector = 'root://cms-xrd-global.cern.ch'
#redirector = 'root://cmsxrootd.fnal.gov'

#files = glob.glob("/afs/cern.ch/work/b/bregnery/public/HHwwwwMCgenerator/CMSSW_8_0_21/src/hhMCgenerator/RootFiles/M2000/*.root") 
#files = ["NLO_VLQ_custom_MiniAOD.root"]
#files = open('NLO_files.txt').read().splitlines()
#files = open('LO_files.txt').read().splitlines()
#files = ["root://xrootd-cms.infn.it//store/mc/RunIIFall17MiniAODv2/TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/100000/187E05CB-55AE-E811-9F64-008CFA1112C0.root"]
files = ["root://cmsxrootd.fnal.gov//store/mc/RunIISummer16MiniAODv3/TprimeTprime_M-1000_TuneCUETP8M1_13TeV-madgraph-pythia8/MINIAODSIM/PUMoriond17_94X_mcRun2_asymptotic_v3-v2/60000/060D21D7-2D36-E911-B490-0CC47AFF01B0.root"]

#[
#    '../RootFiles/M3500/Radion_hh_wwww_M3500_MiniAOD_1.root',
#]

#outFile = root.TFile("NLO_VLQ_custom_FWLite.root",'RECREATE')
#outFile = root.TFile("LO_VLQ_custom_FWLite.root",'RECREATE')
outFile = root.TFile("LO_preUL_FWLite.root",'RECREATE')
outFile.cd()

tree = AnalysisTree()
tree.add('LeadJet_pt', 'F')
tree.add('LeadJet_eta', 'F')
tree.add('LeadJet_mass', 'F')
tree.add('LeadJet_phi', 'F')
tree.add('SubLeadJet_pt', 'F')
tree.add('SubLeadJet_eta', 'F')
tree.add('SubLeadJet_phi', 'F')
tree.add('SubLeadJet_mass', 'F')
tree.add('LeadAK8Jet_pt', 'F')
tree.add('LeadAK8Jet_eta', 'F')
tree.add('LeadAK8Jet_mass', 'F')
tree.add('LeadAK8Jet_softdrop_mass', 'F')
tree.add('LeadAK8Jet_phi', 'F')
tree.add('SubLeadAK8Jet_pt', 'F')
tree.add('SubLeadAK8Jet_eta', 'F')
tree.add('SubLeadAK8Jet_mass', 'F')
tree.add('SubLeadAK8Jet_softdrop_mass', 'F')
tree.add('SubLeadAK8Jet_phi', 'F')
tree.add('nJetsAK8', 'F')
tree.add('nPrimaryVertices', 'F')
tree.add('EventWeight', 'F')

tree.add('Jet3AK8_pt', 'F')
tree.add('Jet3AK8_eta', 'F')
tree.add('Jet3AK8_mass', 'F')
tree.add('Jet3AK8_phi', 'F')
   
tree.add('Jet4AK8_pt', 'F')
tree.add('Jet4AK8_eta', 'F')
tree.add('Jet4AK8_mass', 'F')
tree.add('Jet4AK8_phi', 'F')
   
tree.add('Jet5AK8_pt', 'F')
tree.add('Jet5AK8_eta', 'F')
tree.add('Jet5AK8_mass', 'F')
tree.add('Jet5AK8_phi', 'F')
   
tree.add('Jet6AK8_pt', 'F')
tree.add('Jet6AK8_eta', 'F')
tree.add('Jet6AK8_mass', 'F')
tree.add('Jet6AK8_phi', 'F')
   
events = Events(files)
process(events,maxEvents=100000,tree=tree)
    
outFile.Write()
outFile.Close()
