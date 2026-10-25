
import matplotlib.pyplot as plt

from modules.integrated_simulation import run_integrated_simulation


# ============================================================
# AEROLINK NEPAL
# INTEGRATED AIRCRAFT-WIRELESS VISUALIZATION
# ============================================================

def plot_integrated_results():

    # Run the existing aircraft and wireless simulation
    results = run_integrated_simulation()

    # Extract simulation results
    times = [row["time_seconds"] for row in results]

    distances = [row["distance_km"] for row in results]

    fspl_values = [row["fspl_db"] for row in results]

    received_powers = [
        row["received_power_dbm"] for row in results
    ]

    snr_values = [row["snr_db"] for row in results]

    # --------------------------------------------------------
    # GRAPH 1: AIRCRAFT DISTANCE VS TIME
    # --------------------------------------------------------

    fig1, ax1 = plt.subplots(figsize=(9, 4))

    ax1.plot(times, distances, marker="o")

    ax1.set_title("Aircraft Distance vs Time")
    ax1.set_xlabel("Time (seconds)")
    ax1.set_ylabel("Distance (km)")
    ax1.grid(True)

    fig1.tight_layout()

    # --------------------------------------------------------
    # GRAPH 2: PATH LOSS VS TIME
    # --------------------------------------------------------

    fig2, ax2 = plt.subplots(figsize=(9, 4))

    ax2.plot(times, fspl_values, marker="o")

    ax2.set_title("Free-Space Path Loss vs Time")
    ax2.set_xlabel("Time (seconds)")
    ax2.set_ylabel("FSPL (dB)")
    ax2.grid(True)

    fig2.tight_layout()

    # --------------------------------------------------------
    # GRAPH 3: RECEIVED POWER VS TIME
    # --------------------------------------------------------

    fig3, ax3 = plt.subplots(figsize=(9, 4))

    ax3.plot(times, received_powers, marker="o")

    ax3.set_title("Received Power vs Time")
    ax3.set_xlabel("Time (seconds)")
    ax3.set_ylabel("Received Power (dBm)")
    ax3.grid(True)

    fig3.tight_layout()

    # --------------------------------------------------------
    # GRAPH 4: SNR VS TIME
    # --------------------------------------------------------

    fig4, ax4 = plt.subplots(figsize=(9, 4))

    ax4.plot(times, snr_values, marker="o")

    ax4.set_title("Signal-to-Noise Ratio vs Time")
    ax4.set_xlabel("Time (seconds)")
    ax4.set_ylabel("SNR (dB)")
    ax4.grid(True)

    plt.show()

    for fig in [fig1, fig2, fig3, fig4]:
        plt.close(fig)


if __name__ == "__main__":
    plot_integrated_results()
