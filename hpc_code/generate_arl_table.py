#!/usr/bin/env python3
"""
Simple script to generate ARL table from experimental results.
Prints table to console and optionally saves to CSV/LaTeX.
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

def find_arl_files():
    """Find ARL focus_decay files."""
    import os
    
    # Try multiple possible locations
    possible_dirs = [
        "arl_table_data",
        "hpc_code/arl_table_data", 
        "./arl_table_data",
        "../arl_table_data"
    ]
    
    files = []
    for data_dir in possible_dirs:
        if os.path.exists(data_dir):
            patterns = [
                f"{data_dir}/arl_focus_decay_M*.pkl",
                f"{data_dir}/arl_focus_decay*.pkl"
            ]
            
            for pattern in patterns:
                files.extend(glob.glob(pattern))
            
            if files:  # If we found files, break
                break
    
    return files

def extract_arl_data(data):
    """Extract ARL data from the pickle file."""
    Ms = data['parameters']['Ms']
    thresholds = data['parameters']['thresholds']
    arl_means = data['results']['arl_means']
    
    return Ms, thresholds, arl_means

def print_arl_table(arl_data_dict):
    """Print ARL table in the format shown."""
    print(f"\nTable: Average Run Lengths")
    print(f"{'λ':<12} {'M = 1':<12} {'M = 3':<12} {'M = 5':<12} {'M = 10':<12}")
    print("-" * 65)
    
    # Standard lambda values (log thresholds)
    # log(1000) ≈ 6.907755, log(2000) ≈ 7.600902, etc.
    lambda_values = [np.log(1000), np.log(2000), np.log(3000), np.log(4000), np.log(5000)]
    lambda_labels = ["log(1e3)", "log(2e3)", "log(3e3)", "log(4e3)", "log(5e3)"]
    M_values = [1, 3, 5, 10]
    
    for i, lambda_val in enumerate(lambda_values):
        lambda_str = lambda_labels[i]
        row = f"{lambda_str:<12}"
        
        for M in M_values:
            # Find the closest threshold value in the data
            if M in arl_data_dict:
                # Find the closest threshold to lambda_val
                closest_threshold = None
                min_diff = float('inf')
                for threshold in arl_data_dict[M].keys():
                    diff = abs(threshold - lambda_val)
                    if diff < min_diff:
                        min_diff = diff
                        closest_threshold = threshold
                
                if closest_threshold is not None and min_diff < 0.1:  # Allow small tolerance
                    arl_val = arl_data_dict[M][closest_threshold]
                    if not np.isnan(arl_val):
                        row += f" {arl_val:<11.2f}"
                    else:
                        row += f" {'N/A':<11}"
                else:
                    row += f" {'N/A':<11}"
            else:
                row += f" {'N/A':<11}"
        
        print(row)

def main():
    print("ARL Table Generation for Focus Decay Algorithm")
    print("=" * 50)
    
    # Debug: show current working directory
    import os
    print(f"Current working directory: {os.getcwd()}")
    print(f"Looking for files in: hpc_code/arl_table_data/")
    
    # Check if directory exists
    if os.path.exists("hpc_code/arl_table_data"):
        print("✓ Directory hpc_code/arl_table_data exists")
        files_in_dir = os.listdir("hpc_code/arl_table_data")
        print(f"Files in directory: {files_in_dir}")
    else:
        print("✗ Directory hpc_code/arl_table_data not found")
    
    # Find all ARL files
    files = find_arl_files()
    
    if not files:
        print("No ARL files found!")
        return
    
    print(f"Found {len(files)} ARL files:")
    for f in files:
        print(f"  {f}")
    
    # Group files by M value and find the most recent for each M
    arl_data_dict = {}  # M -> {threshold: arl_value}
    
    for file in files:
        try:
            data = load_pickle_data(file)
            Ms, thresholds, arl_means = extract_arl_data(data)
            
            print(f"\nProcessing: {file}")
            print(f"  Ms: {Ms}")
            print(f"  Thresholds: {thresholds}")
            print(f"  ARL means shape: {arl_means.shape}")
            
            # Process each M value in this file
            for i, M in enumerate(Ms):
                if M not in arl_data_dict:
                    arl_data_dict[M] = {}
                
                # Extract ARL values for this M
                if len(arl_means.shape) == 2:
                    arl_vals = arl_means[i, :]  # i-th M, all thresholds
                else:
                    arl_vals = arl_means  # Single M case
                
                # Store threshold -> ARL mapping
                for j, threshold in enumerate(thresholds):
                    arl_data_dict[M][threshold] = arl_vals[j]
                
                print(f"  M={M}: {len(thresholds)} thresholds processed")
        
        except Exception as e:
            print(f"Error processing {file}: {e}")
            continue
    
    # Print the ARL table
    if arl_data_dict:
        print_arl_table(arl_data_dict)
    else:
        print("No valid ARL data found!")
    
    print("\n" + "="*50)
    print("ARL table generation completed!")

if __name__ == "__main__":
    main()