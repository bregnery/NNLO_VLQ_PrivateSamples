#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# histogramsettings.py ////////////////////////////////////////////////////////////
#==================================================================================
# This module contains settings for histograms ////////////////////////////////////
#==================================================================================

# modules
import ROOT as root

#==================================================================================
# Make histograms with residuals //////////////////////////////////////////////////
#----------------------------------------------------------------------------------
# Axis titles are strings /////////////////////////////////////////////////////////
# residualColor options are: kColor ///////////////////////////////////////////////
# fitfunc is the fitted TF1 from a root fit ///////////////////////////////////////
# stats is for statsbox the options are here: /////////////////////////////////////
#   https://root.cern.ch/doc/master/classTPaveStats.html //////////////////////////
# draw options are here: https://root.cern.ch/doc/master/classTHistPainter.html ///
# residualYtitle is a string that has two options: "data - fit", //////////////////
#   "(data - fit)/ data" //////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------

def makeResidualHist(canvas, hist, xtitle, residualYtitle, stats, drawoption, residualColor, fitfunc):
   # make the TPads that will contain each graph 
   histopad = root.TPad("histopad", "histopad", 0.0, 0.33, 1.0, 1.0) # xlow, ylow, xup, yup
   residualpad = root.TPad("residualpad", "residualpad", 0.0, 0.0, 1.0, 0.33)

   # set margins for splitting canvas into two
   histopad.SetBottomMargin(0.02)
   histopad.SetTopMargin(0.12)
   residualpad.SetTopMargin(0.02)
   residualpad.SetBottomMargin(0.3)
   residualpad.SetBorderMode(0)

   # draw the histograms on the canvas
   histopad.Draw()
   residualpad.Draw()

   # Plot the data and fit results
   histopad.cd()
   hist.SetStats(stats)
   root.gStyle.SetTitleSize(0.08, "t") # moves title, not size, x title is default, need t for actual title
   #root.gStyle.SetTitleOffset(0.5, "t")
   root.gStyle.SetOptFit(1111)
   root.gStyle.SetErrorX(0.0001) # No X error
   hist.SetLabelSize(0.04)
   hist.GetXaxis().SetLabelSize(0)
   hist.Draw(drawoption)
   histopad.Modified() # to make statsbox object
   histopad.Update()
   if stats != 0: # if you do want to include a stats box
       statsbox = hist.FindObject("stats")
       statsbox.SetY2NDC(0.9)
       histopad.Modified() # to update statsbox location
       histopad.Update()
    
   # Settings for the residuals
   residualpad.cd()
   residualHist = root.TH1F("resiualHist","", hist.GetNbinsX(), 
                            hist.GetXaxis().GetXmin(), hist.GetXaxis().GetXmax() )
   residualHist.SetFillColor(residualColor-1)
   residualHist.SetLineColor(residualColor+1)
   residualHist.GetXaxis().SetTitle(xtitle)
   residualHist.GetXaxis().SetTitleSize(0.1)
   residualHist.GetXaxis().SetTitleOffset(1.0)
   residualHist.GetXaxis().SetLabelSize(0.09)
   residualHist.GetYaxis().SetTitle(residualYtitle)
   residualHist.GetYaxis().SetTitleSize(0.09)
   residualHist.GetYaxis().SetTitleOffset(0.7)
   residualHist.GetYaxis().SetLabelSize(0.08)

   # Fill the residuals
   if residualYtitle == "data - fit":
      for nbin in range(1, hist.GetNbinsX() ):
         residual = hist.GetBinContent(nbin) - fitfunc.Eval(hist.GetBinCenter(nbin) )
         residualHist.SetBinContent(nbin, residual)
   elif residualYtitle == "(data - fit)/ data":
      for nbin in range(1, hist.GetNbinsX() ):
         residual = (hist.GetBinContent(nbin) - fitfunc.Eval(hist.GetBinCenter(nbin) ) ) / hist.GetBinContent(nbin)
         residualHist.SetBinContent(nbin, residual)
   elif residualYtitle == "fewz - fit":
      for nbin in range(1, hist.GetNbinsX() ):
         residual = hist.GetBinContent(nbin) - fitfunc.Eval(hist.GetBinCenter(nbin) )
         residualHist.SetBinContent(nbin, residual)
   elif residualYtitle == "(fewz - fit)/ fewz":
      for nbin in range(1, hist.GetNbinsX() ):
         residual = (hist.GetBinContent(nbin) - fitfunc.Eval(hist.GetBinCenter(nbin) ) ) / hist.GetBinContent(nbin)
         residualHist.SetBinContent(nbin, residual)

   # Plot the residuals
   residualHist.SetStats(0)
   residualHist.Draw()
   residualpad.Modified()
   residualpad.Update()

   # save the plot
   canvas.cd()
   canvas.SaveAs("ResidualHist_" + hist.GetName() + ".png")
   canvas.SaveAs("ResidualHist_" + hist.GetName() + ".pdf")

   # delete the histograms and TPads to avoid memory leaks
   residualHist.Delete()
   residualpad.Delete()
   histopad.Delete()

