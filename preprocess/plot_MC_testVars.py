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

# read data from file into a numpy array
NLOjet1pt = root_numpy.root2array("NLO_VLQ_custom_FWLite.root","AnalysisTree","LeadAK8Jet_pt")
NLOjet1mass = root_numpy.root2array("NLO_VLQ_custom_FWLite.root","AnalysisTree","LeadAK8Jet_mass")
NLOnjets = root_numpy.root2array("NLO_VLQ_custom_FWLite.root","AnalysisTree","nJetsAK8")

LOjet1pt = root_numpy.root2array("LO_VLQ_custom_FWLite.root","AnalysisTree","LeadAK8Jet_pt")
LOjet1mass = root_numpy.root2array("LO_VLQ_custom_FWLite.root","AnalysisTree","LeadAK8Jet_mass")
LOnjets = root_numpy.root2array("LO_VLQ_custom_FWLite.root","AnalysisTree","nJetsAK8")

#==================================================================================
# Make Histograms /////////////////////////////////////////////////////////////////
#==================================================================================

# Set style options
settings.setSimpleStyle()

# Stat Box options
root.gStyle.SetOptStat(0)

# make root histogram variables
NLOnJetsHist = root.TH1F("NLOnJetsHist","# of AK8 Jets",8,0,8)
settings.setHistTitles(NLOnJetsHist, "Number of Jets", "Number of Events")

NLOjet1ptHist = root.TH1F("NLOjet1ptHist","Leading Jet pT",20,0,1200)
settings.setHistTitles(NLOjet1ptHist, "Jet p_{T} [GeV]", "Number of Events")

NLOjet1massHist = root.TH1F("NLOjet1massHist","Leading Jet Mass",20,0,400)
settings.setHistTitles(NLOjet1massHist, "Jet Mass [GeV]", "Number of Events")

LOnJetsHist = root.TH1F("LOnJetsHist","# of AK8 Jets",8,0,8)
settings.setHistTitles(LOnJetsHist, "Number of Jets", "Number of Events")

LOjet1ptHist = root.TH1F("LOjet1ptHist","Leading Jet pT",20,0,1200)
settings.setHistTitles(LOjet1ptHist, "Jet p_{T} [GeV]", "Number of Events")

LOjet1massHist = root.TH1F("LOjet1massHist","Leading Jet Mass",20,0,400)
settings.setHistTitles(LOjet1massHist, "Jet Mass [GeV]", "Number of Events")

# fill the histograms
for event in range(len(NLOnjets) ):
    NLOnJetsHist.Fill(NLOnjets[event])
    NLOjet1ptHist.Fill(NLOjet1pt[event])
    NLOjet1massHist.Fill(NLOjet1mass[event])

for event in range(len(LOnjets) ):
    LOnJetsHist.Fill(LOnjets[event])
    LOjet1ptHist.Fill(LOjet1pt[event])
    LOjet1massHist.Fill(LOjet1mass[event])

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

# put the histograms into a vector
NLOhistVec = []
NLOhistVec.append(NLOnJetsHist)
NLOhistVec.append(NLOjet1ptHist)
NLOhistVec.append(NLOjet1massHist)

LOhistVec = []
LOhistVec.append(LOnJetsHist)
LOhistVec.append(LOjet1ptHist)
LOhistVec.append(LOjet1massHist)

# adjust histogram settings
canvas = root.TCanvas()
for ihist in range(len(NLOhistVec) ):
   settings.setFillOptions(NLOhistVec[ihist], root.kBlue, 1, 2, 1)
   settings.setFillOptions(LOhistVec[ihist], root.kRed, 1, 4, 0)
   settings.makeComparisonHist(canvas, NLOhistVec[ihist],  LOhistVec[ihist], "NLO New Model", "LO Old Model", NLOhistVec[ihist].GetXaxis().GetTitle(), "(hist1 - hist2)/ hist1", "hist same", root.kBlue)

# draw and save the histograms
#settings.drawHist(histVec, True, False)

# make a TCanvas and draw the histograms
#canvas = root.TCanvas()
#nctPhotonFullHist.Draw("P")

# make a TCanvas and a histogram plot with residuals

# Save the Plots
#canvas.SaveAs("Hist_nctPhotonFull.png")
