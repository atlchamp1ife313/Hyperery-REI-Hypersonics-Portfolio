"""
Hyperery REI (Hypersonics ReImagined)
Atmospheric Optics & Plume Illumination Analysis
Script: Geometric Solar-Depression Limit by Assumed Altitude
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_solar_depression_limits():
    # Data: Assumed altitudes (km) and corresponding maximum solar depression limits (degrees)
    altitudes = ['50 km', '80 km', '100 km', '120 km', '150 km', '200 km']
    max_depression = [7.15, 9.02, 10.12, 11.05, 12.35, 14.18]

    plt.figure(figsize=(9, 6))
    
    # Horizontal bar chart configuration
    bars = plt.barh(altitudes, max_depression, color='#3498db', edgecolor='#2c3e50', alpha=0.85)

    # Styling and Labels
    plt.xlabel('Maximum Solar Depression (degrees)', fontsize=11, fontweight='bold')
    plt.ylabel('Illustrative Altitude', fontsize=11, fontweight='bold')
    plt.title('3. Geometric Solar-Depression Limit by Assumed Altitude', fontsize=13, fontweight='bold', pad=12)
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    
    # Annotate exact values on the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.2, bar.get_y() + bar.get_height()/2, f'{width:.2f}°', 
                 va='center', ha='left', fontsize=10, fontweight='bold', color='#2c3e50')

    plt.xlim(0, 16)
    plt.tight_layout()
    
    # Save figure for technical report inclusion
    plt.savefig('Geometric_Solar_Depression_Limit.png', dpi=300)
    print("--- Hyperery REI Plot Generation Complete ---")
    plt.show()

if __name__ == '__main__':
    plot_solar_depression_limits()
