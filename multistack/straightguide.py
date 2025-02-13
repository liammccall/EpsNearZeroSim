# From the Meep tutorial: plotting permittivity and fields of a straight waveguide
import meep as mp

cell = mp.Vector3(16, 8, 0)

geometry = [
    mp.Block(
        mp.Vector3(mp.inf, 1, mp.inf),
        center=mp.Vector3(),
        material=mp.Medium(epsilon=12),
    )
]
geometry = []

sources = [
    mp.Source(
        mp.ContinuousSource(frequency=0.15), component=mp.Ez, center=mp.Vector3(-7, 0)
    )
]

pml_layers = [mp.PML(1.0)]

resolution = 10

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=pml_layers,
    geometry=geometry,
    sources=sources,
    resolution=resolution,
)

sim.run(until=200)

import matplotlib.pyplot as plt
import numpy as np

# eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
# plt.axis("off")
# plt.show()

# ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ez)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
# plt.imshow(ez_data.transpose(), interpolation="spline36", cmap="RdBu", alpha=0.9)
# plt.axis("off")
# plt.show()

sim.reset_meep()
f = plt.figure(dpi=100)

def zoomin(ax):
    # ax.set_xlim(-0.7, 0.7)
    # ax.set_ylim(-0.2, 0.2)
    return ax

Animate = mp.Animate2D(fields=mp.Ez, f=f, realtime=False, normalize=True, plot_modifiers=[zoomin])
plt.close()

sim.run(mp.at_every(1, Animate), until=100)
plt.close()

filename = "plots/straightguide.mp4"
Animate.to_mp4(1, filename)