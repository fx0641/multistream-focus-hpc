#!/bin/bash
#SBATCH -J ARLTable
#SBATCH --account=gts-mhale30
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH --partition=cpu-medium
#SBATCH --mem=32G
#SBATCH -t 24:00:00
#SBATCH -o arl_table_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=chawkins64@gatech.edu

# Load required modules
module load anaconda3

# Navigate to project directory
cd /storage/home/hcoda1/7/chawkins64/p-mhale30-0

echo "Starting ARL table experiments..."
echo "Parameters: M=[1,3,5,10] streams, thresholds=[log(1e3),log(2e3),log(3e3),log(4e3),log(5e3)]"
echo "ARL measures false alarm rates (no change point, nu=0, mu1=0)"

# Run ARL experiments for different M values with focus_decay
echo "=== Running ARL experiments with focus_decay ==="

# M=1
echo "Running ARL focus_decay (M=1)..."
python run_arl_experiments.py \
    --algorithms "focus_decay" \
    --Ms "1" \
    --thresholds "6.907755,7.600902,8.006368,8.294049,8.517193" \
    --T 1000000 \
    --sims 500 \
    --workers 24 \
    --save

# M=3
echo "Running ARL focus_decay (M=3)..."
python run_arl_experiments.py \
    --algorithms "focus_decay" \
    --Ms "3" \
    --thresholds "6.907755,7.600902,8.006368,8.294049,8.517193" \
    --T 1000000 \
    --sims 500 \
    --workers 24 \
    --save

# M=5
echo "Running ARL focus_decay (M=5)..."
python run_arl_experiments.py \
    --algorithms "focus_decay" \
    --Ms "5" \
    --thresholds "6.907755,7.600902,8.006368,8.294049,8.517193" \
    --T 1000000 \
    --sims 500 \
    --workers 24 \
    --save

# M=10
echo "Running ARL focus_decay (M=10)..."
python run_arl_experiments.py \
    --algorithms "focus_decay" \
    --Ms "10" \
    --thresholds "6.907755,7.600902,8.006368,8.294049,8.517193" \
    --T 1000000 \
    --sims 500 \
    --workers 24 \
    --save

echo "ARL table experiments completed!"
echo "Use the separate ARL table generation script to create tables from the results."