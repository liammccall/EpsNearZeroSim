import meep as mp
import multifunction
import mpi4py as mpi
import numpy as np

import matplotlib.pyplot as plt

field_dict = ["Ex", "Ey", "Ez", "Bx", "By", "Bz"]

dist = 0.010
wvl = 0.553
fields, eps = multifunction.multi(dist, "", wvl=wvl, returnval="Modes", spatial_resolution=100)
np.save("bin/enz_fields", fields)
np.save("bin/enz_eps", eps)
glass_fields, _ = multifunction.multi(dist, "", wvl=wvl, returnval = "Modes", spatial_resolution=100, glass=True)
np.save("bin/glass_fields", glass_fields)
ctl_fields, _ = multifunction.multi(dist, "", wvl=wvl, returnval="Modes", spatial_resolution=100, emptyspace=True)
np.save("bin/ctl_fields", ctl_fields)
fields = np.sum(np.square(fields), axis = 0)
ctl_fields = np.sum(np.square(ctl_fields), axis = 0)

q_fields = np.log10(fields**2 / ctl_fields**2)

# eps = multifunction.multi(dist, "", returnval="Modes")
field_max = np.minimum(np.max(np.abs(q_fields)), 2)
vmin = -field_max
vmax = field_max

plt.imshow(eps.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(fields.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)
plt.colorbar()
plt.savefig("plots/dft.png")
plt.clf()

plt.imshow(eps.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(ctl_fields.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7)
plt.colorbar()
plt.savefig("plots/dftctl.png")
plt.clf()

plt.imshow(eps.transpose(), interpolation='spline36', cmap='binary')
plt.imshow(q_fields.transpose(), interpolation='spline36', cmap='RdBu', alpha=0.7, vmin=vmin, vmax=vmax)
plt.colorbar()
plt.savefig("plots/dftratio.png")