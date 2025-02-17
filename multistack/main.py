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
    total_x_real = []
    total_x_imag = []
    total_y_real = []
    total_y_imag = []
    total_z_real = []
    total_z_imag = []
    radiative_fluxes = []
    for dist in distances:
        
        print(dist)
        
        with nostdout():
            numx, numy, numz = multifunction.multi(532, dist, "")
            x_real = np.power(np.real(numx), 2)
            x_imag = np.power(np.imag(numx), 2)
            y_real = np.power(np.real(numy), 2)
            y_imag = np.power(np.imag(numy), 2)
            z_real = np.power(np.real(numz), 2)
            z_imag = np.power(np.imag(numz), 2)
            
            total_x_real.append(x_real)
            total_x_imag.append(x_imag)
            total_y_real.append(y_real)
            total_y_imag.append(y_imag)
            total_z_real.append(z_real)
            total_z_imag.append(z_imag)
    
    baseline_total_x, baseline_total_y, baseline_total_z = multifunction.multi(532, 0, "", True)
    
    # total_fluxes_real = total_fluxes_real / np.real(baseline_total)
    # total_fluxes_imag = total_fluxes_imag / np.imag(baseline_total)
    
    # np.save("baseline_total_rad.npy", [baseline_total, baseline_rad])
    
    # np.save("total_e_real.npy", total_fluxes_real)
    # np.save("total_e_imag.npy", total_fluxes_imag)
    
    fig, ax = plt.subplots()
    ax.plot(distances, total_x_real, label="x")
    ax.plot(distances, total_y_real, label="y")
    ax.plot(distances, total_z_real, label="z")
    ax.axhline(np.power(np.real(baseline_total_x), 2), label="x")
    ax.axhline(np.power(np.real(baseline_total_y), 2), label="y")
    ax.axhline(np.power(np.real(baseline_total_z), 2), label="z")
    ax.legend()
    fig.savefig("single_eplot_real.png")

    fig, ax = plt.subplots()
    ax.plot(distances, total_x_imag, label="x")
    ax.plot(distances, total_y_imag, label="y")
    ax.plot(distances, total_z_imag, label="z")
    ax.axhline(np.power(np.imag(baseline_total_x), 2), label="x")
    ax.axhline(np.power(np.imag(baseline_total_y), 2), label="y")
    ax.axhline(np.power(np.imag(baseline_total_z), 2), label="z")
    ax.legend()
    fig.savefig("single_eplot_imag.png")

    # np.save("baseline_total.npy", [baseline_total])
    
    # nonradiative_enhancement = total_fluxes - radiative_fluxes / (baseline_total - baseline_rad)
    # fig, ax = plt.subplots()
    # ax.plot(distances, nonradiative_enhancement)
    # fig.savefig("nonradiative_fluxplot.png")
    
if __name__ == "__main__":
    main()
