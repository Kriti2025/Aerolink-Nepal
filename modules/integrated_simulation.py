
import math

from modules.aircraft_surveillance import (
    create_aircraft,
    update_aircraft_position
)

from modules.wireless_link import (
    calculate_fspl,
    calculate_received_power,
    calculate_noise_power,
    calculate_snr
)


# ============================================================
# CALCULATE DISTANCE BETWEEN TWO GEOGRAPHICAL POSITIONS
# ============================================================

def calculate_distance_km(lat1, lon1, lat2, lon2):

    # Earth's approximate radius in kilometers
    earth_radius = 6371.0

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = lat2 - lat1
    delta_lon = math.radians(lon2 - lon1)

    # Haversine formula
    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    a = max(0.0, min(1.0, a))

    return (
        2 * earth_radius
        * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    )


# ============================================================
# INTEGRATED AIRCRAFT AND WIRELESS SIMULATION
# ============================================================

def run_integrated_simulation():

    # Hypothetical ground station in the Kathmandu area
    ground_lat = 27.70
    ground_lon = 85.35

    # Wireless system settings
    frequency_mhz = 120
    transmit_power_dbm = 30
    bandwidth_hz = 25000
    noise_figure_db = 5

    noise_power_dbm = calculate_noise_power(
        bandwidth_hz,
        noise_figure_db
    )

    # Create a fictional aircraft east of the ground station
    aircraft = create_aircraft(
        aircraft_id="AN101",
        latitude=27.70,
        longitude=85.45,
        altitude_m=3000,
        speed_kmh=360,
        heading_deg=90
    )

    time_step = 10
    number_updates = 6

    results = []

    print("AEROLINK NEPAL")
    print("Integrated Aircraft and Wireless Link Simulation")
    print("=" * 65)

    for step in range(number_updates + 1):

        # Aircraft position is updated after the first step
        if step > 0:
            aircraft = update_aircraft_position(
                aircraft,
                time_step
            )

        elapsed_time = step * time_step

        # Calculate horizontal ground separation
        distance_km = calculate_distance_km(
            ground_lat,
            ground_lon,
            aircraft["latitude"],
            aircraft["longitude"]
        )

        # Free-space path loss
        fspl_db = calculate_fspl(
            distance_km,
            frequency_mhz
        )

        # Received signal power
        received_power_dbm = calculate_received_power(
            transmit_power_dbm,
            distance_km,
            frequency_mhz
        )

        # Signal-to-noise ratio
        snr_db = calculate_snr(
            received_power_dbm,
            noise_power_dbm
        )

        record = {
            "time_seconds": elapsed_time,
            "latitude": aircraft["latitude"],
            "longitude": aircraft["longitude"],
            "distance_km": distance_km,
            "fspl_db": fspl_db,
            "received_power_dbm": received_power_dbm,
            "snr_db": snr_db
        }

        results.append(record)

        print(
            f"Time: {elapsed_time:>2} s | "
            f"Distance: {distance_km:.2f} km | "
            f"FSPL: {fspl_db:.2f} dB | "
            f"Power: {received_power_dbm:.2f} dBm | "
            f"SNR: {snr_db:.2f} dB"
        )

    return results


# ============================================================
# RUN THE SIMULATION
# ============================================================

if __name__ == "__main__":
    run_integrated_simulation()
