
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.aircraft_surveillance import (
    create_aircraft,
    update_aircraft_position
)

from modules.wireless_link import (
    calculate_fspl,
    calculate_received_power,
    calculate_noise_power,
    calculate_snr,
    calculate_link_margin
)


# ============================================================
# AEROLINK NEPAL
# COMPLETE INTEGRATED ENGINEERING SIMULATION
#
# EXPERIMENT 3: 3D SLANT RANGE
# EXPERIMENT 4: WIRELESS LINK PERFORMANCE
# EXPERIMENT 5: BPSK BIT ERROR PROBABILITY
# EXPERIMENT 6: PACKET DELIVERY
# EXPERIMENT 7: RELIABILITY AND FAILOVER
# EXPERIMENT 8: INTEGRATED VISUALIZATION
# ============================================================


# ============================================================
# EXPERIMENT 3: HORIZONTAL DISTANCE AND SLANT RANGE
# ============================================================

def calculate_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate surface distance using the Haversine formula.
    """

    radius_km = 6371.0

    latitude1 = math.radians(lat1)
    latitude2 = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(latitude1)
        * math.cos(latitude2)
        * math.sin(delta_lon / 2) ** 2
    )

    a = max(0.0, min(1.0, a))

    return (
        2
        * radius_km
        * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    )


def calculate_slant_range(
    horizontal_distance_km,
    aircraft_altitude_m,
    ground_altitude_m=0
):
    """
    Calculate approximate straight-line separation.

    Uses local flat-Earth geometry and altitude difference.
    """

    height_difference_km = (
        aircraft_altitude_m - ground_altitude_m
    ) / 1000.0

    slant_range_km = math.sqrt(
        horizontal_distance_km ** 2
        + height_difference_km ** 2
    )

    return slant_range_km


# ============================================================
# EXPERIMENT 5: BPSK ERROR PROBABILITY
# ============================================================

def calculate_bpsk_ber(snr_db):
    """
    Calculate theoretical BER for coherent BPSK over AWGN.

    Educational simplifying assumption:
    Eb/N0 in dB is equal to the supplied SNR in dB.

    This requires an assumed bit rate equal to the
    receiver noise bandwidth, with no extra losses.
    """

    ebn0_linear = 10 ** (snr_db / 10)

    ber = 0.5 * math.erfc(
        math.sqrt(ebn0_linear)
    )

    return ber


# ============================================================
# EXPERIMENT 6: PACKET DELIVERY
# ============================================================

def calculate_packet_error_probability(
    bit_error_rate,
    packet_size_bytes
):
    """
    Probability that at least one bit is incorrect.

    Assumes independent bit errors and no FEC.
    """

    packet_bits = packet_size_bytes * 8

    if bit_error_rate <= 0:
        return 0.0

    if bit_error_rate >= 1:
        return 1.0

    packet_success_probability = (
        (1 - bit_error_rate) ** packet_bits
    )

    return 1 - packet_success_probability


# ============================================================
# EXPERIMENT 7: LINK SELECTION AND FAILOVER
# ============================================================

def determine_active_link(
    current_time,
    primary_failure_time,
    backup_activation_delay
):
    """
    Determine which communication link is active.

    The primary fails at the configured time.
    The backup becomes active after a fixed delay.
    """

    recovery_time = (
        primary_failure_time + backup_activation_delay
    )

    if current_time < primary_failure_time:
        return "Primary"

    if current_time < recovery_time:
        return "Unavailable"

    return "Backup"


# ============================================================
# COMPLETE INTEGRATED SIMULATION
# ============================================================

def run_integrated_simulation(
    time_step=5,
    number_updates=12,
    frequency_mhz=120.0,
    transmit_power_dbm=30.0,
    bandwidth_hz=25000,
    noise_figure_db=5.0,
    required_snr_db=10.0,
    additional_attenuation_db=50.0,
    primary_failure_time=30,
    backup_activation_delay=5,
    backup_snr_penalty_db=3.0,
    packets_per_update=100,
    packet_size_bytes=256,
    random_seed=42,
):
    """
    Integrate aircraft movement, radio propagation,
    BPSK error probability, packet delivery and failover.

    Returns a list of result dictionaries.
    """

    # --------------------------------------------------------
    # VALIDATE SETTINGS
    # --------------------------------------------------------

    if time_step <= 0 or number_updates < 1:
        raise ValueError(
            "Time step must be positive and updates >= 1."
        )

    if frequency_mhz <= 0 or bandwidth_hz <= 0:
        raise ValueError(
            "Frequency and bandwidth must be positive."
        )

    if packets_per_update < 1 or packet_size_bytes < 1:
        raise ValueError(
            "Packet counts and packet size must be positive."
        )

    if backup_activation_delay < 0:
        raise ValueError(
            "Backup activation delay cannot be negative."
        )

    if primary_failure_time < 0:
        raise ValueError(
            "Primary failure time cannot be negative."
        )

    if additional_attenuation_db < 0:
        raise ValueError(
            "Additional attenuation cannot be negative."
        )

    if backup_snr_penalty_db < 0:
        raise ValueError(
            "Backup SNR penalty cannot be negative."
        )

    # --------------------------------------------------------
    # GROUND STATION AND AIRCRAFT SETTINGS
    # --------------------------------------------------------

    ground_lat = 27.70
    ground_lon = 85.35
    ground_altitude_m = 0.0

    aircraft = create_aircraft(
        aircraft_id="AN101",
        latitude=27.70,
        longitude=85.45,
        altitude_m=3000,
        speed_kmh=360,
        heading_deg=90
    )

    # Repeatable random packet simulations
    rng = np.random.default_rng(random_seed)

    noise_power_dbm = calculate_noise_power(
        bandwidth_hz,
        noise_figure_db
    )

    results = []

    # --------------------------------------------------------
    # SIMULATE EVERY AIRCRAFT UPDATE
    # --------------------------------------------------------

    for step in range(number_updates + 1):

        if step > 0:
            aircraft = update_aircraft_position(
                aircraft,
                time_step
            )

        current_time = step * time_step

        # ----------------------------------------------------
        # EXPERIMENT 3: 3D AIRCRAFT DISTANCE
        # ----------------------------------------------------

        horizontal_distance_km = calculate_distance_km(
            ground_lat,
            ground_lon,
            aircraft["latitude"],
            aircraft["longitude"]
        )

        slant_range_km = calculate_slant_range(
            horizontal_distance_km,
            aircraft["altitude_m"],
            ground_altitude_m
        )

        # ----------------------------------------------------
        # EXPERIMENT 4: WIRELESS PERFORMANCE
        # ----------------------------------------------------

        fspl_db = calculate_fspl(
            slant_range_km,
            frequency_mhz
        )

        received_power_dbm = calculate_received_power(
            transmit_power_dbm,
            slant_range_km,
            frequency_mhz
        )

        # A configurable, hypothetical additional attenuation
        received_power_dbm -= additional_attenuation_db

        primary_snr_db = calculate_snr(
            received_power_dbm,
            noise_power_dbm
        )

        # ----------------------------------------------------
        # EXPERIMENT 7: LINK SELECTION
        # ----------------------------------------------------

        active_link = determine_active_link(
            current_time,
            primary_failure_time,
            backup_activation_delay
        )

        # Backup path has a hypothetical SNR penalty
        if active_link == "Backup":
            active_snr_db = (
                primary_snr_db - backup_snr_penalty_db
            )

        elif active_link == "Primary":
            active_snr_db = primary_snr_db

        else:
            active_snr_db = None

        # ----------------------------------------------------
        # EXPERIMENTS 5 AND 6:
        # BER AND PACKET DELIVERY
        # ----------------------------------------------------

        packets_sent = packets_per_update

        if active_snr_db is None:
            bit_error_rate = None
            packet_error_probability = 1.0
            packets_received = 0

        else:
            bit_error_rate = calculate_bpsk_ber(
                active_snr_db
            )

            packet_error_probability = (
                calculate_packet_error_probability(
                    bit_error_rate,
                    packet_size_bytes
                )
            )

            packet_success_probability = (
                1.0 - packet_error_probability
            )

            packets_received = int(
                rng.binomial(
                    packets_sent,
                    packet_success_probability
                )
            )

        packets_lost = packets_sent - packets_received

        packet_loss_percent = (
            packets_lost / packets_sent
        ) * 100

        # SNR margin for active link
        if active_snr_db is None:
            link_margin_db = None
        else:
            link_margin_db = calculate_link_margin(
                active_snr_db,
                required_snr_db
            )

        # Store all results
        results.append({
            "time_seconds": current_time,
            "aircraft_id": aircraft["aircraft_id"],
            "latitude": aircraft["latitude"],
            "longitude": aircraft["longitude"],
            "altitude_m": aircraft["altitude_m"],
            "horizontal_distance_km": horizontal_distance_km,
            "distance_km": slant_range_km,
            "fspl_db": fspl_db,
            "received_power_dbm": received_power_dbm,
            "primary_snr_db": primary_snr_db,
            "snr_db": active_snr_db,
            "link_margin_db": link_margin_db,
            "active_link": active_link,
            "bit_error_rate": bit_error_rate,
            "packet_error_probability": packet_error_probability,
            "packets_sent": packets_sent,
            "packets_received": packets_received,
            "packets_lost": packets_lost,
            "packet_loss_percent": packet_loss_percent,
        })

    return results


# ============================================================
# EXPERIMENT 8: PLOT COMPLETE RESULTS
# ============================================================

def plot_integrated_results(results):
    """
    Create a set of graphs from integrated simulation data.
    """

    df = pd.DataFrame(results)

    graph_definitions = [
        (
            "Aircraft Slant Range vs Time",
            "distance_km",
            "Slant Range (km)"
        ),
        (
            "Free-Space Path Loss vs Time",
            "fspl_db",
            "FSPL (dB)"
        ),
        (
            "Received Power vs Time",
            "received_power_dbm",
            "Power (dBm)"
        ),
        (
            "Active Link SNR vs Time",
            "snr_db",
            "SNR (dB)"
        ),
        (
            "Packet Loss vs Time",
            "packet_loss_percent",
            "Packet Loss (%)"
        ),
    ]

    figures = []

    for title, field, ylabel in graph_definitions:

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            df["time_seconds"],
            df[field],
            marker="o"
        )

        ax.set_title(title)
        ax.set_xlabel("Simulation Time (seconds)")
        ax.set_ylabel(ylabel)
        ax.grid(True)

        if field in (
            "snr_db",
            "packet_loss_percent"
        ):
            ax.axvspan(
                30,
                35,
                color="orange",
                alpha=0.2,
                label="Default failover interval"
            )
            ax.legend()

        fig.tight_layout()
        figures.append(fig)

    # Plot active communication link separately
    status_map = {
        "Unavailable": 0,
        "Primary": 1,
        "Backup": 2
    }

    status_values = [
        status_map[status]
        for status in df["active_link"]
    ]

    fig, ax = plt.subplots(figsize=(9, 4))

    ax.step(
        df["time_seconds"],
        status_values,
        where="post",
        marker="o"
    )

    ax.set_title("Communication Link Selection")
    ax.set_xlabel("Simulation Time (seconds)")
    ax.set_ylabel("Active Link")

    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(
        ["Unavailable", "Primary", "Backup"]
    )

    ax.grid(True)

    fig.tight_layout()
    figures.append(fig)

    return figures


# ============================================================
# MAIN PROGRAM: RUN ALL EXPERIMENTS
# ============================================================

if __name__ == "__main__":

    print("=" * 65)
    print("AEROLINK NEPAL")
    print("COMPLETE INTEGRATED SYSTEM SIMULATION")
    print("=" * 65)

    results = run_integrated_simulation()

    df = pd.DataFrame(results)

    columns_to_display = [
        "time_seconds",
        "distance_km",
        "snr_db",
        "active_link",
        "packets_received",
        "packets_lost",
    ]

    print()
    print(
        df[columns_to_display].to_string(
            index=False
        )
    )

    print()
    print("Total Packets Sent:", int(df["packets_sent"].sum()))

    print(
        "Total Packets Received:",
        int(df["packets_received"].sum())
    )

    print(
        "Total Packets Lost:",
        int(df["packets_lost"].sum())
    )

    total_sent = int(df["packets_sent"].sum())
    total_received = int(df["packets_received"].sum())

    print(
        "Overall Packet Delivery:",
        f"{100 * total_received / total_sent:.2f}%"
    )

    print(
        "\nNote: Theoretical BER, synthetic packets, "
        "and deterministic failover assumptions are used."
    )

    figures = plot_integrated_results(results)

    plt.show()

    for fig in figures:
        plt.close(fig)
