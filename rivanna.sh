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

/scratch/bjb3az/.conda/envs/habitat/bin/python run.py
