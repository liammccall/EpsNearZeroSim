import matplotlib.pyplot as plt
import numpy as np
import meep as mp
from meep import mpb
import os
import io

import materials.asml as asml

import plots.bandvisualizer

import simulation.mpbsolver as hexSolver
import simulation.tdsolver  as tdSolver

def main():
    # fdsim()
    tdsim()
    
def tdsim():
    
    latticeConstant = 0.400
    
    silMat = asml.fitMaterial("data/AspnesCrystallineNanometers.csv", [0.4, 0.7], "um", 1, 1)
    
    sim = tdSolver.create2dHexSolver(silMat, latticeConstant, 30) # ?
    
    
    k_points = [
        latticeConstant * mp.Vector3(y=0.5),  # M
        latticeConstant * mp.Vector3(),  # Gamma
        latticeConstant * mp.Vector3(1 / -3, 1 / 3),  # K
    ]

    k_interp = 10 # number of k_points to interpolate
    k_points = mp.interpolate(k_interp, k_points)
    
    freqs = sim.run_k_points(200, k_points)
    
    # np.save("bin\\simresults\\td\\freqs", freqs)
    
    xGrid = np.linspace(0, 1, len(freqs))
    
    fig = plt.figure(dpi=100, figsize=(5, 5))
    
    for i in range(len(freqs)):
        for ii in range(len(freqs[i])):
            plt.scatter(xGrid[i], 1000 / np.real(freqs[i][ii]), color="b")
            
    plt.xlim(0, 1)
    plt.grid(True)
    plt.xlabel("$K-\Gamma-M$")
    plt.ylabel("$\omega(2\pi c)$")
    plt.tight_layout()
    
    
    fig.savefig("tdout.png", dpi=150, bbox_inches="tight")
    
    eps_data = sim.get_array(center=mp.Vector3(), size=sim.cell_size, component=mp.Dielectric)
    plt.figure()
    plt.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
    plt.axis('off')
    
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
    
    
    np.save("bin\\simresults\\te_freqs", te_freqs)
    
    np.save("bin\\simresults\\te_gaps", te_gaps)
    
    return te_freqs, te_gaps
    
    
    
if(__name__ == '__main__'):
    main()
