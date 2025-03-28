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
from git import Repo

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

def compute_ldos(dist, geometry, thread_id):
    print(dist)
    distString = str(dist).replace(".", "")
    return multifunction.multi(dist, f"plots/{distString}_E_{thread_id}", returnval="EField", emptyspace=geometry)

def worker_process(distances, rank):
    """Worker function executed by each MPI process."""
    return [compute_ldos(dist[0], dist[1], rank) for dist in distances]

def git_push(repo_loc, message):
    try:
        repo = Repo(repo_loc)
        repo.git.add(update=True)
        repo.index.commit(message)
        origin = repo.remote(name='origin')
        origin.push()
    except:
        print('Some error occured while pushing the code')

def main():
    start = 5
    end = 30
    res = [3, 1, 1]
    
    distances = []
    points = np.linspace(start, end, len(res) + 1)
    
    for idx, point in enumerate(points[:-1]):
        distances.extend(np.linspace(point, points[idx + 1], res[idx])[:-1])

    distances.append(end)
    
    distances = [[x, False] for x in distances]
    distances.append([0, True])
    
    results = [compute_ldos(dist[0], dist[1], 0) for dist in distances]
        
    # def flatten(arr):
    #     return [x for xl in arr for x in xl]
    
    # print(results)
    
    # flatldos = flatten(results)
    # flatldos = flatten(results)
    ldos = results[:-1]
    baseline = results[-1]
    distances = [pair[0] for pair in distances[:-1]]
    
    print(results)
    print(distances)

    fig, ax = plt.subplots()
    ax.plot(distances, np.divide(ldos, baseline))
    fig.savefig("nret.png")

    os.makedirs("bin", exist_ok=True)
    np.save("bin/nret", ldos)
    np.save("bin/distances", distances)
    print(ldos)
    print(distances)

if __name__ == "__main__":
    main()
