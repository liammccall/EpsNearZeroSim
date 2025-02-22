import numpy as np
import multifunction
import matplotlib.pyplot as plt
import io
import sys
import multiprocessing
import argparse
import os

def setup_stdout(thread_id):
    """Redirects stdout to a file for each thread."""
    os.makedirs("out", exist_ok=True)
    sys.stdout = open(f"out/thread{thread_id}.out", "w")

#deprecate
def nostdout(func):
    """Decorator to suppress standard output."""
    def wrapper(*args, **kwargs):
        save_stdout = sys.stdout
        sys.stdout = io.StringIO()
        result = func(*args, **kwargs)
        sys.stdout = save_stdout
        return result
    return wrapper

# @nostdout
def compute_ldos(dist, geometry, thread_id):
    print(dist)
    return multifunction.multi(dist, "plots/{dist}_Ex_{thread_id}.mp4", emptyspace=geometry)

def worker_process(args):
    thread_id, distances = args
    setup_stdout(thread_id)
    return [compute_ldos(dist[0], dist[1], thread_id) for dist in distances]

def main(k):
    start = 1
    end = 10
    res = [50, 10, 10, 10]
    
    distances = []
    points = np.linspace(start, end, len(res) + 1)
    
    for idx, point in enumerate(points[:-1]):
        distances.extend(np.linspace(point, points[idx + 1], res[idx]))

    distances = [[x, False] for x in distances]
    distances.append([0, True])
        
    distances_split = np.array_split(distances, k)
    
    with multiprocessing.Pool(k) as pool:
        results = pool.map(worker_process, enumerate(distances_split))
    
    def flatten(arr):
        return [x for xs in arr for x in xs]
    
    flatldos = flatten(results)
    print(flatldos)
    ldos = flatldos[:-1]
    baseline = flatldos[-1]
    distances = flatten(distances_split)[:-1]
    
    fig, ax = plt.subplots()
    ax.plot(distances, np.divide(ldos, baseline))
    fig.savefig("ldos.png")
    
    np.save("bin/ldos", ldos)
    np.save("bin/distances", distances)
    print(ldos)
    print(distances)
    
if __name__ == "__main__":
    total_processes = 8
    sim_processes = 2
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", type=int, default=total_processes, help="Number of processes total")
    # parser.add_argument("-n", type=int, default=sim_processes, help="Number of processes per simulation (ideally total_processes mod sim_processes = 0)")
    args = parser.parse_args()
    try:
        processes = int(args.k)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid value for -k: '{args.k}'. Must be an integer.")
    
    main(processes)
