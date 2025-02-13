import numpy as np
import multifunction
import matplotlib.pyplot as plt

def main():
    distances = np.linspace(5, 45, 10)
    fluxes = []
    for dist in distances:
        fluxes.append(multifunction.multi(532, dist, ""))
    
    np.save("fluxes.npy", fluxes)
    
    fig, ax = plt.subplots()
    ax.plot(distances, fluxes)
    fig.savefig("fluxplot.png")
    
if __name__ == "__main__":
    main()