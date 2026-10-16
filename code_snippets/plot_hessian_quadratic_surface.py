"""
Hyperery REI (Hypersonics ReImagined)
CFD Mesh Adaptation & Curvature Analysis
Script: Quadratic Surface Defined by Symmetric Hessian Tensor
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_hessian_surface():
    # Define spatial grid domain
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)

    # Define Hessian Matrix H = [[2, 3], [3, 4]]
    # f(x, y) = 0.5 * (H11*X^2 + 2*H12*X*Y + H22*Y^2)
    H11, H12, H22 = 2.0, 3.0, 4.0
    Z = 0.5 * (H11 * X**2 + 2 * H12 * X * Y + H22 * Y**2)

    # Create 3D Surface Plot
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)

    # Colorbar configuration
    cbar = fig.colorbar(surf, ax=ax, shrink=0.6, aspect=15, pad=0.1)
    cbar.set_label('f(x, y)', fontsize=10)

    # Labels and Title
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.set_zlabel('f(x, y)', fontsize=11, fontweight='bold')
    ax.set_title(r'Quadratic Surface Defined by Hessian $H = [[2, 3], [3, 4]]$', fontsize=12, pad=15)

    plt.tight_layout()
    plt.savefig('Hessian_Quadratic_Surface.png', dpi=300)
    print("--- Hyperery REI Hessian Surface Plot Generated Successfully ---")
    plt.show()

if __name__ == '__main__':
    plot_hessian_surface()
