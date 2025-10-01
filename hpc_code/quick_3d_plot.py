#!/usr/bin/env python3
"""
Quick script to generate 3D plot from local data in more_3d_data directory.
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import os

def load_data_from_3d_folder():
    """Load data from hpc_code/more_3d_data directory."""
    data_points = []
    
    # Find all pickle files
    files = glob.glob('hpc_code/more_more_3d/*.pkl')
    print(f"Found {len(files)} data files")
    
    for filepath in files:
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            # Extract info
            M = data['parameters']['M']
            mu1 = data['parameters'].get('mu1', data['metadata'].get('mu1', 1.0))
            nus = data['parameters']['nus']
            thresholds = data['parameters']['thresholds']
            edd_means = data['results']['edd_means']
            
            # Find nu=500 index
            nu_idx = 0  # Should be first since we only ran nu=500
            for i, nu in enumerate(nus):
                if abs(nu - 500) < 1:
                    nu_idx = i
                    break
            
            # Use middle threshold (index 5 out of 10)
            threshold_idx = 5
            edd_value = edd_means[nu_idx, threshold_idx]
            threshold_value = thresholds[threshold_idx]
            
            # Include all mu1 values (both positive and negative)
            data_points.append({
                'M': M,
                'mu1': mu1, 
                'edd': edd_value,
                'threshold': threshold_value
            })
            
            print(f"  M={M}, mu1={mu1:.2f}, EDD={edd_value:.1f}")
            
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
    
    return data_points

def create_3d_surface_plot(data_points):
    """Create 3D surface plot."""
    if not data_points:
        print("No data points to plot!")
        return
    
    # Extract coordinates
    M_values = np.array([d['M'] for d in data_points])
    mu1_values = np.array([d['mu1'] for d in data_points])
    edd_values = np.array([d['edd'] for d in data_points])
    
    print(f"\nPlotting {len(data_points)} data points")
    print(f"M range: {min(M_values)} - {max(M_values)}")
    print(f"mu1 range: {min(mu1_values):.1f} - {max(mu1_values):.1f}")
    print(f"EDD range: {min(edd_values):.1f} - {max(edd_values):.1f}")
    
    # Get unique values for grid
    M_unique = np.unique(M_values)
    mu1_unique = np.unique(mu1_values)
    
    print(f"Unique M values: {M_unique}")
    print(f"Unique mu1 values: {sorted(mu1_unique)}")
    print(f"Expected mu1 values: [-2.0, -1.5, -1.0, -0.5, -0.25, -0.1, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0]")
    
    # Create meshgrid
    M_grid, mu1_grid = np.meshgrid(M_unique, mu1_unique)
    edd_grid = np.full(M_grid.shape, np.nan)
    
    # Fill in the grid with EDD values
    for d in data_points:
        i = np.where(mu1_unique == d['mu1'])[0][0]
        j = np.where(M_unique == d['M'])[0][0]
        edd_grid[i, j] = d['edd']
    
    print(f"Grid shape: {edd_grid.shape}")
    print(f"Non-NaN values: {np.sum(~np.isnan(edd_grid))}")
    
    # Create 3D plot
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create surface plot
    surface = ax.plot_surface(M_grid, mu1_grid, edd_grid, 
                             cmap='viridis', alpha=0.8, 
                             linewidth=0.5, edgecolors='black')
    
    # Also add scatter points for clarity
    scatter = ax.scatter(M_values, mu1_values, edd_values, 
                        c=edd_values, cmap='viridis', 
                        s=60, alpha=1.0, edgecolors='red', linewidth=1)
    
    # Labels and title
    ax.set_xlabel('Number of Streams (M)', fontsize=12)
    ax.set_ylabel('Mean Shift (mu1)', fontsize=12)
    ax.set_zlabel('Expected Detection Delay (EDD)', fontsize=12)
    
    threshold_val = data_points[0]['threshold']
    ax.set_title(f'Focus Decay Algorithm: EDD Surface (Symmetric)\n'
                f'(nu=500, lambda={threshold_val:.1f})', fontsize=14)
    
    # Add colorbar
    cbar = plt.colorbar(surface, ax=ax, shrink=0.6, aspect=30)
    cbar.set_label('Expected Detection Delay', fontsize=11)
    
    # Improve viewing angle
    ax.view_init(elev=25, azim=45)
    
    # Set better tick spacing
    ax.set_xticks(M_unique)
    ax.set_yticks(mu1_unique[::2])  # Every other mu1 value to avoid crowding
    
    plt.tight_layout()
    
    # Save plot
    os.makedirs('3d_plots', exist_ok=True)
    plt.savefig('3d_plots/edd_3d_surface.png', dpi=300, bbox_inches='tight')
    print(f"\nSaved surface plot to: 3d_plots/edd_3d_surface.png")
    
    # Show plot
    plt.show()
    
    return fig

def main():
    print("=== Quick 3D EDD Plot Generation ===")
    
    # Load data
    data_points = load_data_from_3d_folder()
    
    if not data_points:
        print("No data found! Check that files are in hpc_code/more_3d_data/")
        return
    
    # Create surface plot
    create_3d_surface_plot(data_points)

if __name__ == "__main__":
    main()