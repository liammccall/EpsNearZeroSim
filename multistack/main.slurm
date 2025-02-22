#!/bin/bash
#SBATCH -N 1
#SBATCH -c 12
#SBATCH --mem=4G
#SBATCH --mail-user=lkm49@case.edu
#SBATCH --mail-type=END
#SBATCH -o multistack
#SBATCH --job-name="Multistack Sim"
#SBATCH --cpus-per-task=4
#SBATCH --output=multistack.out
envs/enzSim/bin/python3.11 main.py
