import meep as mp
import numpy as np
import math
import matplotlib.pyplot as plt

import meep as mp
import math
import matplotlib.pyplot as plt
import analyses.ldos as ldos
import analyses.efields as efields
import numpy as np


def multi(source_dist, file_name, wvl = 532, spatial_resolution = 1, time_resolution=0.1,
          emptyspace = False, returnval = "LDOS",
          time_len=25, time_res = 0.1, rot_angle = 0):
    cell = mp.Vector3(600, 600, 0)  

    #all nm
    freq = 1/wvl

    tio2N = 2.67
    tio2K = 0
    tio2C = 0
    tio2Width = 12
    auN =  0.43
    auK =  2.455
    auC =  2 * math.pi * freq * auK / auN
    auWidth = 10

    rot_rads = np.radians(rot_angle)

    #Uncomment to include APTMS 1 nm layers
    def createLayer(initialOffset, order):
            return [
            mp.Block(
                mp.Vector3(tio2Width, mp.inf, mp.inf),
                center=mp.Vector3((0.5 + order) * tio2Width + 
                                #   (0 + 2 * order) * aptmsWidth + 
                                  (0 + order) * auWidth + 
                                  initialOffset, 0, 0).rotate(mp.Vector3(z=1), rot_rads),
                material=mp.Medium(epsilon=tio2N, D_conductivity=tio2C),
                e1=mp.Vector3(x=1).rotate(mp.Vector3(z=1),rot_rads),
                e2=mp.Vector3(y=1).rotate(mp.Vector3(z=1),rot_rads)
            ),
            mp.Block(
                mp.Vector3(auWidth, mp.inf, mp.inf),
                center=mp.Vector3((1.5 + order) * tio2Width + 
                                #   (1 + 2 * order) * aptmsWidth + 
                                  (0 + order) * auWidth + 
                                  initialOffset, 0, 0).rotate(mp.Vector3(z=1), rot_rads),
                material=mp.Medium(epsilon=auN, D_conductivity=auC),
                e1=mp.Vector3(x=1).rotate(mp.Vector3(z=1),rot_rads),
                e2=mp.Vector3(y=1).rotate(mp.Vector3(z=1),rot_rads)
            )
        ]
    
    geometry = []
    if not emptyspace:
        for i in range(0, 3, 1):
            geometry.extend(createLayer(source_dist, i))


    # beam_x0 = mp.Vector3(100, 0, 0)  # beam focus (relative to source center)
    # beam_kdir = mp.Vector3(1, 0, 0)  # beam propagation direction
    # beam_w0 = 100  # beam waist radius
    # beam_E0 = mp.Vector3(0, 1, 0)
    # source_size = 100
    # sources = [
    #     mp.GaussianBeamSource(
    #         src=mp.ContinuousSource(freq),
    #         center=mp.Vector3(),
    #         size=mp.Vector3(y=source_size, z=source_size),
    #         beam_x0=beam_x0,
    #         beam_kdir=beam_kdir,
    #         beam_w0=beam_w0,
    #         beam_E0=beam_E0,
    #     )
    # ]

    sources = [
        mp.Source(mp.ContinuousSource(freq,is_integrated=True), component = mp.Hx, center = mp.Vector3()),
        mp.Source(mp.ContinuousSource(freq,is_integrated=True), component = mp.Hy, center = mp.Vector3()),
        mp.Source(mp.ContinuousSource(freq,is_integrated=True), component = mp.Hz, center = mp.Vector3()),
        mp.Source(mp.ContinuousSource(freq,is_integrated=True), component = mp.Ex, center = mp.Vector3()),
        mp.Source(mp.ContinuousSource(freq,is_integrated=True), component = mp.Ey, center = mp.Vector3()),
        mp.Source(mp.ContinuousSource(freq,is_integrated=True), component = mp.Ez, center = mp.Vector3()),
    #    mp.Source(mp.GaussianSource(freq, fwidth = freq / 20), component = mp.Hx, center = mp.Vector3()),
    #    mp.Source(mp.GaussianSource(freq, fwidth = freq / 20), component = mp.Hy, center = mp.Vector3()),
    #    mp.Source(mp.GaussianSource(freq, fwidth = freq / 20), component = mp.Hz, center = mp.Vector3()),
    #    mp.Source(mp.GaussianSource(freq, fwidth = freq / 20), component = mp.Ex, center = mp.Vector3()),
    #    mp.Source(mp.GaussianSource(freq, fwidth = freq / 20), component = mp.Ey, center = mp.Vector3()),
    #    mp.Source(mp.GaussianSource(freq, fwidth = freq / 20), component = mp.Ez, center = mp.Vector3())
    ]
    
    pml_thickness = 150
    pml_layers = [mp.PML(pml_thickness)]

    sim = mp.Simulation(
        cell_size=cell,
        boundary_layers=pml_layers,
        geometry=geometry,
        sources=sources,
        resolution=spatial_resolution,
        Courant=time_resolution
    )

    dna_length = 7.3
    
    match returnval:
        case "LDOS":
            return ldos.evaluate(sim, freq)
        case "EField":
            framerate = 10
            cmap = 'hsv'
            return efields.evaluate(sim, time_len, time_res, framerate, cmap, file_name)
        case _:
            raise ValueError(f"Return type \"{returnval}\" unknown")

