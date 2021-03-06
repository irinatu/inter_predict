from sys import argv, exit
from collections import defaultdict

import optparse, os, math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from util import clip_and_blur

from matplotlib.backends import backend_pdf
from matplotlib import rcParams, cm



def lines(path,header=True):
    with open(path,'r') as handle:
        if header:
            handle.next()
        else: pass
        for line in handle:
            yield line.split('\n')[0].split()

def parse_domains(gen):
    domains = defaultdict(list)
    #nr = 0
    for l in gen:
        #print l
        if l[0].split('chr')[1] == opts.Chrom:
            start = float(l[1])/50000.0 
            end = (float(l[2])/50000.0) - 1 
            domains[l[3].split('\n')[0]].append((start,end))
    return domains

def plot_all(mtx, mt_i, inp, out):
    #with backend_pdf.PdfPages("%s-%s_Rafala.pdf" % (os.path.basename(inp), os.path.basename(out))) as pdf:
        #plt.figure(dpi=1200)
        #mtx = np.load(mat)
        #fig = plt.figure(dpi=2200)
        #fig = plt.figure()
        #colormap = plt.cm.gist_ncar
        #plt.imshow(mtx,interpolation='nearest',origin='lower',norm=LogNorm(),cmap=cm.jet)
        
    plt.imshow(np.tril(mtx),origin='upper',norm=LogNorm(),cmap="Blues", interpolation='nearest')
    #print "SPRAWDZAM", mt_i[1196:1219, 1640:1672]    
    plt.imshow(mt_i,origin='upper',norm=LogNorm(),cmap="Reds", interpolation = 'nearest')
    plt.colorbar()
    
    plt.axis([0,mtx.shape[0],0,mtx.shape[0]])
    plt.legend(loc='best')
    plt.title("Plot",fontsize=7)
    out = "%s-%s.png" % (os.path.basename(inp).split('.')[0], os.path.basename(out).split('.')[0])
    #pdf.savefig(fig, dpi = 1500)
    plt.savefig(out, dpi = 1500, bbox_inches='tight')
    plt.close()
    print "finished plotting" 

def prepar_interac_matr(inte, si, dom):
    i_m = np.zeros((si, si))
    ZERO = True
    #print dom
    header = True
    if header: inte.next()
    else: pass
    for l in inte:
        #print l
        if l[2] != '0.0':
            print l, dom.keys()
            dom1 = [dom[i] for i in dom.keys() if i == l[0]]
            dom2 = [dom[i] for i in dom.keys() if i == l[1]]
            dom1_2 = sum(dom1 + dom2,[])
            print dom1_2
            if dom1_2[0]==dom1_2[1]:
                #print dom1_2[0], dom1_2[1]
                i_m[int(dom1_2[0][0]):int(dom1_2[0][1])+1, int(dom1_2[1][0]):int(dom1_2[1][1])+1] = 0.0
            
            elif len(dom1_2) == 2:
                #print dom1_2[0][0], int(dom1_2[0][1])+1, dom1_2[1][0], int(dom1_2[1][1])+1, i_m.shape
                i_m[int(dom1_2[0][0]):int(dom1_2[0][1])+1, int(dom1_2[1][0]):int(dom1_2[1][1])+1] = round(-math.log10(float(l[2])), 5)
                
            elif len(dom1_2) == 1:
                #print dom1_2, dom1, dom2
                i_m[int(dom1_2[0][0]):int(dom1_2[0][1])+1, int(dom1_2[1][0]):int(dom1_2[1][1])+1] = round(-math.log10(float(l[2])), 5)
                
            else: print "More domains!!!!", dom1_2
        elif ZERO:
            
            dom1 = [dom[i] for i in dom.keys() if i == l[0]]
            dom2 = [dom[i] for i in dom.keys() if i == l[1]]
            dom1_2 = sum(dom1 + dom2,[])
           
            if dom1_2[0]==dom1_2[1]:
                #print dom1_2[0], dom1_2[1]
                i_m[int(dom1_2[0][0]):int(dom1_2[0][1])+1, int(dom1_2[1][0]):int(dom1_2[1][1])+1] = 0.0
                
            elif len(dom1_2) == 2:
                #print dom1_2, type(dom1)
                i_m[int(dom1_2[0][0]):int(dom1_2[0][1])+1, int(dom1_2[1][0]):int(dom1_2[1][1])+1] = 500
                
            elif len(dom1_2) == 1:
                #print dom1_2, dom1, dom2
                i_m[int(dom1_2[0][0]):int(dom1_2[0][1])+1, int(dom1_2[1][0]):int(dom1_2[1][1])+1] = 500
                
            else: print "More domains!!!!", dom1_2
        else:
            pass
    
    return np.triu(i_m)

if __name__=="__main__":
    
    optparser = optparse.OptionParser(usage = "%prog [<options>]")
    optparser.add_option('-m', type = "string", default = "", dest="Matrix", help = "Numpy matrix in npy format")
    optparser.add_option('-d', type = "string", default = "", dest="Domains", help ="Txt file with domain information")
    optparser.add_option('-i', type = "string", default = "", dest="Interaction", help ="Txt file with domain-domain interactions")
    optparser.add_option('-l', type = "string", default = "", dest="Level", help ="The level of sherpa")
    optparser.add_option('-c', type = "string", default = "", dest="Chrom", help ="The level of sherpa")
    
    (opts,args) = optparser.parse_args()
    if len(argv) ==1:
        print optparser.format_help()
        exit(1)

    domeny = parse_domains(lines(opts.Domains, header=False))
    #print domeny
    matr = np.load(opts.Matrix)
    
    matr = clip_and_blur(matr)
    size =  matr.shape[0]
    
    inter_mtx = prepar_interac_matr(lines(opts.Interaction, header=False), size, domeny)
    
    plot_all(matr, inter_mtx, opts.Matrix, opts.Interaction)
    
    #Sprawdzenie symetrycznosci
    #inter_mtx[np.isnan(inter_mtx)] = 0
    #print  np.allclose(np.transpose(inter_mtx), inter_mtx), inter_mtx.size - np.isnan(inter_mtx).sum()
    
    
