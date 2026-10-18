import numpy as np

# Simulate altitude array from space down to ground sensor
altitudes = np.linspace(200, 0, 100)
n_0 = 1.0003
H_scale = 8.5

# Compute cumulative horizontal deflection (km) at each altitude layer
deflection = np.zeros_like(altitudes)
for i in range(1, len(altitudes)):
    h = altitudes[i]
    dn_dh = - (n_0 - 1.0) / H_scale * np.exp(-max(h, 0) / H_scale)
    deflection[i] = deflection[i-1] - dn_dh * 15.0

# Maximum positional error at ground level (h = 0)
max_positional_error_km = deflection[-1]
# Apparent angular error (arctan of deflection over altitude span)
angular_error_deg = np.degrees(np.arctan2(max_positional_error_km, 200.0))

print(f"Maximum Ground Positional Offset: {max_positional_error_km:.4f} km")
print(f"Apparent Sensor Angular Error: {angular_error_deg:.4f} degrees")
