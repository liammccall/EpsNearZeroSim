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
    distances = np.linspace(10, 100, 100)
    total_fluxes_real = []
    total_fluxes_imag = []
    radiative_fluxes = []
    for dist in distances:
        
        print(dist)
        
        with nostdout():
            num = multifunction.multi(532, dist, "")
            total = np.power(np.real(num), 2)
            total_im = np.power(np.imag(num), 2)
            
        total_fluxes_real.append(total)
        total_fluxes_imag.append(total_im)
    
    baseline_total = multifunction.multi(532, 0, "", True)
    
    # total_fluxes_real = total_fluxes_real / np.real(baseline_total)
    # total_fluxes_imag = total_fluxes_imag / np.imag(baseline_total)
    
    # np.save("baseline_total_rad.npy", [baseline_total, baseline_rad])
    
    np.save("total_e_real.npy", total_fluxes_real)
    np.save("total_e_imag.npy", total_fluxes_imag)
    
    fig, ax = plt.subplots()
    ax.plot(distances, total_fluxes_real)
    ax.axhline(np.power(np.real(baseline_total), 2))
    fig.savefig("single_eplot_real.png")

    fig, ax = plt.subplots()
    ax.plot(distances, total_fluxes_imag)
    ax.axhline(np.power(np.imag(baseline_total), 2))
    fig.savefig("single_eplot_imag.png")

    np.save("baseline_total.npy", [baseline_total])
    
    # nonradiative_enhancement = total_fluxes - radiative_fluxes / (baseline_total - baseline_rad)
    # fig, ax = plt.subplots()
    # ax.plot(distances, nonradiative_enhancement)
    # fig.savefig("nonradiative_fluxplot.png")
    
if __name__ == "__main__":
    main()
