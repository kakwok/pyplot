from ROOT import *
from hPlus import *
from style import *
from util import *
import glob

#global variables
flistOfDict= []
Pages      = []
legend     = TLegend(0.5,0.7,0.9,0.9, "", "brNDC")

#f1 = path to filename,  labelname = label for histograms from this file
flistOfDict.append({'fname':f1,'hname':"labelname"})
#Make Pages (get from files)
for i in range(2,12):
    page  = getHlistFromFiles(flistOfDict,"ST/stExc%02iHist"%i,"ST/GeV","N")
    Pages.append({'Title':"ST(N=%s)"%i,"list":page,"legend":legend})

c1 = TCanvas("c1","c1",800,600)
gStyle.SetOptStat(0)
c1.SetLogy(1)

makepdf(Pages, "test.pdf")
