from ROOT import *
from hPlus import *
from style import *

def DrawSameFromList(hTitle,hlist,legend):
    ymins = []
    ymaxs = []
    for h in hlist:
        h.setStyle()
        h.setLabel()
        ymins.append( h.getTH1().GetMinimum() )
        ymaxs.append( h.getTH1().GetMaximum() )
        legend.AddEntry(h.getTH1(),h.getTH1().GetName(),"l")
    hlist[0].getTH1().SetMaximum( max(ymaxs)*1.5 )
    hlist[0].getTH1().GetXaxis().SetRangeUser(1500,13000) 
    if (not min(ymins)==0): 
        hlist[0].getTH1().SetMinimum( min(ymins)*0.5 )
    elif (c1.GetLogy()):
        hlist[0].getTH1().SetMinimum( min(ymins)+1E-1 ) # if there are empty bins but we need log axis
    else:
        hlist[0].getTH1().SetMinimum( 0 )
    hlist[0].getTH1().SetTitle(hTitle)
    hlist.pop(0).getTH1().Draw()
    for h in hlist:
        print h.getTH1().GetName(),h.getTH1().GetMean(1)
        h.getTH1().Draw("Same")
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.Draw()
    #c1.BuildLegend(0.7,0.7,0.9,0.9)
    
# Loop through a list of hPlus, print it into a pdf file
# histo_Dict:
# key hname, value list of hPlus objects from flist with name hTitle
def makepdf(pages,outputFile):
    nItems = len(pages)
    i      = 1
    nPad   = 1
    nPages = 0
    IsLast = False
    for page in pages:
        # Prepare the canvas
        DrawSameFromList(page["Title"],page["list"],page["legend"])
        # Open a new page
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
def getHlistFromNames(tFile,hKeys,xLabel,yLabel):
    hlist = []
    rootfile = TFile(tFile)
    istyle=0
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
