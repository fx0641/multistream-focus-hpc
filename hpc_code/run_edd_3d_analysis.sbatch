#!/bin/bash
#SBATCH -J EDD_3D_Analysis
#SBATCH --account=gts-mhale30
#SBATCH -N 1
#SBATCH --ntasks-per-node=24
#SBATCH --partition=cpu-medium
#SBATCH --mem=32G
#SBATCH -t 24:00:00
#SBATCH -o edd_3d_analysis_%j.out
#SBATCH --mail-type=ALL
#SBATCH --mail-user=chawkins64@gatech.edu


echo "=== EDD 3D Analysis Experiments ==="
echo "Job ID: $SLURM_JOB_ID"
echo "Start time: $(date)"
echo "Running on node: $(hostname)"

# Load any necessary modules
# module load python/3.8  # Uncomment if needed

# Configuration
FIXED_NU=500  # Fixed change point
THRESHOLDS="5.0-12.0"
THRESHOLD_STEPS=10
TIME_HORIZON=1000000
SIMS=500
WORKERS=24
ALGORITHM="focus_decay"

# Multiple M values (number of streams)
M_VALUES="10,25,50,100,200"

# Multiple mean shift values
MU_VALUES='-2.0,-1.5,-1.0,-0.5,0.5,1.0,1.5,2.0'

# Data directory
DATA_DIR="edd_3d_data"

echo "Configuration:"
echo "  Fixed nu (change point): $FIXED_NU"
echo "  M values (streams): $M_VALUES"
echo "  Mu values (mean shifts): $MU_VALUES"
echo "  Thresholds: $THRESHOLDS"
echo "  Algorithm: $ALGORITHM"
echo "  Simulations: $SIMS"
echo "  Data directory: $DATA_DIR"
echo ""

# Create data directory
mkdir -p $DATA_DIR

echo "=== Running EDD experiments for 3D analysis ==="

# Run EDD experiments
echo "Starting EDD experiments..."
python run_edd_experiments.py \
    --algorithms "$ALGORITHM" \
    --nus "$FIXED_NU" \
    --Ms "$M_VALUES" \
    --threshold-min 5.0 \
    --threshold-max 12.0 \
    --threshold-steps $THRESHOLD_STEPS \
    --T $TIME_HORIZON \
    --mu1-values '$MU_VALUES' \
    --sims $SIMS \
    --workers $WORKERS \
    --data-dir "$DATA_DIR" \
    --save

echo ""
echo "=== Experiments completed ==="
echo "End time: $(date)"
echo "Data saved in: $DATA_DIR"
echo ""
echo "Next steps:"
echo "1. Check the generated data files in $DATA_DIR/"
echo "2. Run: python create_edd_3d_plot.py --data-dir $DATA_DIR"
echo "3. Generated plots will be saved in edd_3d_plots/"