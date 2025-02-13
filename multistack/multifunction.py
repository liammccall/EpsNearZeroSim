
import meep as mp
import math

wvls = [[500, "plots/multistack500.mp4"],
        [510, "plots/multistack510.mp4"], 
        [520, "plots/multistack520.mp4"], 
        [530, "plots/multistack530.mp4"], 
        [540, "plots/multistack540.mp4"], 
        [550, "plots/multistack550.mp4"], 
        [560, "plots/multistack560.mp4"]]

def multi(wvl, source_dist, filename):
    cell = mp.Vector3(1000, 1000, 0)

    #all nm
    freq = 1/wvl

    tio2N = 2.67
    tio2K = 0
    tio2C = 0
    tio2Width = 12
    aptmsN = 1.46
    aptmsK = 0
    aptmsC = 0
    aptmsWidth = 1
    auN = 0.43
    auK = 2.455
    auC = 2 * math.pi * freq * auK / auN
    auWidth = 10

    # simLength = 2 / freq
    # timeRes = simLength / 100


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
            # mp.Block(
            #     mp.Vector3(aptmsWidth, mp.inf, mp.inf),
            #     center=mp.Vector3((1 + order) * tio2Width + 
            #                       (0 + 2 * order) * aptmsWidth + 
            #                       (0 + order) * auWidth + 
            #                       initialOffset, 0, 0),
            #     material=mp.Medium(epsilon=aptmsN, D_conductivity=aptmsC),
            # ),
            mp.Block(
                mp.Vector3(auWidth, mp.inf, mp.inf),
                center=mp.Vector3((1 + order) * tio2Width + 
                                #   (1 + 2 * order) * aptmsWidth + 
                                  (0 + order) * auWidth + 
                                  initialOffset, 0, 0),
                material=mp.Medium(epsilon=auN, D_conductivity=auC),
            ),
            # mp.Block(
            #     mp.Vector3(aptmsWidth, mp.inf, mp.inf),
            #     center=mp.Vector3((1 + order) * tio2Width + 
            #                       (1 + 2 * order) * aptmsWidth + 
            #                       (1 + order) * auWidth + 
            #                       initialOffset, 0, 0),
            #     material=mp.Medium(epsilon=aptmsN, D_conductivity=aptmsC),
            # )
        ]

    geometry = []

    for i in range(0, 3, 1):
        geometry.extend(createLayer(0, i))

    # geometry = []

    source_pos = mp.Vector3(source_dist, 0)

    df = freq

    sources = [
        mp.Source(
            mp.GaussianSource(frequency=freq, fwidth=df, cutoff=5), component=mp.Ez, center=source_pos
        )
    ]

    pml_layers = [mp.PML(200)]


    resolution = 1

    sim = mp.Simulation(
        cell_size=cell,
        boundary_layers=pml_layers,
        geometry=geometry,
        sources=sources,
        resolution=resolution,
        Courant=0.2
    )

    dna_length = 2.1#7.3

    #Find flux around emitter
    total_flux = mp.FluxRegion(center=source_pos, size=mp.Vector3(2 * dna_length, 2 * dna_length), weight = -1.0)

    acceptor_box = sim.add_flux(freq, 0, 1,        
                mp.FluxRegion(source_pos + mp.Vector3(y = dna_length), size=mp.Vector3(2 * dna_length)),
                mp.FluxRegion(source_pos + mp.Vector3(y = -dna_length), size=mp.Vector3(2 * dna_length), weight=-1),
                mp.FluxRegion(source_pos + mp.Vector3(dna_length), size=mp.Vector3(y=2 * dna_length)),
                mp.FluxRegion(source_pos + mp.Vector3(-dna_length), size=mp.Vector3(y=2 * dna_length), weight=-1))

    ez_data = []
    
    sim.run(until_after_sources=mp.stop_when_fields_decayed(1, mp.Ez, source_pos + mp.Vector3(dna_length), 1e-8))
    
    return mp.get_fluxes(acceptor_box)