resolution = 50  # pixels/μm

# Define computational domain parameters
dpml = 1.0  # PML thickness
dsub = 1.0  # Substrate thickness
dpad = 1.0  # Padding thickness
gp = 6.5  # Grating period

# Define material properties
n_0 = 1.55
k_0 = 0.02  # Imaginary part for absorption
delta_n = 0.159
epsilon_diag = mp.Matrix(mp.Vector3(n_0**2 - k_0**2, 0, 0),
                          mp.Vector3(0, n_0**2 - k_0**2, 0),
                          mp.Vector3(0, 0, (n_0 + delta_n)**2 - k_0**2))

wvl = 0.54  # Wavelength
fcen = 1 / wvl  # Center frequency

# Define grating structure
def pol_grating(d, ph, gp, nmode):
    sx = dpml + dsub + d + d + dpad + dpml
    sy = gp
    cell_size = mp.Vector3(sx, sy, 0)

    def phi(p):
        xx = p.x - (-0.5 * sx + dpml + dsub)
        if 0 <= xx <= d:
            return math.pi * p.y / gp + ph * xx / d
        else:
            return math.pi * p.y / gp - ph * xx / d + 2 * ph

    def lc_mat(p):
        Rx = mp.Matrix(mp.Vector3(1, 0, 0),
                       mp.Vector3(0, math.cos(phi(p)), math.sin(phi(p))),
                       mp.Vector3(0, -math.sin(phi(p)), math.cos(phi(p))))
        lc_epsilon = Rx * epsilon_diag * Rx.transpose()
        return mp.Medium(epsilon_diag=mp.Vector3(lc_epsilon[0].x, lc_epsilon[1].y, lc_epsilon[2].z))

    geometry = [mp.Block(center=mp.Vector3(-0.5 * sx + 0.5 * (dpml + dsub)),
                          size=mp.Vector3(dpml + dsub, mp.inf, mp.inf),
                          material=mp.Medium(index=n_0)),
                mp.Block(center=mp.Vector3(-0.5 * sx + dpml + dsub + d),
                          size=mp.Vector3(2 * d, mp.inf, mp.inf),
                          material=lc_mat)]

    sources = [mp.Source(mp.GaussianSource(fcen, fwidth=0.05 * fcen),
                          component=mp.Ez,
                          center=mp.Vector3(-0.5 * sx + dpml + 0.3 * dsub, 0, 0),
                          size=mp.Vector3(0, sy, 0))]

    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=[mp.PML(thickness=dpml)],
                        geometry=geometry,
                        sources=sources)

    tran_flux = sim.add_flux(fcen, 0, 1, mp.FluxRegion(center=mp.Vector3(0.5 * sx - dpml - 0.5 * dpad, 0, 0), size=mp.Vector3(0, sy, 0)))
    sim.run(until_after_sources=300)
    res = sim.get_eigenmode_coefficients(tran_flux, range(1, nmode + 1))
    return res.alpha[:, 0, 0]

# Compute mode coefficients for different thicknesses
ph = math.radians(70)
nmode = 5
dd = np.arange(0.1, 3.5, 0.1)
coefficients = [pol_grating(d, ph, gp, nmode) for d in dd]

# Plot diffraction efficiency
plt.figure(dpi=150)
plt.plot(dd, [abs(c[0])**2 for c in coefficients], 'bo-', label='0th order')
plt.plot(dd, [abs(c[1])**2 for c in coefficients], 'ro-', label='±1 orders')
plt.xlabel("Grating Thickness (μm)")
plt.ylabel("Diffraction Efficiency")
plt.legend()
plt.show()
