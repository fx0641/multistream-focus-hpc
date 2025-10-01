#!/bin/bash
#SBATCH -J EDD_MultiStreamFocus
#SBATCH --account=gts-mhale30
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH --partition=cpu-medium
#SBATCH --mem=32G
#SBATCH -t 24:00:00
#SBATCH -o edd_multistream_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=chawkins64@gatech.edu

# Load required modules
module load anaconda3

# Navigate to project directory
cd /storage/home/hcoda1/7/chawkins64/p-mhale30-0

# Run EDD experiments
python run_edd_experiments.py \
    --algorithms "focus_decay" \
    --nus "1,1000,10000" \
    --Ms "10,50,100" \
    --threshold-min 1000 \
    --threshold-max 5000 \
    --threshold-steps 5 \
    --T 1000000 \
    --mu1 1.0 \
    --sims 500 \
    --workers 24 \
    --save

echo "EDD experiments completed!"