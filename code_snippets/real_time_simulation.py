import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Real-Time Simulation Setup ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

frames = 30
downrange = np.linspace(0, 800, 80)
altitude = 66.2 * (1 - np.exp(-downrange / 150.0))

# Subplot 1: Radiance Decay
ax1.set_xlim(0, 800)
ax1.set_ylim(0, 500)
ax1.set_xlabel('Downrange Distance (km)')
ax1.set_ylabel('Radiance (W/sr*m^2)')
ax1.set_title('Real-Time Plume Quenching ("Stealth Cliff")', fontsize=11, fontweight='bold')
ax1.grid(True, linestyle='--', alpha=0.5)

line_baseline, = ax1.plot([], [], color='orange', lw=2.5, label='Baseline Plume')
line_quenched, = ax1.plot([], [], color='blue', lw=2.5, label='Mitigated (Quenched) Plume')
ax1.legend(loc='upper right')

# Subplot 2: Ray-Tracing Wavefront Bending
ax2.set_xlim(-0.1, 0.1)
ax2.set_ylim(0, 200)
ax2.set_xlabel('Wavefront Deflection (km)')
ax2.set_ylabel('Altitude (km)')
ax2.set_title('Real-Time Atmospheric Ray Bending ($\\nabla n$)', fontsize=11, fontweight='bold')
ax2.grid(True, linestyle='--', alpha=0.5)

ray_line, = ax2.plot([], [], color='red', lw=2.5, label='Refracted Photon Path')
vacuum_line, = ax2.plot([0, 0], [0, 200], color='gray', linestyle='--', lw=1.5, label='Vacuum Line')
ax2.legend(loc='upper left')

baseline_rad = 450 * np.exp(-downrange / 250.0)

def animate(i):
    progress = (i + 1) / frames
    current_idx = int(progress * len(downrange))
    current_idx = max(current_idx, 1)
    
    quenched_rad = baseline_rad[:current_idx] * np.exp(-downrange[:current_idx] / 20.0) * 0.05
    
    line_baseline.set_data(downrange[:current_idx], baseline_rad[:current_idx])
    line_quenched.set_data(downrange[:current_idx], quenched_rad)
    
    z_sub = np.linspace(200, 200 - (200 * progress), 50)
    if len(z_sub) > 1:
        deflection_sub = 0.0025 * (200 - z_sub) / 200.0
        ray_line.set_data(deflection_sub, z_sub)
    
    return line_baseline, line_quenched, ray_line

ani = animation.FuncAnimation(fig, animate, frames=frames, interval=100, blit=True)
ani.save('real_time_simulation.gif', writer='pillow', fps=15)
plt.show()
print("📁 Saved real-time simulation GIF as: real_time_simulation.gif")
