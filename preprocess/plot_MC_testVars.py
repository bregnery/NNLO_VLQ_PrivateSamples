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

NLOcomparison = True

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
           "nPrimaryVertices"]

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
weightNLO = 1/float(len(NLOlist[0]))
weightLO  = 1/float(len(LOlist[0]))

# Set style options
settings.setSimpleStyle()

# Stat Box options
root.gStyle.SetOptStat(0)

# make root histogram variables
NLOhistVec = []

NLOhistVec.append(root.TH1F("NLOnJetsHist","# of AK8 Jets",8,0,8) )
settings.setHistTitles(NLOhistVec[0], "Number of Jets", "Number of Events")

iVec = 1

for ijet in range(1, 6) :
    
    strJet = str(ijet)

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"ptHist","Jet "+strJet+" pT",20,0,1200) )
    settings.setHistTitles(NLOhistVec[iVec], "Jet p_{T} [GeV]", "Number of Events")

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"massHist","Jet "+strJet+" Mass",20,0,400) )
    settings.setHistTitles(NLOhistVec[iVec], "Jet Mass [GeV]", "Number of Events")

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"etaHist","Jet "+strJet+" Eta",20,0,4) )
    settings.setHistTitles(NLOhistVec[iVec], "Eta", "Number of Events")

    NLOhistVec.append(root.TH1F("NLOjet"+strJet+"phiHist","Leading Jet Phi",20,-4,4) )
    settings.setHistTitles(NLOhistVec[iVec], "Phi", "Number of Events")

NLOhistVec.append(root.TH1F("NLOnVertHist","# of Primary Vertices",50,0,50) )
settings.setHistTitles(NLOhistVec[9], "Number of Primary Vertices", "Number of Events")

NLOhistVec.append(root.TH1F("NLOjet1massZoomHist","Leading Jet Mass",50,150,300) )
settings.setHistTitles(NLOhistVec[10], "Jet Mass [GeV]", "Number of Events")

LOhistVec = []

LOhistVec.append(root.TH1F("LOnJetsHist","# of AK8 Jets",8,0,8) )
settings.setHistTitles(LOhistVec[0], "Number of Jets", "Number of Events")

LOhistVec.append(root.TH1F("LOjet1ptHist","Leading Jet pT",20,0,1200) )
settings.setHistTitles(LOhistVec[1], "Jet p_{T} [GeV]", "Number of Events")

LOhistVec.append(root.TH1F("LOjet1massHist","Leading Jet Mass",20,0,400) )
settings.setHistTitles(LOhistVec[2], "Jet Mass [GeV]", "Number of Events")

LOhistVec.append(root.TH1F("LOjet1etaHist","Leading Jet Eta",20,0,4) )
settings.setHistTitles(LOhistVec[3], "Eta", "Number of Events")

LOhistVec.append(root.TH1F("LOjet1phiHist","Leading Jet Phi",20,-4,4) )
settings.setHistTitles(LOhistVec[4], "Phi", "Number of Events")

LOhistVec.append(root.TH1F("LOjet2ptHist","SubLeading Jet pT",20,0,1200) )
settings.setHistTitles(LOhistVec[5], "Jet p_{T} [GeV]", "Number of Events")

LOhistVec.append(root.TH1F("LOjet2massHist","SubLeading Jet Mass",20,0,400) )
settings.setHistTitles(LOhistVec[6], "Jet Mass [GeV]", "Number of Events")

LOhistVec.append(root.TH1F("LOjet2etaHist","SubLeading Jet Eta",20,0,4) )
settings.setHistTitles(LOhistVec[7], "Eta", "Number of Events")

LOhistVec.append(root.TH1F("LOjet2phiHist","SubLeading Jet Phi",20,-4,4) )
settings.setHistTitles(LOhistVec[8], "Phi", "Number of Events")

LOhistVec.append(root.TH1F("LOnVertHist","# of Primary Vertices",50,0,50) )
settings.setHistTitles(LOhistVec[9], "Number of Primary Vertices", "Number of Events")

LOhistVec.append(root.TH1F("LOjet1massZoomHist","Leading Jet Mass",50,150,300) )
settings.setHistTitles(LOhistVec[10], "Jet Mass [GeV]", "Number of Events")

# fill the histograms
for event in range(len(NLOlist[0]) ):
    for i in range(len(varList) ) :
        NLOhistVec[i].Fill(NLOlist[i][event], weightNLO)
        if "LeadAK8Jet_mass" in varList[i] :
            NLOhistVec[10].Fill(NLOlist[i][event], weightNLO)

#Weighting the LO Histograms 
for event in range(len(LOlist[0]) ):
    for i in range(len(varList) ) :
        LOhistVec[i].Fill(LOlist[i][event], weightLO)
        if "LeadAK8Jet_mass" in varList[i] :
            LOhistVec[10].Fill(LOlist[i][event], weightLO)

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
