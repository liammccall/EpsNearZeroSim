import meep as mp
import math
from numpy import random

def create2dHexSolver(silMat, latticeConstant : float, numSources : int):
    
    #phase decoherence look at website
    #simulate dipole

    rPillar = latticeConstant * ((1/3) - (1/30))
    
    # Rectangular supercell
    
    sideLength = latticeConstant / (2 * math.cos(math.pi / 6))
    
    cellLength = 3 * sideLength

    cell = mp.Vector3(latticeConstant, cellLength)
    
    geometry = [
        
        # Four permutations of interior pillars
        
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(latticeConstant / 2, sideLength / 2),
            height=mp.inf,
            material=silMat
        ),
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(-latticeConstant / 2, sideLength / 2),
            height=mp.inf,
            material=silMat
        ),
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(latticeConstant / 2, -sideLength / 2),
            height=mp.inf,
            material=silMat
        ),
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(-latticeConstant / 2, -sideLength / 2),
            height=mp.inf,
            material=silMat
        ),
        
        # Other two
        
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(0, sideLength),
            height=mp.inf,
            material=silMat
        ),
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(0, -sideLength),
            height=mp.inf,
            material=silMat
        ),
    ]

    
    sources = []
        
    # fcen = 1 / latticeConstant #- 2 * rng.random() # pulse center frequency
    # df = 0.5  # pulse freq. width: large df = short impulse

    # s = mp.Source(
    #     src=mp.GaussianSource(fcen, fwidth=df),
    #     component=mp.Ez,
    #     center=mp.Vector3(0, 0, 0),
    # )
    # sources.append(s)
    
    rng = random.default_rng()

    for i in range(numSources):
        
        fcen = 2.2 - 1 * (0.5 - rng.random()) # pulse center frequency
        df = 0.5  # pulse freq. width: large df = short impulse
        
        comp = mp.Hz
        # if((i // 2) * 2 == i):
        #     comp = mp.Hz
        
        s = mp.Source(
            src=mp.GaussianSource(fcen, fwidth=df),
            component=comp,
            center=mp.Vector3(0 + latticeConstant * (0.5 - rng.random()), 0 + latticeConstant * (0.5 - rng.random()), 0),
        )
        sources.append(s)

    # sym = mp.Periodic(direction=mp.Y, phase=-1)

    return mp.Simulation(
        cell_size=cell,
        symmetries=[mp.Mirror(direction = mp.ALL, phase=1)],
        geometry=geometry,
        sources=sources,
        resolution=200,
    )
    
    # 

    kx = False  # if true, do run at specified kx and get fields
    if kx:
        sim.k_point = mp.Vector3(kx)

        sim.run(
            mp.at_beginning(mp.output_epsilon),
            mp.after_sources(mp.Harminv(mp.Hz, mp.Vector3(0.1234), fcen, df)),
            until_after_sources=300,
        )

        sim.run(mp.at_every(1 / fcen / 20, mp.output_hfield_z), until=1 / fcen)

    else:
        k_interp = 19  # # k-points to interpolate, otherwise

        sim.run_k_points(300, mp.interpolate(k_interp, [mp.Vector3(), mp.Vector3(0.5)]))