import matplotlib.pyplot as plt
import numpy as np
import meep as mp
from meep import mpb
import os
import io

import disRel.lorentzfit as lf
import disRel.processInput as pi

import plots.bandvisualizer

import simulation.mpbsolver as hexSolver
import simulation.tdsolver  as tdSolver

def main():
    fdsim()
    # tdsim()
    
def tdsim():
    
    silMat = pi.getFitted("data/AspnesCrystallineNanometers.csv", 0.4, 0.7, "um", 1, 1)
    
    sim = tdSolver.create2dHexSolver(silMat, 1) # ?
    
    
    f = plt.figure(dpi=150)
    sim.plot2D(ax=f.gca())
    plt.show()
    
        

def fdsim():
    
    latticeConstant = 0.400 # um
    
    # te_freqs, te_gaps = recalc(latticeConstant)
    
    te_freqs = np.load("bin\\simresults\\te_freqs.npy")
    te_gaps = np.load("bin\\simresults\\te_gaps.npy")
    
    te_freqs = ((latticeConstant / 3e8) / te_freqs) * 1e12
    
    plots.bandvisualizer.saveFigure(te_freqs, te_freqs, te_gaps, te_gaps)
    
    gammaDiracPoint = te_freqs[(len(te_freqs) + 1) // 2][4]
    
    print(str(gammaDiracPoint) + " c/a")
    
    print("a = " + str(gammaDiracPoint * latticeConstant) + "um")
    
def recalc(latticeConstant):
    
    silMat = pi.getFitted("data/AspnesCrystallineNanometers.csv", (0.4, 0.8), "um", 6, 15)
    
    #silMat = mp.Medium(epsilon = 18.7)
    hexSim =  hexSolver.create2DHexSolver(silMat, latticeConstant)
    
    #np.save("bin\\mats", hexSim)
    
    # hexSim.run_tm()
    # tm_freqs = hexSim.all_freqs
    # tm_gaps = hexSim.gap_list
     
    hexSim.run_te()
    te_freqs = hexSim.all_freqs
    te_gaps = hexSim.gap_list
    
    # hexSim._output_scalar_field("n", "te")
    
    # hexSim.output_field_to_file(mp.Ez, "field")
    
    field : mpb.MPBArray = hexSim.get_efield(5)
    
    
    
    np.save("bin\\simresults\\te_freqs", te_freqs)
    
    np.save("bin\\simresults\\te_gaps", te_gaps)
    
    return te_freqs, te_gaps
    
    
    
if(__name__ == '__main__'):
    main()
