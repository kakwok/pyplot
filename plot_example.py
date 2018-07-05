from ROOT import *
from hPlus import *
from style import *
from util import *
import glob,tdrstyle

gROOT.SetBatch()
tdrstyle.setTDRStyle()
#global variables
flistOfDict= []
Pages      = []
legend     = TLegend(0.5,0.7,0.9,0.9, "", "brNDC")

#f1 = path to filename,  labelname = label for histograms from this file
flistOfDict.append({'fname':f1,'hname':"labelname"})

#Setting options:: xlow,xup, ylow,yup , logy, drawOpt
Setting ={"xlow":0}

#Make Pages (get from files)
for i in range(2,12):
    page  = getHlistFromFiles(flistOfDict,"ST/stExc%02iHist"%i,"ST/GeV","N")
    Pages.append({'Title':"ST(N=%s)"%i,"list":page,"legend":legend,"Setting":Setting})
#Make a page from same file, different histograms
histos = [
    {'hLabel':"Jets in N=%i events, abs(#eta)>3.0, E_{T}>%s","hname":"Jets/Jet_ST_ISR_Exc03"},
    {'hLabel':"Jets in N=%i events, dRmin <1.0, E_{T}>%s"   ,"hname":"Jets/Jet_ST_FSR_Exc03"},
    {'hLabel':"Jets in N=%i events, E_{T}>%s"               ,"hname":"ST/stExc03Hist"       }
]
page  = getHlistFromNames(f['fname'],histos,"ST[GeV]","Fraction of entries")
selfnormalize(page,2000,7000)
Pages.append({'Title':"IsoJet,ST>2TeV,(N=%s)"%i,"list":page,"legend":legend,"Setting":Setting})

c1 = TCanvas("c1","c1",800,600)
gStyle.SetOptStat(0)
c1.SetLogy(1)

makepdf(Pages, "test.pdf")
