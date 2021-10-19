#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ExamplePlots.py /////////////////////////////////////////////////////////////////
#==================================================================================
# This program reads data from a file and makes histograms ////////////////////////
#==================================================================================

# Give interpreter a search path

# modules
import ROOT as root
import numpy
import root_numpy

# import modules from other directories
import style.histogramsettings as settings

# enter batch mode in root (so python can access displays)
root.gROOT.SetBatch(True)

#==================================================================================
# Load Data ///////////////////////////////////////////////////////////////////////
#==================================================================================

NLOcomparison = False

if NLOcomparison == True: 
    NLOfile = "NLO_VLQ_custom_FWLite.root"
    LOfile  = "LO_VLQ_custom_FWLite.root"
    NLOlabel = "NLO New Model"
    LOlabel = "LO Old Model UL"

if NLOcomparison == False: 
    NLOfile  = "LO_VLQ_custom_FWLite.root"
    LOfile = "LO_preUL_FWLite.root"
    NLOlabel = "LO Old Model UL"
    LOlabel = "LO Pre UL"

varList = ["nJetsAK8", "LeadAK8Jet_pt", "LeadAK8Jet_mass", "LeadAK8Jet_eta", "LeadAK8Jet_phi",
           "SubLeadAK8Jet_pt", "SubLeadAK8Jet_mass", "SubLeadAK8Jet_eta", "SubLeadAK8Jet_phi",
           "Jet3AK8_pt", "Jet3AK8_mass", "Jet3AK8_eta", "Jet3AK8_phi",
           "Jet4AK8_pt", "Jet4AK8_mass", "Jet4AK8_eta", "Jet4AK8_phi",
           "Jet5AK8_pt", "Jet5AK8_mass", "Jet5AK8_eta", "Jet5AK8_phi",
           "Jet6AK8_pt", "Jet6AK8_mass", "Jet6AK8_eta", "Jet6AK8_phi",
           "nPrimaryVertices", "EventWeight"]

# read data from file into a numpy array
LOlist  = []
NLOlist = []
for var in varList :
    NLOlist.append(root_numpy.root2array(NLOfile,"AnalysisTree",var) )
    LOlist.append(root_numpy.root2array(LOfile,"AnalysisTree", var) )

#==================================================================================
# Make Histograms /////////////////////////////////////////////////////////////////
#==================================================================================

# Create weight for the LO histograms so that Histograms have the same scale
#weight = len(NLOnjets)/float(len(LOnjets))
#weightNLO = 1/float(len(NLOlist[0]))
#weightLO  = 1/float(len(LOlist[0]))

# Set style options
settings.setSimpleStyle()

# Stat Box options
root.gStyle.SetOptStat(0)

# make root histogram variables
NLOhistVec = []

NLOhistVec.append(root.TH1F("NLOnJetsHist","# of AK8 Jets",8,0,8) )
settings.setHistTitles(NLOhistVec[0], "Number of Jets", "Number of Events")

iVec = 1

for ijet in range(1, 7) :
    
    strJet = str(ijet)

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"ptHist","Jet "+strJet+" pT",20,0,1200) )
    settings.setHistTitles(NLOhistVec[iVec], "Jet p_{T} [GeV]", "Number of Events")

    iVec+=1

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"massHist","Jet "+strJet+" Mass",20,0,400) )
    settings.setHistTitles(NLOhistVec[iVec], "Jet Mass [GeV]", "Number of Events")

    iVec+=1

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"etaHist","Jet "+strJet+" Eta",20,0,4) )
    settings.setHistTitles(NLOhistVec[iVec], "Eta", "Number of Events")

    iVec+=1

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"phiHist","Jet "+strJet+" Phi",20,-4,4) )
    settings.setHistTitles(NLOhistVec[iVec], "Phi", "Number of Events")

    iVec+=1

NLOhistVec.append(root.TH1F("NLOnVertHist","# of Primary Vertices",50,0,50) )
settings.setHistTitles(NLOhistVec[iVec], "Number of Primary Vertices", "Number of Events")

iVec+=1

NLOhistVec.append(root.TH1F("NLOeventWeigth","Event Weight",100,-1.2,1.2) )
settings.setHistTitles(NLOhistVec[iVec], "EventWeight", "Number of Events")

iVec+=1

NLOhistVec.append(root.TH1F("NLOjetHTHist","HT",30,0,2500) )
settings.setHistTitles(NLOhistVec[iVec], "HT", "Number of Events")

iVec+=1

NLOhistVec.append(root.TH1F("NLOjet1massZoomHist","Leading Jet Mass",50,150,300) )
settings.setHistTitles(NLOhistVec[iVec], "Jet Mass [GeV]", "Number of Events")

LOhistVec = []

LOhistVec.append(root.TH1F("LOnJetsHist","# of AK8 Jets",8,0,8) )
settings.setHistTitles(LOhistVec[0], "Number of Jets", "Number of Events")

iVec = 1

