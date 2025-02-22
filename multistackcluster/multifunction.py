
import meep as mp
import math
import matplotlib.pyplot as plt
import analyses.ldos as ldos
import analyses.efields as efields

wvls = [[500, "plots/multistack500.mp4"],
        [510, "plots/multistack510.mp4"], 
        [520, "plots/multistack520.mp4"], 
        [530, "plots/multistack530.mp4"], 
        [540, "plots/multistack540.mp4"], 
        [550, "plots/multistack550.mp4"], 
        [560, "plots/multistack560.mp4"]]

def multi(source_dist, file_name, wvl = 532, spatial_resolution = 5, time_resolution=0.05, emptyspace = False, returnval = "LDOS", time_len=10, time_res = 0.1):
    cell = mp.Vector3(500, 500, 0)

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


    #Uncomment to include APTMS 1 nm layers
    def createLayer(initialOffset, order):
            return [
            mp.Block(
                mp.Vector3(tio2Width, mp.inf, mp.inf),
                center=mp.Vector3((0 + order) * tio2Width + 
                                #   (0 + 2 * order) * aptmsWidth + 
                                  (0 + order) * auWidth + 
                                  initialOffset, 0, 0),
                material=mp.Medium(epsilon=tio2N, D_conductivity=tio2C),
            ),
            mp.Block(
                mp.Vector3(auWidth, mp.inf, mp.inf),
                center=mp.Vector3((1 + order) * tio2Width + 
                                #   (1 + 2 * order) * aptmsWidth + 
                                  (0 + order) * auWidth + 
                                  initialOffset, 0, 0),
                material=mp.Medium(epsilon=auN, D_conductivity=auC),
            )
        ]


    source_pos = mp.Vector3(source_dist, 0)
    
    geometry = []
    if not emptyspace:
        for i in range(0, 4, 1):
            geometry.extend(createLayer(source_pos.x, i))

    df = freq

    sources = [
        mp.Source(
            mp.GaussianSource(frequency=freq, fwidth=df / 8, cutoff=5), component=mp.Ex, center=mp.Vector3()
        ),
        mp.Source(
            mp.GaussianSource(frequency=freq, fwidth=df / 8, cutoff=5), component=mp.Ex, center=mp.Vector3()
        ),
        mp.Source(
            mp.GaussianSource(frequency=freq, fwidth=df / 8, cutoff=5), component=mp.Ez, center=mp.Vector3()
        )
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
            framerate = 60
            cmap = 'gist_rainbow'
            return efields.evaluate(sim, time_len, time_res, framerate, cmap, file_name)
    
