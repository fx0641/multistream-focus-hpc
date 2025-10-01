#!/usr/bin/env python3
"""
Simple script to generate EDD tables from experimental results.
Prints tables to console and optionally saves to CSV/LaTeX.
"""

import pickle
import numpy as np
import glob
import os
from datetime import datetime

def load_pickle_data(filepath):
    """Load data from pickle file."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def extract_edd_data(data, nu_target):
    """Extract EDD data for specific change point."""
    thresholds = data['parameters']['thresholds']
    nus = data['parameters']['nus']
    edd_means = data['results']['edd_means']
    
    # Find the index for the target nu
    try:
        nu_idx = list(nus).index(nu_target)
    except ValueError:
        print(f"Warning: nu={nu_target} not found in {nus}")
        return None, None
    
    # Extract data for the specific change point
    edd_vals = edd_means[nu_idx, :]  # nu_idx row, all thresholds
    
    return thresholds, edd_vals

def find_focus_decay_files(mu_value):
    """Find focus_decay EDD files for given mu value."""
    # Look for files with the pattern
    patterns = [
        f"edd_focus_decay*M10*mu{abs(mu_value):.1f}*.pkl",
        f"edd_focus_decay*M10*mu{int(abs(mu_value))}*.pkl"
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))
    
    return files

def print_edd_table(mu_value, data_dict, title_suffix=""):
    """Print EDD table for given mu value."""
    print(f"\nTable: Expected Detection Delay (μ={mu_value}){title_suffix}")
    print(f"{'λ':<8} {'ν=0':<10} {'ν=1e3':<10} {'ν=1e4':<10} {'ν=1e5':<10}")
    print("-" * 55)
    
    # Standard lambda values from the tables
    lambda_values = [1000, 2000, 3000, 4000, 5000]
    nu_values = [0, 1000, 10000, 100000]
    
    for lambda_val in lambda_values:
        row = f"{int(lambda_val/1000)}e3"
        row = f"{row:<8}"
        
        for nu in nu_values:
            if nu in data_dict and lambda_val in data_dict[nu]:
                edd_val = data_dict[nu][lambda_val]
                if not np.isnan(edd_val):
                    row += f" {edd_val:<9.1f}"
                else:
                    row += f" {'N/A':<9}"
            else:
                row += f" {'N/A':<9}"
        
        print(row)

def print_ratio_table(mu_value, data_dict, title_suffix=""):
    """Print ratio table (EDD / theoretical_EDD) for given mu value."""
    print(f"\nTable: EDD Ratio to Theoretical (2λ/μ²) (μ={mu_value}){title_suffix}")
    print(f"{'λ':<8} {'ν=0':<10} {'ν=1e3':<10} {'ν=1e4':<10} {'ν=1e5':<10}")
    print("-" * 55)
    
    # Standard lambda values from the tables
    lambda_values = [1000, 2000, 3000, 4000, 5000]
    nu_values = [0, 1000, 10000, 100000]
    
    for lambda_val in lambda_values:
        row = f"{int(lambda_val/1000)}e3"
        row = f"{row:<8}"
        
        theoretical_edd = 2 * lambda_val / (mu_value**2)
        
        for nu in nu_values:
            if nu in data_dict and lambda_val in data_dict[nu]:
                edd_val = data_dict[nu][lambda_val]
                if not np.isnan(edd_val):
                    ratio = edd_val / theoretical_edd
                    row += f" {ratio:<9.3f}"
                else:
                    row += f" {'N/A':<9}"
            else:
                row += f" {'N/A':<9}"
        
        print(row)

def main():
    print("EDD Table Generation for Focus Decay Algorithm")
    print("=" * 50)
    
    mu_values = [1.0, -1.0]
    
    for mu in mu_values:
        print(f"\n{'='*20} μ = {mu} {'='*20}")
        
        # Find relevant files
        files = find_focus_decay_files(mu)
        
        if not files:
            print(f"No focus_decay files found for μ={mu}")
            continue
        
        print(f"Found {len(files)} files:")
        for f in files:
            print(f"  {f}")
        
        # Load and process the most recent file
        latest_file = max(files, key=os.path.getctime)
        print(f"\nUsing: {latest_file}")
        
        try:
            data = load_pickle_data(latest_file)
            
            # Extract data for each nu value
            data_dict = {}
            nu_values = [0, 1000, 10000, 100000]
            
            for nu in nu_values:
                thresholds, edd_vals = extract_edd_data(data, nu)
                if thresholds is not None:
                    data_dict[nu] = {}
                    for i, threshold in enumerate(thresholds):
                        data_dict[nu][threshold] = edd_vals[i]
            
            # Print the tables
            print_edd_table(mu, data_dict)
            print_ratio_table(mu, data_dict)
            
        except Exception as e:
            print(f"Error processing {latest_file}: {e}")
            continue
    
    print("\n" + "="*50)
    print("Table generation completed!")

if __name__ == "__main__":
    main()