for ijet in range(1, 7) :
    
    strJet = str(ijet)

    LOhistVec.append(root.TH1F("LOjet"+strJet+"ptHist","Jet "+strJet+" pT",20,0,1200) )
    settings.setHistTitles(LOhistVec[iVec], "Jet p_{T} [GeV]", "Number of Events")

    iVec+=1

    LOhistVec.append(root.TH1F("LOjet"+strJet+"massHist","Jet "+strJet+" Mass",20,0,400) )
    settings.setHistTitles(LOhistVec[iVec], "Jet Mass [GeV]", "Number of Events")

    iVec+=1

    LOhistVec.append(root.TH1F("LOjet"+strJet+"etaHist","Jet "+strJet+" Eta",20,0,4) )
    settings.setHistTitles(LOhistVec[iVec], "Eta", "Number of Events")

    iVec+=1

    LOhistVec.append(root.TH1F("LOjet"+strJet+"phiHist","Jet "+strJet+" Phi",20,-4,4) )
    settings.setHistTitles(LOhistVec[iVec], "Phi", "Number of Events")

    iVec+=1

LOhistVec.append(root.TH1F("LOnVertHist","# of Primary Vertices",50,0,50) )
settings.setHistTitles(LOhistVec[iVec], "Number of Primary Vertices", "Number of Events")

iVec+=1

LOhistVec.append(root.TH1F("LOeventWeigth","Event Weight",100,-1.2,1.2) )
settings.setHistTitles(LOhistVec[iVec], "EventWeight", "Number of Events")

iVec+=1

LOhistVec.append(root.TH1F("LOjetHTHist","HT",30,0,2500) )
settings.setHistTitles(LOhistVec[iVec], "HT", "Number of Events")

iVec+=1

LOhistVec.append(root.TH1F("LOjet1massZoomHist","Leading Jet Mass",50,150,300) )
settings.setHistTitles(LOhistVec[iVec], "Jet Mass [GeV]", "Number of Events")

# fill the histograms
eventWeightNLO = root_numpy.root2array(NLOfile,"AnalysisTree","EventWeight") 
TotWeightNLO=0.0
for event in range(len(NLOlist[0]) ):
    TotWeightNLO += eventWeightNLO[event]
weightNLO = 1/TotWeightNLO

eventWeightLO = root_numpy.root2array(LOfile,"AnalysisTree","EventWeight") 
TotWeightLO=0.0
for event in range(len(LOlist[0]) ):
    TotWeightLO += eventWeightLO[event]
weightLO = 1/float(TotWeightLO)

for event in range(len(NLOlist[0]) ):
    jetHT = 0.0
    for i in range(len(varList) ) :
        weight = eventWeightNLO[event] * weightNLO
        NLOhistVec[i].Fill(NLOlist[i][event], weight)
        if "LeadAK8Jet_mass" in varList[i] :
            NLOhistVec[iVec].Fill(NLOlist[i][event], weight)

        if "pt" in varList[i] :
            if NLOlist[i][event] > 0.0: 
                jetHT += NLOlist[i][event]
        if "Jet6AK8_pt" in varList[i] :
            NLOhistVec[iVec-1].Fill(jetHT, weight)

#Weighting the LO Histograms 
for event in range(len(LOlist[0]) ):
    jetHT = 0.0
    for i in range(len(varList) ) :
        weight = eventWeightLO[event] * weightLO
        LOhistVec[i].Fill(LOlist[i][event], weight)
        if "LeadAK8Jet_mass" in varList[i] :
            LOhistVec[iVec].Fill(LOlist[i][event], weight)

        if "pt" in varList[i] :
            if LOlist[i][event] > 0.0: 
                jetHT += LOlist[i][event]
        if "Jet6AK8_pt" in varList[i] :
            LOhistVec[iVec-1].Fill(jetHT, weight)


# adjust histogram settings
#settings.setDataPoint(nctPhotonFullHist, root.kBlack, root.kFullDotLarge)

#==================================================================================
# Fit the Histograms //////////////////////////////////////////////////////////////
#==================================================================================

# specify number of fit parameters

# fit with root

#==================================================================================
# Draw Plots //////////////////////////////////////////////////////////////////////
#==================================================================================

# adjust histogram settings
canvas = root.TCanvas()
for ihist in range(len(NLOhistVec) ):
   settings.setFillOptions(NLOhistVec[ihist], root.kBlue, 1, 2, 1)
   settings.setFillOptions(LOhistVec[ihist], root.kRed, 1, 4, 0)
   settings.makeComparisonHist(canvas, NLOhistVec[ihist],  LOhistVec[ihist], NLOlabel, LOlabel, NLOhistVec[ihist].GetXaxis().GetTitle(), "NLO/LO", "hist same", root.kBlue)

# draw and save the histograms
#settings.drawHist(histVec, True, False)

# make a TCanvas and draw the histograms
#canvas = root.TCanvas()
#nctPhotonFullHist.Draw("P")

# make a TCanvas and a histogram plot with residuals

# Save the Plots
#canvas.SaveAs("Hist_nctPhotonFull.png")
