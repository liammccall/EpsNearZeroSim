
import meep as mp
import math
import matplotlib.pyplot as plt
import analyses.ldos as ldos
import analyses.efields as efields
import numpy as np

wvls = [[500, "plots/multistack500.mp4"],
        [510, "plots/multistack510.mp4"], 
        [520, "plots/multistack520.mp4"], 
        [530, "plots/multistack530.mp4"], 
        [540, "plots/multistack540.mp4"], 
        [550, "plots/multistack550.mp4"], 
        [560, "plots/multistack560.mp4"]]

def multi(source_dist, file_name, wvl = 532, spatial_resolution = 0.1, time_resolution=0.1,
          emptyspace = False, returnval = "LDOS",
          time_len=500, time_res = 1, rot_angle = -20):
    cell = mp.Vector3(600, 600, 0)

    #all nm
    freq = 1/wvl

    tio2N = 2.67
    tio2K = 0
    tio2C = 0
    tio2Width = 12
    auN = 0.43
    auK = 2.455
    auC = 2 * math.pi * freq * auK / auN
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
            geometry.extend(createLayer(source_dist / 2, i))


    # beam_x0 = mp.Vector3(100, 0, 0)  # beam focus (relative to source center)
    # beam_kdir = mp.Vector3(1, 0, 0)  # beam propagation direction
    # beam_w0 = 100  # beam waist radius
    # beam_E0 = mp.Vector3(0, 1, 0)
    # source_size = 100
    # sources = [
    #     mp.GaussianBeamSource(
    #         src=mp.ContinuousSource(freq),
    #         center=mp.Vector3(),
    #         size=mp.Vector3(y=source_size),
    #         beam_x0=beam_x0,
    #         beam_kdir=beam_kdir,
    #         beam_w0=beam_w0,
    #         beam_E0=beam_E0,
    #     )
    # ]
    
    sources = [
        mp.Source(mp.GaussianSource(freq, fwidth=freq / 100), mp.Ey)
    ]

    pml_thickness = 100
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
    
