"""
Real-Time Kinematics (RTK) is a satellite navigation technique that enhances the accuracy of position data from
Global Navigation Satellite Systems (GNSS) like GPS. It works by comparing phase differences between satellite signals
received by a stationary reference station and a mobile drone, in this case. The reference station calculates
corrections for factors like atmospheric effects and satellite clock errors, which are transmitted to the drone in
real-time. By applying these corrections, RTK achieves centimeter-level accuracy in determining the drone's position.
"""

import time
import random

def obtain_data_position():
    """
    Simulates obtaining position data.
    """
    # Simulates generating random coordinates for the current position
    position = {
        'latitude': round(random.uniform(40.785, 40.787), 6),
        'longitude': round(random.uniform(6.797, 6.799), 6),
        'altitude': round(random.uniform(8.0, 12.0), 2)
    }
    return position

def calculate_distance(p1, p2):
    """
    Calculates the Euclidean distance between two points in 3D.
    """
    # x -> longitude, y -> latitude, z -> altitude
    eu_distance = ((p1['latitude'] - p2['latitude'])**2 +
                   (p1['longitude'] - p2['longitude'])**2 +
                   (p1['altitude'] - p2['altitude'])**2)**0.5
    return eu_distance

def main():
    # Set the initial reference position (base station)
    reference = {
        'latitude': 40.7864,
        'longitude': 6.7986,
        'altitude': 10.0
    }
    print("Reference position: ", reference)

    try:
        while True:
            # Obtain the current position
            current_position = obtain_data_position()
            print("Current position: ", current_position)

            # Calculate the distance between the current position and the reference position
            dist = calculate_distance(reference, current_position)
            print("Distance from the reference position: ", dist)

            # Set the reference distance to check for position changes
            dist_ref = 0.1  # m

            # Check if the distance is greater than the reference distance
            if dist > dist_ref:
                print("Significant position change detected!")

                # Calculate correction factors for each coordinate
                correction_factor_lat = current_position['latitude'] - reference['latitude']
                correction_factor_lon = current_position['longitude'] - reference['longitude']
                correction_factor_alt = current_position['altitude'] - reference['altitude']

                # Apply corrections to the reference position
                reference['latitude'] += correction_factor_lat
                reference['longitude'] += correction_factor_lon
                reference['altitude'] += correction_factor_alt

                print("Corrected coordinates:", reference)
            else:
                print("No significant position change detected.")

            # Wait before checking the position again
            time.sleep(1)  # Wait 1 second (example) between each position check
            # Can be adapted to our needs in the future

    except KeyboardInterrupt:  # CTRL+C
        print("Program stopped.")

if __name__ == "__main__":
    main()