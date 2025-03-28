## launch a Gaussian beam
import math

import matplotlib

import meep as mp

# matplotlib.use("agg")
import matplotlib.pyplot as plt

s = 1500
resolution = 0.1
dpml = 50

cell_size = mp.Vector3(s, s)

boundary_layers = [mp.PML(thickness=dpml)]

beam_x0 = mp.Vector3(10)  # beam focus (relative to source center)
rot_angle = 10  # CCW rotation angle about z axis (0: +y axis)
beam_kdir = mp.Vector3(1, 0, 0).rotate(
    mp.Vector3(0, 0, 1), math.radians(rot_angle))  # beam propagation direction
beam_w0 = 50  # beam waist radius
beam_E0 = mp.Vector3(0, 1, 0).rotate(
    mp.Vector3(0, 0, 1), math.radians(rot_angle))
beam_E0 = mp.Vector3(0, 0, 1)
fcen = 1/532
sources = [
    mp.GaussianBeamSource(
        src=mp.ContinuousSource(fcen),
        center=mp.Vector3(-s / 2 + dpml),
        size=mp.Vector3(y=s/2),
        beam_x0=beam_x0,
        beam_kdir=beam_kdir,
        beam_w0=beam_w0,
        beam_E0=beam_E0,
    )
]

sim = mp.Simulation(
    resolution=resolution,
    cell_size=cell_size,
    boundary_layers=boundary_layers,
    sources=sources,
)

sim.run(until=1500)

sim.plot2D(
    fields=mp.Ez,
    output_plane=mp.Volume(
        center=mp.Vector3(), size=mp.Vector3(s - 2 * dpml, s - 2 * dpml)
    ),
)

plt.show()
# plt.savefig(f"Ex_angle{rot_angle}.png", bbox_inches="tight", pad_inches=0)