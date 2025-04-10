import meep as mp
import numpy as np
import matplotlib.pyplot as plt

idx = 0

wvl = ""
# Load data
ex_data = np.load(f"bin/enz_fields{wvl}.npy")[idx]
ex_data_ctl = np.load(f"bin/ctl_fields.npy")[idx]
ex_data_glass = np.load(f"bin/glass_fields{wvl}.npy")[idx]
eps_data = np.load(f"bin/enz_eps.npy")

# Extract center halves

ex_data = np.power(ex_data, 2)
ex_data_ctl = np.power(ex_data_ctl, 2)
ex_data_glass = np.power(ex_data_glass, 2)

# ex = ex_data
# ey = ey_data
# ez = ez_data
ex = np.log10(np.divide(ex_data , ex_data_glass)) / 2
# ex = np.log10(ex_data_ctl)
# ex = np.subtract(ex_data , ex_data_ctl)
# ey = np.subtract(ey_data , ey_data_ctl)
# ez = np.subtract(ez_data , ez_data_ctl)
print(np.average(ex))

# ex = ex / np.average(ex_data)
# ey = ey / np.average(ey_data)
# ez = ez / np.average(ez_data)
    
# plt.figure()
fig, axes = plt.subplots(1, 1, figsize=(5, 5))
bound = np.maximum(np.max(ex), -1 * np.min(ex))
print(bound)
bound = np.minimum(bound, 2)
axes.imshow(eps_data.transpose(), interpolation='spline36', cmap='binary')
im0 = axes.imshow(ex.transpose(), interpolation='spline36', cmap='Reds', alpha=0.9, vmax = bound, vmin = 0)#-bound)
fig.colorbar(im0, ax=axes)
# plt.show()
fig.savefig("plots/compare.png")