#!/bin/bash
#SBATCH -N 1
#SBATCH --mem=100G
#SBATCH --time=00:05:00
#SBATCH --mail-user=lkm49@case.edu
#SBATCH --mail-type=END
#SBATCH --job-name="Multistack Sim"
#SBATCH --cpus-per-task=24
#SBATCH --output=multistack.out
envs/enzSim/bin/python3.11 main.py -k 24
