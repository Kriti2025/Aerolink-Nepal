
import math


# ============================================================
# EXPERIMENT 1: AIRCRAFT SURVEILLANCE DATA
# ============================================================

def create_aircraft(
    aircraft_id,
    latitude,
    longitude,
    altitude_m,
    speed_kmh,
    heading_deg
):
    """
    Create a synthetic aircraft surveillance record.

    Heading convention:
    0 = North
    90 = East
    180 = South
    270 = West
    """

    if not 0 <= heading_deg < 360:
        raise ValueError("Heading must be between 0 and 359 degrees.")

    if speed_kmh < 0:
        raise ValueError("Speed cannot be negative.")

    if not -90 <= latitude <= 90:
        raise ValueError("Invalid latitude.")

    if not -180 <= longitude <= 180:
        raise ValueError("Invalid longitude.")

    if altitude_m < 0:
        raise ValueError("Altitude cannot be negative in this model.")

    return {
        "aircraft_id": aircraft_id,
        "latitude": latitude,
        "longitude": longitude,
        "altitude_m": altitude_m,
        "speed_kmh": speed_kmh,
        "heading_deg": heading_deg
    }


# ============================================================
# EXPERIMENT 2: AIRCRAFT MOVEMENT SIMULATION
# ============================================================

def update_aircraft_position(aircraft, time_seconds):
    """
    Update aircraft position using constant ground speed
    and heading over a short interval.

    This is an approximate model for educational use.
    """

    if time_seconds < 0:
        raise ValueError("Time cannot be negative.")

    speed_kmh = aircraft["speed_kmh"]

    # Calculate traveled distance in kilometers
    distance_km = speed_kmh * time_seconds / 3600

    # Convert heading from degrees to radians
    heading_rad = math.radians(aircraft["heading_deg"])

    # Northward and eastward components
    north_km = distance_km * math.cos(heading_rad)
    east_km = distance_km * math.sin(heading_rad)

    # Approximate conversion from kilometers to coordinates
    latitude_change = north_km / 111.32

    latitude_rad = math.radians(aircraft["latitude"])

    longitude_scale = 111.32 * math.cos(latitude_rad)

    if abs(longitude_scale) < 1e-9:
        raise ValueError("Longitude approximation invalid near the poles.")

    longitude_change = east_km / longitude_scale

    new_latitude = aircraft["latitude"] + latitude_change
    new_longitude = aircraft["longitude"] + longitude_change

    if not -90 <= new_latitude <= 90:
        raise ValueError("Updated latitude is outside valid range.")

    if not -180 <= new_longitude <= 180:
        raise ValueError("Updated longitude is outside valid range.")

    updated_aircraft = aircraft.copy()

    updated_aircraft["latitude"] = new_latitude
    updated_aircraft["longitude"] = new_longitude

    return updated_aircraft


# ============================================================
# MAIN PROGRAM: TEST THE SIMULATOR
# ============================================================

if __name__ == "__main__":

    print("AEROLINK NEPAL")
    print("Aircraft Surveillance Simulator")
    print("=" * 55)

    # Fictional aircraft in a hypothetical Kathmandu-area scenario
    aircraft = create_aircraft(
        aircraft_id="AN101",
        latitude=27.70,
        longitude=85.35,
        altitude_m=3000,
        speed_kmh=360,
        heading_deg=90
    )

    print("\nINITIAL AIRCRAFT INFORMATION")

    for key, value in aircraft.items():
        print(f"{key}: {value}")

    print("\nAIRCRAFT POSITION UPDATES")

    # Generate updates at 10-second intervals
    time_step_seconds = 10

    for step in range(1, 7):

        aircraft = update_aircraft_position(
            aircraft,
            time_step_seconds
        )

        elapsed_time = step * time_step_seconds

        print(
            f"Time: {elapsed_time:>2} seconds | "
            f"Latitude: {aircraft['latitude']:.5f} | "
            f"Longitude: {aircraft['longitude']:.5f} | "
            f"Altitude: {aircraft['altitude_m']} m"
        )
