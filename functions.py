import numpy as np
import matplotlib.pyplot as plt
import random

# Generate synthetic true positions
def generate_true_positions(num_points=50):
    """
    Generate synthetic true positions (latitude, longitude, altitude).
    """
    positions = []
    for _ in range(num_points):
        positions.append({
            'latitude': round(random.uniform(40.785, 40.787), 6),
            'longitude': round(random.uniform(6.797, 6.799), 6),
            'altitude': round(random.uniform(8.0, 12.0), 2),
        })
    return positions

# Simulate measured positions with errors
def add_position_error(true_positions, error_range=0.001):
    """
    Add random errors to simulate GNSS-measured positions.
    """
    measured_positions = []
    for pos in true_positions:
        measured_positions.append({
            'latitude': pos['latitude'] + np.random.uniform(-error_range, error_range),
            'longitude': pos['longitude'] + np.random.uniform(-error_range, error_range),
            'altitude': pos['altitude'] + np.random.uniform(-error_range * 100, error_range * 100),
        })
    return measured_positions

# Apply RTK corrections
def apply_rtk_corrections(base_station, measured_positions):
    """
    Apply RTK corrections using a base station.
    """
    corrected_positions = []
    for pos in measured_positions:
        corrected_positions.append({
            'latitude': pos['latitude'] - (pos['latitude'] - base_station['latitude']),
            'longitude': pos['longitude'] - (pos['longitude'] - base_station['longitude']),
            'altitude': pos['altitude'] - (pos['altitude'] - base_station['altitude']),
        })
    return corrected_positions

# Calculate error
def calculate_position_error(true_positions, measured_positions):
    """
    Calculate Euclidean error between true and measured/corrected positions.
    """
    errors = []
    for true_pos, measured_pos in zip(true_positions, measured_positions):
        error = np.sqrt(
            (true_pos['latitude'] - measured_pos['latitude'])**2 +
            (true_pos['longitude'] - measured_pos['longitude'])**2 +
            (true_pos['altitude'] - measured_pos['altitude'])**2
        )
        errors.append(error)
    return errors

# Visualization
def visualize_errors(true_positions, measured_positions, corrected_positions, measured_errors, corrected_errors):
    """
    Visualize position errors before and after correction.
    """
    # Scatter plot of positions
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.scatter([pos['longitude'] for pos in true_positions],
                [pos['latitude'] for pos in true_positions], label="True Positions", c="green")
    plt.scatter([pos['longitude'] for pos in measured_positions],
                [pos['latitude'] for pos in measured_positions], label="Measured Positions", c="red")
    plt.scatter([pos['longitude'] for pos in corrected_positions],
                [pos['latitude'] for pos in corrected_positions], label="Corrected Positions", c="blue")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Position Scatter Plot")
    plt.legend()

    # Error comparison
    plt.subplot(1, 2, 2)
    plt.plot(measured_errors, label="Measured Errors", c="red")
    plt.plot(corrected_errors, label="Corrected Errors", c="blue")
    plt.xlabel("Position Index")
    plt.ylabel("Error (Euclidean Distance)")
    plt.title("Error Comparison")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Main function
def main():
    # Define a fixed base station
    base_station = {'latitude': 40.7865, 'longitude': 6.7985, 'altitude': 10.0}

    # Generate synthetic data
    true_positions = generate_true_positions()
    measured_positions = add_position_error(true_positions)
    corrected_positions = apply_rtk_corrections(base_station, measured_positions)

    # Calculate errors
    measured_errors = calculate_position_error(true_positions, measured_positions)
    corrected_errors = calculate_position_error(true_positions, corrected_positions)

    # Visualize results
    visualize_errors(true_positions, measured_positions, corrected_positions, measured_errors, corrected_errors)

if __name__ == "__main__":
    main()
