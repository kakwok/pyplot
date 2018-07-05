from ROOT import *
from hPlus import *
from style import *
import os,CMS_lumi

def DrawSameFromList(hTitle,hlist,legend,Setting=None):
    ymins = []
    ymaxs = []
    for h in hlist:
        h.setStyle()
        h.setLabel()
        ymins.append( h.getTH1().GetMinimum() )
        ymaxs.append( h.getTH1().GetMaximum() )
        legend.AddEntry(h.getTH1(),h.getTH1().GetName(),"l")
    hlist[0].getTH1().SetMaximum( max(ymaxs)*1.5 )
    if ((not Setting is None) and ("xlow" in Setting) and ("xup" in Setting)):
        hlist[0].getTH1().GetXaxis().SetRangeUser(Setting["xlow"],Setting["xup"]) 
    if (not min(ymins)==0): 
        hlist[0].getTH1().SetMinimum( min(ymins)*0.5 )
    elif (c1.GetLogy()):
        hlist[0].getTH1().SetMinimum( min(ymins)+1E-1 ) # if there are empty bins but we need log axis
    else:
        hlist[0].getTH1().SetMinimum( 0 )
 
    if ((not Setting is None) and ("ylow" in Setting)):
        hlist[0].getTH1().SetMinimum( Setting["ylow"] )
    if ((not Setting is None) and ("ylow" in Setting) and ("yup" in Setting)):
        hlist[0].getTH1().GetYaxis().SetRangeUser(Setting["ylow"],Setting["yup"]) 
    if ((not Setting is None) and ("logy" in Setting)):
        print "Setting logY to %s"%Setting["logy"]
        c1.SetLogy(Setting["logy"])
    #hlist[0].getTH1().GetYaxis().SetRangeUser(0,5) 
    hlist[0].getTH1().SetTitle(hTitle)
    hlist[0].getTH1().GetYaxis().SetTitleOffset(1.4)
    if (not Setting is None and "drawOpt" in Setting):
        hlist.pop(0).getTH1().Draw(Setting["drawOpt"]) 
    else:
        hlist.pop(0).getTH1().Draw("HIST")   # default drawOption
    for h in hlist:
        print h.getTH1().GetName(),h.getTH1().GetMean(1)
        if (not Setting is None and "drawOpt" in Setting):
            hlist.pop(0).getTH1().Draw(Setting["drawOpt"]+" same") 
        else:
            h.getTH1().Draw("Same HIST")     # default drawOption
    legend.SetTextFont(42)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.Draw()
    #c1.BuildLegend(0.7,0.7,0.9,0.9)
    
# Loop through a list of hPlus, print it into a pdf file
# histo_Dict:
# key hname, value list of hPlus objects from flist with name hTitle
# outputFolder: if set to a path, print each page as separate pdf.
def makepdf(pages,outputFile,outputFolder=None):
    nItems = len(pages)
    i      = 1
    nPad   = 1
    nPages = 0
    IsLast = False
    for page in pages:
                # Prepare the canvas
        if (not "Setting" in page):
           DrawSameFromList(page["Title"],page["list"],page["legend"])
        else:
           DrawSameFromList(page["Title"],page["list"],page["legend"],page["Setting"])
        iPeriod=0
        iPos = 11
        CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
        c1.cd()
        c1.Update()
        # Open a new page
        if(outputFolder==None):
            #Print all pages into same pdf
            if(nPages==0): 
                if(int(nItems/nPad)==1):
                    c1.Print(outputFile,"pdf")
                else:
                    c1.Print(outputFile+"(","pdf")
            if(i == nItems):
                c1.Print(outputFile+")","pdf")
                IsLast = True
            else:
                if(nPages!=0 and IsLast==False):
                     c1.Print(outputFile,"pdf")
        else:
            if not (os.path.exists(outputFolder)):     os.system("mkdir %s"%outputFolder)
            c1.Print(outputFolder+outputFile.replace(".pdf","")+"_"+page["Title"]+".pdf")
            #c1.Print(outputFolder+outputFile.replace(".pdf","")+"_"+str(nPages)+".pdf")
        nPages+=1
        i+=1
        nPad = 1
        c1.Clear()
        page["legend"].Clear()
    #print IsLast
    if(IsLast==False): 
        c1.Print(outputFile+")","pdf")

# For drawing same histogram from different TFile

# return the class name given a list of keys in ROOT file
def getClassName(keys,hKey):
    foundKey=False
    className=""
    for key in keys:
        if key.GetName()==hKey: 
            #print key.GetName(),hKey,key.GetClassName()
            className = key.GetClassName()
            foundKey=True
            continue
    return className

# input: List of dicts{fname,hname}, hKey
# fname   = name of file,   hname = name of histo label
# hKey    = historgram name in each files
# setting = a dict with : {"xlow","xup","isLogY","i_style"} 
def getHlistFromFiles(flist,hKey,xLabel,yLabel,style_init=0):
    hlist =[]
    #istyle=setting['i_style']
    istyle=style_init
    for f in flist:
        rootfile = TFile(f['fname'])
        #rootfile.ls()
        keys  =  rootfile.GetListOfKeys()
        className = getClassName(keys,hKey)
        if ("TProfile" in className):
            hist      = rootfile.Get(hKey).ProjectionX()
        else:
            hist      = rootfile.Get(hKey)
        hist.SetDirectory(0)
        label    = {'Name':f['hname'],'x':xLabel,'y':yLabel}
        hlist.append(hPlus(hist,style(istyle),label))
        istyle= istyle+1
    return hlist

# For drawing N different histogram in same file
# hKeys = list of hDict
# hDict = {hName,hLabel}
# hName = Name of histogram,   hLabel = Label for that histogram
# returns list of hPlus
def getHlistFromNames(tFile,hKeys,xLabel,yLabel,style_init=0):
    hlist = []
    rootfile = TFile(tFile)
    istyle=style_init
    for hDict in hKeys:
        hist  = rootfile.Get(hDict['hname'])
        # Default to use histogram name as label
        if (hDict['hLabel']=="default"):
            legName = hist.GetName()
        else:
            legName = hDict['hLabel']
        hist.SetDirectory(0)
        label =  {'Name':legName,"x":xLabel,"y":yLabel}
        hlist.append(hPlus(hist,style(istyle),label))
        istyle += 1
    return hlist

#Normalize all histograms in hlist to unit area:
def selfnormalize(hlist,xlow=0,xup=0):
    for hP in hlist:
        if(not (xlow==0 and xup==0)):
            xlowBin = hP.getTH1().FindBin(xlow)
            xupBin  = hP.getTH1().FindBin(xup)
            hP.getTH1().Scale( 1.0/hP.getTH1().Integral(xlowBin,xupBin))
        else:
            hP.getTH1().Scale( 1.0/hP.getTH1().Integral())
        hP.getTH1().Sumw2(False)

