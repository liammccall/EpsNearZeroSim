import numpy as np
import multifunction
import matplotlib.pyplot as plt
import io
import sys
import multiprocessing
import argparse
import os
from mpi4py import MPI
import numpy as np
import os
import sys

og_std = sys.stdout

def setup_stdout(thread_id):
    """Redirects stdout to a file for each thread."""
    os.makedirs("out", exist_ok=True)
    og_std = sys.stdout
    sys.stdout = open(f"out/thread{thread_id}.out", "w")

def reset_stdout():
    """Back to main stdout."""
    sys.stdout.close
    sys.stdout = og_std
    
def setup_stdout(thread_id):
    """Redirects stdout to a file for each thread."""
    os.makedirs("out", exist_ok=True)
    sys.stdout = open(f"out/thread{thread_id}.out", "w")

def compute_ldos(dist, angle, geometry, thread_id):
    print(f"{dist} nm from emitter at {angle} degrees")
    return multifunction.multi(dist, f"plots/{dist}_E_{thread_id}.mp4", returnval="LDOS", emptyspace=geometry, rot_angle=angle)

def worker_process(distances, rank):
    """Worker function executed by each MPI process."""
    return [compute_ldos(dist[0], dist[1], dist[2], rank) for dist in distances]

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    start = 50
    end = 100
    res = [1]#[20, 10, 5, 5]
    num_angles = 10
    
    distances = []
    points = np.linspace(start, end, len(res) + 1)
    
    for idx, point in enumerate(points[:-1]):
        distances.extend(np.linspace(point, points[idx + 1], res[idx])[:-1])

    distances.append(end)
    
    angle_sample = np.arange(0, 360, num_angles / 360)
    
    distances = [[x, angle, False] for x in distances for angle in angle_sample]
    distances.append([0, 0, True])

    # Distribute distances across MPI ranks
    distances_split = np.array_split(distances, size)[rank]
    
    print(rank)
    setup_stdout(rank)
    
    print(rank)
    print("um")
    print(distances_split)

    # Each MPI process runs its own worker function
    procs = worker_process(distances_split, rank)

    if rank == 0:

        # Gather results at rank 0
        results = comm.gather(procs, root=0)
        print("gathered")
        
        reset_stdout()
        
        def flatten(arr):
            return [x for xl in arr for x in xl]
        
        # print(results)
        
        # flatldos = flatten(results)
        flatldos = flatten(results)
        ldos = flatldos[:-1]
        baseline = flatldos[-1]
        distances = [dist[0] for dist in distances[:-1]]
        
        print(flatldos)
        print(distances)

        fig, ax = plt.subplots()
        ax.plot(distances, np.divide(ldos, baseline))
        fig.savefig("ldos.png")

        os.makedirs("bin", exist_ok=True)
        np.save("bin/ldos", ldos)
        np.save("bin/distances", distances)
        print(ldos)
        print(distances)

if __name__ == "__main__":
    main()
