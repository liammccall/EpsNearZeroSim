#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=100G
#SBATCH --time=1-12:00:00
#SBATCH --mail-user=lkm49@case.edu
#SBATCH --mail-type=END
#SBATCH --job-name="Multistack Sim"
#SBATCH --cpus-per-task=24
#SBATCH --output=multistack.out
module load OpenMPI
mpirun -np 24 --bind-to none --oversubscribe ~/.conda/envs/enzSim/bin/python3.11 main.py
