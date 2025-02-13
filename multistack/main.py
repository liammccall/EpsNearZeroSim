import numpy as np
import multifunction
import matplotlib.pyplot as plt

import contextlib
import io
import sys

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout

def main():
    distances = np.linspace(5, 100, 100)
    total_fluxes = []
    radiative_fluxes = []
    for dist in distances:
        
        print(dist)
        
        with nostdout():
            total = np.abs(multifunction.multi(532, dist, ""))
            
        total_fluxes.append(total)
    
    baseline_total= multifunction.multi(532, 0, "", True)
    
    total_fluxes = total_fluxes / np.abs(baseline_total)
    
    # np.save("baseline_total_rad.npy", [baseline_total, baseline_rad])
    
    np.save("total_fluxes.npy", total_fluxes)
    
    fig, ax = plt.subplots()
    ax.plot(distances, total_fluxes)
    fig.savefig("single_eplot.png")
    
    # nonradiative_enhancement = total_fluxes - radiative_fluxes / (baseline_total - baseline_rad)
    # fig, ax = plt.subplots()
    # ax.plot(distances, nonradiative_enhancement)
    # fig.savefig("nonradiative_fluxplot.png")
    
if __name__ == "__main__":
    main()
