#!/bin/bash
#SBATCH -t 6:00:00
#SBATCH -A cral
#SBATCH --partition=gpu
#SBATCH --gres=gpu:a100:1
#SBATCH --ntasks=1
#SBATCH -o out.txt

module purge
module load cuda apptainer pytorch
module load anaconda

# /scratch/bjb3az/.conda/envs/habitat/bin/python mcq.py
# /scratch/bjb3az/.conda/envs/habitat/bin/python yes_no.py
/scratch/bjb3az/.conda/envs/habitat/bin/python yes_no_candidates.py