#==================================================================================
# Draw the histogram on a canvas and save output //////////////////////////////////
#----------------------------------------------------------------------------------
# histVec is a 2D aray of histograms and draw options /////////////////////////////
#    ( [ [TH_1, drawOption1], [TH_2, drawOption2], ... ] ) ////////////////////////
# savePNG and savePDF are boolean variables ///////////////////////////////////////
#----------------------------------------------------------------------------------

def drawHist(histVec, savePNG, savePDF):

   # make canas
   canvas = root.TCanvas()

   for ihist in range(len(histVec) ):

      # draw histogram
      histVec[ihist][0].Draw(histVec[ihist][1])

      # remove hist part of histogram name
      name = histVec[ihist][0].GetName()
      if name.endswith("Hist") or name.endswith("hist"):
         name = name[:-4]

      # save histogram
      if savePNG == True :
         canvas.SaveAs("Hist_" + name + ".png")
      if savePDF == True :
         canvas.SaveAs("Hist_" + name + ".pdf")

      # clear the canvas
      canvas.Clear()
   

#==================================================================================
# Make stacked histograms /////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------
# Axis titles are strings /////////////////////////////////////////////////////////
# HistList is a List of TH1F //////////////////////////////////////////////////////
# residualColor options are: kColor ///////////////////////////////////////////////
# stats is for statsbox the options are here: /////////////////////////////////////
#   https://root.cern.ch/doc/master/classTPaveStats.html //////////////////////////
# draw options are here: https://root.cern.ch/doc/master/classTHistPainter.html ///
#----------------------------------------------------------------------------------

def makeStackHist(canvas, histList, title, xtitle, ytitle, drawoption, logY):

   # Make THStack variable
   stackHist = root.THStack("stackHist",title)

   # Add the histograms to the stack
   for i, hist in enumerate(histList):
       stackHist.Add(histList[i])

   # save the plot
   canvas.cd()
   stackHist.Draw(drawoption)
   stackHist.GetXaxis().SetTitle(xtitle)
   stackHist.GetYaxis().SetTitle(ytitle)
   canvas.Modified()
   if logY == 1: canvas.SetLogy() 
   canvas.SaveAs("StackHist_" + hist.GetName() + ".png")
   canvas.SaveAs("StackHist_" + hist.GetName() + ".pdf")

   # return the stacked histogram
   return stackHist

#==================================================================================
# Set the histogram axis titles ///////////////////////////////////////////////////
#----------------------------------------------------------------------------------
# Axis titles are strings /////////////////////////////////////////////////////////
#----------------------------------------------------------------------------------

def setHistTitles(hist, xtitle, ytitle):
   hist.GetXaxis().SetTitle(xtitle)
   hist.GetYaxis().SetTitle(ytitle)
   hist.Sumw2()

