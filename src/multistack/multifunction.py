
import meep as mp
import math
import matplotlib.pyplot as plt
import analyses.ldos as ldos
import analyses.efields as efields
import analyses.cwfields as cwfields
import analyses.modes as modes
import numpy as np

from meep.materials import Au as meepAu

def get_source_dict(freq):
    return {
       "Ex": mp.Source(mp.GaussianSource(freq, fwidth = freq / 5), component = mp.Ex, center = mp.Vector3()),
       "Ey": mp.Source(mp.GaussianSource(freq, fwidth = freq / 5), component = mp.Ey, center = mp.Vector3()),
       "Ez": mp.Source(mp.GaussianSource(freq, fwidth = freq / 5), component = mp.Ez, center = mp.Vector3()),
       "Hx": mp.Source(mp.GaussianSource(freq, fwidth = freq / 5), component = mp.Hx, center = mp.Vector3()),
       "Hy": mp.Source(mp.GaussianSource(freq, fwidth = freq / 5), component = mp.Hy, center = mp.Vector3()),
       "Hz": mp.Source(mp.GaussianSource(freq, fwidth = freq / 5), component = mp.Hz, center = mp.Vector3())
    }

def multi(source_dist, file_name, wvl = 0.553, spatial_resolution = 1000, time_resolution=0.1,
          emptyspace = False, returnval = "LDOS", pml = False, glass = False,
          time_len=25, time_res = 0.1, rot_angle = 0, polarizations = ["Ex", "Ey", "Ez"]):
    cell = mp.Vector3(0.6, 0.6, 0)  

    #all nm
    freq = 1/wvl

    # tio2N = 2.67
    # tio2K = 0
    # tio2C = 0
    tio2mat = mp.Medium(epsilon = 4.855)
    tio2Width = 0.012
    # auN =  0.43
    # auK =  2.455
    # auC =  2 * math.pi * freq * auK / auN
    auMat = meepAu
    auWidth = 0.010

    if(glass):
        tio2mat = mp.Medium(epsilon = 1.52**2)
        auMat = mp.Medium(epsilon = 1.52**2)
    
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
                material=tio2mat,
                e1=mp.Vector3(x=1).rotate(mp.Vector3(z=1),rot_rads),
                e2=mp.Vector3(y=1).rotate(mp.Vector3(z=1),rot_rads)
            ),
            mp.Block(
                mp.Vector3(auWidth, mp.inf, mp.inf),
                center=mp.Vector3((1 + order) * tio2Width + 
                                #   (1 + 2 * order) * aptmsWidth + 
                                  (0.5 + order) * auWidth + 
                                  initialOffset, 0, 0).rotate(mp.Vector3(z=1), rot_rads),
                material=auMat,
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

    sources = []
    
    for pol in polarizations:
        sources.append(get_source_dict(freq)[pol])
    
    pml_thickness = 0.2
    pml_layers = [mp.Absorber(pml_thickness)]
    if(pml):
        pml_layers = [mp.PML(pml_thickness)]

    sim = mp.Simulation(
        cell_size=cell,
        eps_averaging=False,
        boundary_layers=pml_layers,
        geometry=geometry,
        sources=sources,
        force_complex_fields=True,
        resolution=spatial_resolution,
        Courant=time_resolution
    )

    dna_length = 0.0073
    framerate = 10
    cmap = 'RdBu'
    #tmp
    # non_pml_vol = mp.Volume(mp.Vector3(), mp.Vector3(cell.x - 2 * pml_thickness, cell.y - 2 * pml_thickness))
    non_pml_vol = mp.Volume(mp.Vector3(), mp.Vector3(source_dist, source_dist))
    match returnval:
        case "LDOS":
            return ldos.evaluate(sim, freq)
        case "CW":
            return cwfields.evaluate(sim, non_pml_vol, cmap, file_name)
        case "Modes":
            return modes.evaluate(sim, non_pml_vol, freq)
        case "EField":
            return efields.evaluate(sim, time_len, time_res, framerate, cmap, file_name)
        case _:
            raise ValueError(f"Return type \"{returnval}\" unknown")
    
