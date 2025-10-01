#!/bin/bash
#SBATCH -J TableRecreation
#SBATCH --account=gts-mhale30
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH --partition=cpu-medium
#SBATCH --mem=32G
#SBATCH -t 48:00:00
#SBATCH -o table_recreation_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=chawkins64@gatech.edu

# Load required modules
module load anaconda3

# Navigate to project directory
cd /storage/home/hcoda1/7/chawkins64/p-mhale30-0

echo "Starting table recreation experiments..."
echo "Parameters: M=10 streams, mu=±1, thresholds=[1e3,2e3,3e3,4e3,5e3], changepoints=[0,1e3,1e4,1e5]"

# Run EDD experiments for mu=1 (positive mean shift)
echo "=== Running EDD experiments for mu=1 ==="

# EDD with focus_decay for mu=1
echo "Running EDD focus_decay (mu=1)..."
python run_edd_experiments.py \
    --algorithms "focus_decay" \
    --nus "0,1000,10000,100000" \
    --Ms "10" \
    --threshold-min 1000 \
    --threshold-max 5000 \
    --threshold-steps 5 \
    --T 1000000 \
    --mu1 1.0 \
    --sims 500 \
    --workers 24 \
    --save

# Run EDD experiments for mu=-1 (negative mean shift)
echo "=== Running EDD experiments for mu=-1 ==="

# EDD with focus_decay for mu=-1
echo "Running EDD focus_decay (mu=-1)..."
python run_edd_experiments.py \
    --algorithms "focus_decay" \
    --nus "0,1000,10000,100000" \
    --Ms "10" \
    --threshold-min 1000 \
    --threshold-max 5000 \
    --threshold-steps 5 \
    --T 1000000 \
    --mu1 -1.0 \
    --sims 500 \
    --workers 24 \
    --save

echo "Table recreation experiments completed!"
echo "Use the separate table generation script to create tables from the results."