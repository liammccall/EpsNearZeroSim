import meep as mp
from meep import mpb
import math
import numpy as np

def create2DHexSolver(silMat, latticeConstant):

    rPillar = latticeConstant * ((1/3) - (1/30))

    geometry_lattice = mp.Lattice(
        size=latticeConstant * mp.Vector3(1, 1),
        basis1=latticeConstant * mp.Vector3(math.sqrt(3) / 2, 0.5),
        basis2=latticeConstant * mp.Vector3(math.sqrt(3) / 2, -0.5),
    )

    # Two rods per unit cell, at the correct positions to form a honeycomb
    # lattice, and arranged to have inversion symmetry:
    geometry = [
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(1 / 6, 1 / 6),
            height=mp.inf,
            material=silMat
        ),
        mp.Cylinder(
            rPillar,
            center=latticeConstant * mp.Vector3(1 / -6, 1 / -6),
            height=mp.inf,
            material=silMat,
        ),
    ]

    # The k_points list, for the Brillouin zone of a triangular lattice:
    k_points = [
        latticeConstant * mp.Vector3(y=0.5),  # M
        latticeConstant * mp.Vector3(),  # Gamma
        latticeConstant * mp.Vector3(1 / -3, 1 / 3),  # K
    ]

    k_interp = 60  # number of k_points to interpolate
    k_points = mp.interpolate(k_interp, k_points)
    
    # np.mgrid[-0.5:0.5:0.05, -0.5:0.5:0.05]

    resolution = 32
    num_bands = 8

    return mpb.ModeSolver(
        geometry_lattice=geometry_lattice,
        geometry=geometry,
        k_points=k_points,
        resolution=resolution,
        num_bands=num_bands,
    )
    
def create3dHexSim(silMat, latticeConstant, widths : tuple[float, float]):

    rPillar = latticeConstant * ((1/3) - (1/30))

    geometry_lattice = mp.Lattice(
        size=latticeConstant * mp.Vector3(1, 1),
        basis1=latticeConstant * mp.Vector3(math.sqrt(3) / 2, 0.5),
        basis2=latticeConstant * mp.Vector3(math.sqrt(3) / 2, -0.5),
    )

    # Two rods per unit cell, at the correct positions to form a honeycomb
    # lattice, and arranged to have inversion symmetry:
    geometry = [
        mp.Cylinder(
            rPillar,
            center=mp.Vector3(1 / 6, 1 / 6),
            height=widths[1],
            material=silMat
        ),
        mp.Cylinder(
            rPillar,
            center=latticeConstant * mp.Vector3(1 / -6, 1 / -6),
            height=widths[1],
            material=silMat,
        ),
    ]

    # The k_points list, for the Brillouin zone of a triangular lattice:
    k_points = [
        latticeConstant * mp.Vector3(y=0.5),  # M
        latticeConstant * mp.Vector3(),  # Gamma
        latticeConstant * mp.Vector3(1 / -3, 1 / 3),  # K
    ]

    k_interp = 60  # number of k_points to interpolate
    k_points = mp.interpolate(k_interp, k_points)
    
    # np.mgrid[-0.5:0.5:0.05, -0.5:0.5:0.05]

    resolution = 32
    num_bands = 8

    return mpb.ModeSolver(
        geometry_lattice=geometry_lattice,
        geometry=geometry,
        k_points=k_points,
        resolution=resolution,
        num_bands=num_bands,
    )

