import meep as mp
import numpy as np
import matplotlib.pyplot as plt

def center(array):
    M, N = array.shape  # Get dimensions
    return array[3*M//8:5*M//8, 3*N//8:5*N//8]  # Slice center

# Load data
ex_data = np.load("bin/cw_10_1_tm_ex.npy")
ey_data = np.load("bin/cw_10_1_tm_ey.npy")
ez_data = np.load("bin/cw_10_1_tm_ez.npy")
ex_data_ctl = np.load("bin/cw_10_1_tm_ctl_ex.npy")
ey_data_ctl = np.load("bin/cw_10_1_tm_ctl_ey.npy")
ez_data_ctl = np.load("bin/cw_10_1_tm_ctl_ez.npy")

# Extract center halves
ex_data = center(ex_data)
ey_data = center(ey_data)
ez_data = center(ez_data)
ex_data_ctl = center(ex_data_ctl)
ey_data_ctl = center(ey_data_ctl)
ez_data_ctl = center(ez_data_ctl)

ex_data = np.power(ex_data, 2)
ey_data = np.power(ey_data, 2)
ez_data = np.power(ez_data, 2)
ex_data_ctl = np.power(ex_data_ctl, 2)
ey_data_ctl = np.power(ey_data_ctl, 2)
ez_data_ctl = np.power(ez_data_ctl, 2)

# ex = np.divide(ex_data , ex_data_ctl)
# ey = np.divide(ey_data , ey_data_ctl)
# ez = np.divide(ez_data , ez_data_ctl)
ex = np.subtract(ex_data , ex_data_ctl)
ey = np.subtract(ey_data , ey_data_ctl)
ez = np.subtract(ez_data , ez_data_ctl)
print(np.max(ex))
print(np.average(ex_data))
print(np.min(ex))

ex = ex / np.average(ex_data)
ey = ey / np.average(ey_data)
ez = ez / np.average(ez_data)
    
# plt.figure()
fig, axes = plt.subplots(3, 1, figsize=(5, 15))
im0 = axes[0].imshow(ex.transpose(), interpolation='spline36', cmap='Reds', alpha=0.9)
im1 = axes[1].imshow(ey.transpose(), interpolation='spline36', cmap='Reds', alpha=0.9)
im2 = axes[2].imshow(ez.transpose(), interpolation='spline36', cmap='Reds', alpha=0.9)

fig.colorbar(im0, ax=axes[0])
fig.colorbar(im1, ax=axes[1])
fig.colorbar(im2, ax=axes[2])
plt.show()