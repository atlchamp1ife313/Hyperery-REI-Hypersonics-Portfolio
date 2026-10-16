"""
Hyperery REI (Hypersonics ReImagined)
Onboard Sensor Telemetry & Extended Kalman Filter (EKF) Fusion Module
Fuses IR optical tracking data with inertial telemetry for real-time state estimation.
"""

import numpy as np

class PlumeStateEKF:
    def __init__(self):
        # State vector: [Position X, Position Y, Altitude Z, Velocity Z]
        self.x = np.array([0.0, 0.0, 2.0, 100.0])
        
        # State covariance matrix
        self.P = np.eye(4) * 10.0
        
        # Process noise covariance
        self.Q = np.eye(4) * 0.1
        
        # Measurement noise covariance (IR sensor noise)
        self.R = np.eye(2) * 1.5

    def predict(self, dt):
        """Predict step using simple constant-velocity kinematic model."""
        # State transition matrix F
        F = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, dt],
            [0, 0, 0, 1]
        ])
        
        # Predict state
        self.x = F @ self.x
        
        # Predict covariance
        self.P = F @ self.P @ F.T + self.Q
        return self.x

    def update(self, z):
        """Update step using optical IR sensor measurements [Measured Altitude, Measured Radiance/Position]."""
        # Measurement matrix H (mapping state to measurement space)
        H = np.array([
            [0, 0, 1, 0],  # Measuring altitude Z
            [1, 0, 0, 0]   # Measuring X coordinate
        ])
        
        # Innovation / Measurement residual
        y = z - (H @ self.x)
        
        # Innovation covariance
        S = (H @ self.P @ H.T) + self.R
        
        # Kalman Gain
        K = self.P @ H.T @ np.linalg.inv(S)
        
        # Update state estimate
        self.x = self.x + (K @ y)
        
        # Update covariance matrix
        I = np.eye(len(self.x))
        self.P = (I - (K @ H)) @ self.P
        
        return self.x

if __name__ == "__main__":
    print("--- Hyperery REI EKF Sensor Fusion Simulation ---")
    ekf = PlumeStateEKF()
    
    dt = 0.1  # 100 ms sensor cycle
    # Simulate 5 steps of tracking
    for step in range(5):
        predicted_state = ekf.predict(dt)
        # Mock sensor measurement arriving from the dual-band FPA
        simulated_measurement = np.array([predicted_state[2] + np.random.normal(0, 0.2), 
                                          predicted_state[0] + np.random.normal(0, 0.2)])
        updated_state = ekf.update(simulated_measurement)
        print(f"Step {step+1}: Fused Position Z (Altitude) = {updated_state[2]:.2f} km")