#==================================================================================
# Set the data point style and color //////////////////////////////////////////////
#----------------------------------------------------------------------------------
# Color options are: kColor ///////////////////////////////////////////////////////
# marker options are: kMarker /////////////////////////////////////////////////////
#----------------------------------------------------------------------------------

def setDataPoint(hist, color, marker):
   hist.SetMarkerStyle(marker)
   hist.SetMarkerColor(color)

#==================================================================================
# Set the line color, line style, line width, fill color and fill style ///////////
#----------------------------------------------------------------------------------
# Color options are: kColor ///////////////////////////////////////////////////////
# Line style options are integers 1-10 ////////////////////////////////////////////
# Line Width options are integers 1-10 ////////////////////////////////////////////
# Fill style options are: https://root.cern.ch/doc/master/classTAttFill.html //////
#----------------------------------------------------------------------------------

def setFillOptions(hist, color, lstyle, lwidth, fstyle):
   hist.SetFillColor(color-1)
   hist.SetLineColor(color+1)
   hist.SetLineStyle(lstyle)
   hist.SetLineWidth(lwidth)
   hist.SetFillStyle(fstyle)

#==================================================================================
# Set the style to a simple clean look ////////////////////////////////////////////
#----------------------------------------------------------------------------------

def setSimpleStyle():
   root.gStyle.SetCanvasColor(0)
   root.gStyle.SetCanvasBorderSize(10)
   root.gStyle.SetCanvasBorderMode(0)
   root.gStyle.SetCanvasDefH(700)
   root.gStyle.SetCanvasDefW(700)
 
   root.gStyle.SetPadColor       (0)
   root.gStyle.SetPadBorderSize  (10)
   root.gStyle.SetPadBorderMode  (0)
   root.gStyle.SetPadBottomMargin(0.13)
   root.gStyle.SetPadTopMargin   (0.08)
   root.gStyle.SetPadLeftMargin  (0.16)
   root.gStyle.SetPadRightMargin (0.05)
   root.gStyle.SetPadGridX       (0)
   root.gStyle.SetPadGridY       (0)
   root.gStyle.SetPadTickX       (1)
   root.gStyle.SetPadTickY       (1)
 
   root.gStyle.SetFrameFillStyle ( 0)
   root.gStyle.SetFrameFillColor ( 0)
   root.gStyle.SetFrameLineColor ( 1)
   root.gStyle.SetFrameLineStyle ( 0)
   root.gStyle.SetFrameLineWidth ( 1)
   root.gStyle.SetFrameBorderSize(10)
   root.gStyle.SetFrameBorderMode( 0)
 
   root.gStyle.SetNdivisions(505)
 
   root.gStyle.SetLineWidth(2)
   root.gStyle.SetHistLineWidth(2)
   root.gStyle.SetFrameLineWidth(2)
   root.gStyle.SetLegendFillColor(root.kWhite)
   root.gStyle.SetLegendFont(42)
   root.gStyle.SetMarkerSize(1.2)
   root.gStyle.SetMarkerStyle(20)
  
   root.gStyle.SetLabelSize(0.040,"X")
   root.gStyle.SetLabelSize(0.040,"Y")
 
   root.gStyle.SetLabelOffset(0.010,"X")
   root.gStyle.SetLabelOffset(0.010,"Y")
  
   root.gStyle.SetLabelFont(42,"X")
   root.gStyle.SetLabelFont(42,"Y")
  
   root.gStyle.SetTitleBorderSize(0)
   root.gStyle.SetTitleFont(42)
   root.gStyle.SetTitleFont(42,"X")
   root.gStyle.SetTitleFont(42,"Y")
 
   root.gStyle.SetTitleSize(0.045,"X")
   root.gStyle.SetTitleSize(0.045,"Y")
  
   root.gStyle.SetTitleOffset(1.4,"X")
   root.gStyle.SetTitleOffset(1.85,"Y")
  
   root.gStyle.SetTextSize(0.055)
   root.gStyle.SetTextFont(42)
