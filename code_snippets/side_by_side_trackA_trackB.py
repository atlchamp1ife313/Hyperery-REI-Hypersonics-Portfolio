import pandas as pd
import matplotlib.pyplot as plt

# Load coupled data
df = pd.read_csv('dual_track_coupled_kinetics_output.csv')

# Create side-by-side comparative plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Track A: Particulate Dispersion
ax1.plot(df['Downrange_km'], df['TrackA_Baseline_Particulate_kg_m3'] * 1e6, label='Baseline Particulate', color='tab:blue', linewidth=2)
ax1.plot(df['Downrange_km'], df['TrackA_Quenched_Particulate_kg_m3'] * 1e6, label='Quenched Particulate', color='tab:orange', linewidth=2, linestyle='--')
ax1.set_title('Track A: Particulate Dispersion Density')
ax1.set_xlabel('Downrange Distance (km)')
ax1.set_ylabel('Concentration ($\mu g / m^3$)')
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend()

# Track B: Sensor Lock-Loss Range
ax2.plot(df['Downrange_km'], df['TrackB_Baseline_LockRange_km'], label='Baseline Lock-Loss Range', color='tab:red', linewidth=2)
ax2.plot(df['Downrange_km'], df['TrackB_Quenched_LockRange_km'], label='Quenched Lock-Loss Range', color='tab:green', linewidth=2, linestyle='--')
ax2.set_title('Track B: Ground Sensor Lock-Loss Distance')
ax2.set_xlabel('Downrange Distance (km)')
ax2.set_ylabel('Lock Range (km)')
ax2.grid(True, linestyle=':', alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig('dual_track_side_by_side_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("Side-by-side comparative plots generated successfully.")
