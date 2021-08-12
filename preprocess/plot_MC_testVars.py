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
jet1pt = root_numpy.root2array("NLO_VLQ_custom_FWLite.root","AnalysisTree","LeadAK8Jet_pt")
jet1mass = root_numpy.root2array("NLO_VLQ_custom_FWLite.root","AnalysisTree","LeadAK8Jet_mass")
njets = root_numpy.root2array("NLO_VLQ_custom_FWLite.root","AnalysisTree","nJetsAK8")

#==================================================================================
# Make Histograms /////////////////////////////////////////////////////////////////
#==================================================================================

# Set style options
settings.setSimpleStyle()

# Stat Box options
root.gStyle.SetOptStat(0)

# make root histogram variables
nJetsHist = root.TH1F("nJetsHist","# of AK8 Jets",8,0,8)
settings.setHistTitles(nJetsHist, "Number of Jets", "Number of Events")

jet1ptHist = root.TH1F("jet1ptHist","Leading Jet pT",20,0,1200)
settings.setHistTitles(jet1ptHist, "Jet p_{T} [GeV]", "Number of Events")

jet1massHist = root.TH1F("jet1massHist","Leading Jet Mass",20,0,400)
settings.setHistTitles(jet1ptHist, "Jet Mass [GeV]", "Number of Events")

# fill the histograms
for event in range(len(njets) ):
    nJetsHist.Fill(njets[event])
    jet1ptHist.Fill(jet1pt[event])
    jet1massHist.Fill(jet1mass[event])

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
histVec = []
histVec.append([nJetsHist, "hist"])
histVec.append([jet1ptHist, "hist"])
histVec.append([jet1massHist, "hist"])

# adjust histogram settings
for ihist in range(len(histVec) ):
   settings.setFillOptions(histVec[ihist][0], root.kBlue, 1, 2, 1)

# draw and save the histograms
settings.drawHist(histVec, True, False)

# make a TCanvas and draw the histograms
#canvas = root.TCanvas()
#nctPhotonFullHist.Draw("P")

# make a TCanvas and a histogram plot with residuals

# Save the Plots
#canvas.SaveAs("Hist_nctPhotonFull.png")
