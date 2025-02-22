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
    ldos=[]
    for dist in distances:
        
        print(dist)
        
        with nostdout():
            numx = multifunction.multi(532, dist, "")
            ldos.append(numx)
    
    baseline = multifunction.multi(532, 0, "", True)
    
    # total_fluxes_real = total_fluxes_real / np.real(baseline_total)
    # total_fluxes_imag = total_fluxes_imag / np.imag(baseline_total)
    
    # np.save("baseline_total_rad.npy", [baseline_total, baseline_rad])
    
    # np.save("total_e_real.npy", total_fluxes_real)
    # np.save("total_e_imag.npy", total_fluxes_imag)
    
    fig, ax = plt.subplots()
    ax.plot(distances, np.divide(ldos,baseline))
    # ax.axhline(np.power(np.real(baseline), 2))
    fig.savefig("ldos.png")

    # np.save("baseline_total.npy", [baseline_total])
    
    # nonradiative_enhancement = total_fluxes - radiative_fluxes / (baseline_total - baseline_rad)
    # fig, ax = plt.subplots()
    # ax.plot(distances, nonradiative_enhancement)
    # fig.savefig("nonradiative_fluxplot.png")
    
if __name__ == "__main__":
    main()
