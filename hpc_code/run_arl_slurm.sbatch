#!/bin/bash
#SBATCH -J ARL_MultiStreamFocus
#SBATCH --account=gts-mhale30
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH --partition=cpu-medium
#SBATCH --mem=32G
#SBATCH -t 24:00:00
#SBATCH -o arl_multistream_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=chawkins64@gatech.edu

# Load required modules
module load anaconda3

# Navigate to project directory
cd /storage/home/hcoda1/7/chawkins64/p-mhale30-0

# Run ARL experiments with M=100 streams

echo "Running focus_decay..."
python run_arl_experiments.py \
    --algorithms "focus_decay" \
    --Ms "100" \
    --threshold-min 5 \
    --threshold-max 12 \
    --threshold-steps 10 \
    --T 1000000 \
    --sims 500 \
    --workers 24 \
    --save

echo "ARL experiments completed!"