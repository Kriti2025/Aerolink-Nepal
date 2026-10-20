
import math
import matplotlib.pyplot as plt


# ============================================================
# EXPERIMENT 1: FREE-SPACE PATH LOSS
# ============================================================

def calculate_fspl(distance_km, frequency_mhz):
    if distance_km <= 0 or frequency_mhz <= 0:
        raise ValueError(
            "Distance and frequency must be greater than zero."
        )

    return (
        32.44
        + 20 * math.log10(distance_km)
        + 20 * math.log10(frequency_mhz)
    )


# ============================================================
# EXPERIMENT 2: RECEIVED POWER AND LINK BUDGET
# ============================================================

def calculate_received_power(
    transmit_power_dbm,
    distance_km,
    frequency_mhz,
    transmit_gain_dbi=0,
    receive_gain_dbi=0,
    additional_loss_db=0
):
    if additional_loss_db < 0:
        raise ValueError(
            "Additional loss cannot be negative."
        )

    fspl = calculate_fspl(
        distance_km,
        frequency_mhz
    )

    return (
        transmit_power_dbm
        + transmit_gain_dbi
        + receive_gain_dbi
        - fspl
        - additional_loss_db
    )


# ============================================================
# EXPERIMENT 3: RECEIVER NOISE AND SNR
# ============================================================

def calculate_noise_power(
    bandwidth_hz,
    noise_figure_db=5
):
    if bandwidth_hz <= 0:
        raise ValueError(
            "Bandwidth must be greater than zero."
        )

    if noise_figure_db < 0:
        raise ValueError(
            "Noise figure cannot be negative."
        )

    # Approximate thermal noise density at room temperature
    return (
        -174
        + 10 * math.log10(bandwidth_hz)
        + noise_figure_db
    )


def calculate_snr(
    received_power_dbm,
    noise_power_dbm
):
    return received_power_dbm - noise_power_dbm


# ============================================================
# MAIN PROGRAM: RUN ALL FOUR EXPERIMENTS
# ============================================================

if __name__ == "__main__":

    # Simulation assumptions
    frequency_mhz = 120
    transmit_power_dbm = 30
    transmit_gain_dbi = 0
    receive_gain_dbi = 0
    additional_loss_db = 0

    bandwidth_hz = 25000
    noise_figure_db = 5

    distances_km = [1, 5, 10, 20, 50, 100]

    print("AEROLINK NEPAL")
    print("Wireless Channel Analyzer")
    print("=" * 55)

    print(f"Frequency: {frequency_mhz} MHz")
    print(f"Transmit Power: {transmit_power_dbm} dBm")
    print(f"Receiver Bandwidth: {bandwidth_hz} Hz")
    print(f"Receiver Noise Figure: {noise_figure_db} dB")
    print()

    # --------------------------------------------------------
    # EXPERIMENT 1: FREE-SPACE PATH LOSS
    # --------------------------------------------------------

    print("EXPERIMENT 1: FREE-SPACE PATH LOSS")
    print()

    for distance in distances_km:
        fspl = calculate_fspl(
            distance,
            frequency_mhz
        )

        print(
            f"Distance: {distance:>3} km | "
            f"FSPL: {fspl:.2f} dB"
        )

    # --------------------------------------------------------
    # EXPERIMENT 2: RECEIVED POWER
    # --------------------------------------------------------

    print()
    print("EXPERIMENT 2: RECEIVED POWER")
    print()

    for distance in distances_km:
        received_power = calculate_received_power(
            transmit_power_dbm,
            distance,
            frequency_mhz,
            transmit_gain_dbi,
            receive_gain_dbi,
            additional_loss_db
        )

        print(
            f"Distance: {distance:>3} km | "
            f"Received Power: {received_power:.2f} dBm"
        )

    # --------------------------------------------------------
    # EXPERIMENT 3: RECEIVER NOISE AND SNR
    # --------------------------------------------------------

    print()
    print("EXPERIMENT 3: RECEIVER NOISE AND SNR")
    print()

    noise_power_dbm = calculate_noise_power(
        bandwidth_hz,
        noise_figure_db
    )

    print(
        f"Receiver Noise Power: {noise_power_dbm:.2f} dBm"
    )
    print()

    for distance in distances_km:
        received_power = calculate_received_power(
            transmit_power_dbm,
            distance,
            frequency_mhz,
            transmit_gain_dbi,
            receive_gain_dbi,
            additional_loss_db
        )

        snr_db = calculate_snr(
            received_power,
            noise_power_dbm
        )

        print(
            f"Distance: {distance:>3} km | "
            f"SNR: {snr_db:.2f} dB"
        )

    # --------------------------------------------------------
    # EXPERIMENT 4: GRAPHICAL ANALYSIS
    # --------------------------------------------------------

    graph_distances = list(range(1, 101))

    graph_fspl = [
        calculate_fspl(d, frequency_mhz)
        for d in graph_distances
    ]

    graph_received_power = [
        calculate_received_power(
            transmit_power_dbm,
            d,
            frequency_mhz,
            transmit_gain_dbi,
            receive_gain_dbi,
            additional_loss_db
        )
        for d in graph_distances
    ]

    graph_snr = [
        calculate_snr(power, noise_power_dbm)
        for power in graph_received_power
    ]

    # Graph 1: FSPL versus distance
    plt.figure(figsize=(9, 5))
    plt.plot(
        graph_distances,
        graph_fspl,
        label="FSPL"
    )
    plt.title("Free-Space Path Loss vs Distance")
    plt.xlabel("Distance (km)")
    plt.ylabel("Path Loss (dB)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Graph 2: Received power versus distance
    plt.figure(figsize=(9, 5))
    plt.plot(
        graph_distances,
        graph_received_power,
        label="Received Power"
    )
    plt.title("Received Power vs Distance")
    plt.xlabel("Distance (km)")
    plt.ylabel("Received Power (dBm)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Graph 3: SNR versus distance
    plt.figure(figsize=(9, 5))
    plt.plot(
        graph_distances,
        graph_snr,
        label="SNR"
    )
    plt.title("SNR vs Distance")
    plt.xlabel("Distance (km)")
    plt.ylabel("SNR (dB)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Display all three figures
    plt.show()
