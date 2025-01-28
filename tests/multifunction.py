
import meep as mp
import math

wvls = [[500, "plots/multistack500.mp4"],
        [510, "plots/multistack510.mp4"], 
        [520, "plots/multistack520.mp4"], 
        [530, "plots/multistack530.mp4"], 
        [540, "plots/multistack540.mp4"], 
        [550, "plots/multistack550.mp4"], 
        [560, "plots/multistack560.mp4"]]

def multi(wvl, filename):
    # From the Meep tutorial: plotting permittivity and fields of a straight waveguide

    cell = mp.Vector3(1000, 1000, 0)

    #all nm
    #wvl = 532
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

    simLength = 10 / freq
    timeRes = simLength / 1000


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

    sources = [
        mp.Source(
            mp.ContinuousSource(frequency=freq), component=mp.Ez, center=mp.Vector3(-100, 0)
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

    import matplotlib.pyplot as plt
    
    f = plt.figure()

    def zoomin(ax):
        ax.set_xlim(-100, 100)
        ax.set_ylim(-100, 100)
        return ax
    
    Animate = mp.Animate2D(fields=mp.Ez, f=f, realtime=False, normalize=False, plot_modifiers=[zoomin], 
                               field_parameters={'alpha':0.8, 'cmap':'prism', 'interpolation':'spline36'})
    plt.close()

    sim.run(mp.at_every(timeRes, Animate), until=simLength)
    plt.close()

    # filename = "plots/multistack.mp4"
    Animate.to_mp4(10, filename)
    
for combi in wvls:
    multi(combi[0], combi[1])