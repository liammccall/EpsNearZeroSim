import numpy as np
import meep as mp
import matplotlib.pyplot as plt

import multifunction

num_wvl = 5

wvls = np.linspace(0.500, 0.600, num_wvl)

fields = []

dist = 0.010

field_dict = ["Ex", "Ey", "Ez", "Bx", "By", "Bz"]

for wvl in wvls:
    dft, _ = multifunction.multi(dist, "", wvl=wvl, returnval="Modes", spatial_resolution=500)
    fields.append([np.average(field**2) for field in dft])
    
np.save("bin/fieldvfreq_500_600", fields)    

print(fields)
for index in range(6):
    plt.plot(wvls, [field[index] for field in fields], label=field_dict[index])
    
plt.savefig("plots/fieldvfreq.png")