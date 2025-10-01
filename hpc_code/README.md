# Multi-Stream Change Point Detection - HPC Code

Quick guide for running experiments on the HPC cluster.

## Running ARL Experiments

ARL (Average Run Length) measures false alarm rates when there's no changepoint.

**Example:**
```bash
python run_arl_experiments.py \
    --algorithms "focus_decay" \
    --Ms "10,25,50,100" \
    --threshold-min 5.0 \
    --threshold-max 12.0 \
    --threshold-steps 10 \
    --T 1000000 \
    --sims 500 \
    --workers 24 \
    --save
```

**On SLURM:**
```bash
sbatch run_arl_slurm.sbatch
```

## Running EDD Experiments

EDD (Expected Detection Delay) measures how fast we detect actual changepoints.

**Example:**
```bash
python run_edd_experiments.py \
    --algorithms "focus_decay" \
    --nus "500" \
    --Ms "10,25,50,100" \
    --threshold-min 5.0 \
    --threshold-max 12.0 \
    --threshold-steps 10 \
    --T 1000000 \
    --mu1 1.0 \
    --sims 500 \
    --workers 24 \
    --save
```

**On SLURM:**
```bash
sbatch run_edd_slurm.sbatch
```

## Generating Tables

After running experiments, generate LaTeX tables:

```bash
python generate_arl_table.py --data-dir data/
python generate_edd_tables.py --data-dir data/
```

## Making 3D Plots

For visualizing EDD across different M and mu1 values:

```bash
python quick_3d_plot.py
```

## Key Parameters

- `--Ms`: Number of streams (e.g., "10,25,50,100")
- `--nus`: Changepoint location (use "500" for EDD)
- `--mu1`: Post-change mean shift (try 1.0 or -1.0)
- `--threshold-min/max`: Range of detection thresholds
- `--sims`: Number of Monte Carlo simulations
- `--workers`: Number of parallel workers

## Output

Results are saved as `.pkl` files in the `data/` directory with timestamps.
