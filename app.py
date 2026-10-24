
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# IMPORT EXISTING ENGINEERING SIMULATION FUNCTIONS
# ============================================================

from modules.fec_awgn_experiment import run_fec_awgn
from modules.ber_snr_analysis_new import run_ber_snr_analysis

from modules.wireless_link import (
    calculate_fspl,
    calculate_received_power,
    calculate_noise_power,
    calculate_snr,
    calculate_link_margin,
    interpret_link_quality
)

from modules.network_monitor import simulate_network

from modules.aircraft_surveillance import (
    create_aircraft,
    update_aircraft_position
)

from modules.reliability import (
    simulate_failover,
    simulate_recovery,
    plot_failover_timeline
)


# ============================================================
# AEROLINK NEPAL - MAIN STREAMLIT APPLICATION
# ============================================================

st.set_page_config(
    page_title="AeroLink Nepal",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AeroLink Nepal")

st.subheader(
    "Airport Communication & Surveillance Network Simulator"
)

st.info("Version 0.1 | Educational Engineering Simulation")

st.write(
    "Explore digital communication, radio propagation, "
    "network quality, aircraft surveillance, and "
    "communication reliability."
)


# ============================================================
# ENGINEERING MODULE SELECTION
# ============================================================

st.header("Engineering Modules")

modules = [
    "Digital Communication",
    "Wireless Link Analyzer",
    "Network Monitor",
    "Aircraft Surveillance Simulator",
    "Reliability and Failover"
]

selected_module = st.selectbox(
    "Choose an Engineering Module",
    modules,
    key="main_module_selector"
)


# ============================================================
# MODULE 1: DIGITAL COMMUNICATION
# ============================================================

if selected_module == "Digital Communication":

    st.header("Digital Communication Simulator")

    st.write(
        "Study BPSK modulation, AWGN noise, Bit Error Rate "
        "and Forward Error Correction."
    )

    # --------------------------------------------------------
    # EXPERIMENT 1: BPSK THROUGH AWGN
    # --------------------------------------------------------

    st.subheader("Experiment 1: BPSK Through AWGN")

    num_bits = st.slider(
        "Number of transmitted bits",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100,
        key="bpsk_bits"
    )

    ebn0_db = st.slider(
        "Eb/N0 (dB)",
        min_value=0,
        max_value=12,
        value=6,
        key="bpsk_ebn0"
    )

    if st.button(
        "Run BPSK Simulation",
        key="bpsk_run"
    ):

        bits = np.random.randint(0, 2, num_bits)

        # BPSK: 0 -> -1 and 1 -> +1
        symbols = 2 * bits - 1

        ebn0_linear = 10 ** (ebn0_db / 10)

        noise_std = np.sqrt(
            1 / (2 * ebn0_linear)
        )

        noise = np.random.normal(
            0,
            noise_std,
            num_bits
        )

        received = symbols + noise

        detected = (received > 0).astype(int)

        errors = int(
            np.count_nonzero(bits != detected)
        )

        ber = errors / num_bits

        st.subheader("BPSK Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Transmitted Bits", num_bits)
        col2.metric("Bit Errors", errors)
        col3.metric("BER", f"{ber:.6f}")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            symbols[:30],
            "o-",
            label="Transmitted"
        )

        ax.plot(
            received[:30],
            "x--",
            label="Received"
        )

        ax.axhline(
            0,
            linestyle=":",
            label="Decision Boundary"
        )

        ax.set_title("BPSK Transmission Through AWGN")
        ax.set_xlabel("Symbol Index")
        ax.set_ylabel("Amplitude")
        ax.grid(True)
        ax.legend()

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 2: FEC UNDER AWGN
    # --------------------------------------------------------

    st.subheader("Experiment 2: FEC Performance Under AWGN")

    fec_bits = st.slider(
        "Number of information bits",
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        key="fec_bits"
    )

    fec_esn0 = st.slider(
        "Channel Es/N0 (dB)",
        min_value=0,
        max_value=10,
        value=0,
        key="fec_esn0"
    )

    if st.button(
        "Run FEC + AWGN",
        key="fec_awgn_run"
    ):

        results = run_fec_awgn(
            num_bits=fec_bits,
            esn0_db=fec_esn0
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Coded-Bit BER",
            f"{results['coded_ber']:.6f}"
        )

        col2.metric(
            "Decoded Information BER",
            f"{results['decoded_ber']:.6f}"
        )

        st.write(
            "Original information bits:",
            results["num_bits"]
        )

        st.write(
            "Transmitted coded bits:",
            results["coded_bits"]
        )

        st.write(
            "Coded-bit errors:",
            results["coded_errors"]
        )

        st.write(
            "Information-bit errors after FEC:",
            results["decoded_errors"]
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            ["Before Decoding", "After Decoding"],
            [
                results["coded_ber"],
                results["decoded_ber"]
            ]
        )

        ax.set_title("BER Before and After FEC Decoding")
        ax.set_ylabel("Bit Error Rate")
        ax.grid(True, axis="y", alpha=0.3)

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "This educational comparison uses different BER "
            "denominators and does not establish an "
            "energy-efficiency advantage."
        )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 3: MANUAL FEC DEMONSTRATION
    # --------------------------------------------------------

    st.subheader("Experiment 3: Repetition-3 FEC")

    message = st.text_input(
        "Enter binary information",
        value="10110",
        key="fec_message"
    )

    if st.button(
        "Run FEC Demonstration",
        key="fec_demo_run"
    ):

        if not message or any(
            character not in "01" for character in message
        ):

            st.error("Enter only binary digits 0 and 1.")

        else:

            original = np.array(
                [int(character) for character in message]
            )

            encoded = np.repeat(original, 3)

            received = encoded.copy()

            # Flip one bit in each group of three
            received[1::3] ^= 1

            groups = received.reshape(-1, 3)

            decoded = (
                groups.sum(axis=1) >= 2
            ).astype(int)

            errors_before = int(
                np.count_nonzero(encoded != received)
            )

            errors_after = int(
                np.count_nonzero(original != decoded)
            )

            st.write("Original:", message)

            st.write(
                "Encoded:",
                "".join(map(str, encoded))
            )

            st.write(
                "Received:",
                "".join(map(str, received))
            )

            st.write(
                "Decoded:",
                "".join(map(str, decoded))
            )

            col1, col2 = st.columns(2)

            col1.metric("Coded Errors", errors_before)

            col2.metric(
                "Errors After FEC",
                errors_after
            )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 4: BER VS Eb/N0
    # --------------------------------------------------------

    st.subheader("Experiment 4: BER vs Eb/N0")

    analysis_bits = st.slider(
        "Bits for BER Analysis",
        min_value=10000,
        max_value=500000,
        value=100000,
        step=10000,
        key="ber_analysis_bits"
    )

    if st.button(
        "Run BER Analysis",
        key="ber_analysis_run"
    ):

        snr_values, ber_values = run_ber_snr_analysis(
            num_bits=analysis_bits
        )

        st.subheader("BER Analysis Results")

        for snr_value, ber_value in zip(
            snr_values,
            ber_values
        ):

            st.write(
                f"Eb/N0 = {snr_value} dB | "
                f"BER = {ber_value:.6f}"
            )

        snr_array = np.asarray(
            snr_values,
            dtype=float
        )

        ber_array = np.asarray(
            ber_values,
            dtype=float
        )

        valid = ber_array > 0

        fig, ax = plt.subplots(figsize=(9, 4))

        if np.any(valid):

            ax.semilogy(
                snr_array[valid],
                ber_array[valid],
                "o-",
                label="Simulated BER"
            )

            ax.legend()

        else:

            st.warning(
                "No bit errors were observed."
            )

        ax.set_title("BER vs Eb/N0 for BPSK over AWGN")
        ax.set_xlabel("Eb/N0 (dB)")
        ax.set_ylabel("Bit Error Rate")
        ax.grid(True, which="both")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# MODULE 2: WIRELESS LINK ANALYZER
# ============================================================

elif selected_module == "Wireless Link Analyzer":

    st.header("Wireless Channel Analyzer")

    st.write(
        "Analyze an idealized aircraft-to-ground radio link "
        "using free-space propagation and receiver noise."
    )

    distance = st.slider(
        "Aircraft Distance (km)",
        min_value=1,
        max_value=100,
        value=10,
        key="wireless_distance"
    )

    frequency = st.number_input(
        "Frequency (MHz)",
        min_value=1.0,
        value=120.0,
        key="wireless_frequency"
    )

    transmit_power = st.slider(
        "Transmit Power (dBm)",
        min_value=0,
        max_value=50,
        value=30,
        key="wireless_power"
    )

    bandwidth = st.number_input(
        "Receiver Bandwidth (Hz)",
        min_value=1,
        value=25000,
        key="wireless_bandwidth"
    )

    noise_figure = st.slider(
        "Noise Figure (dB)",
        min_value=0,
        max_value=20,
        value=5,
        key="wireless_noise_figure"
    )

    required_snr = st.slider(
        "Assumed Required SNR (dB)",
        min_value=0,
        max_value=30,
        value=10,
        key="wireless_required_snr"
    )

    # --------------------------------------------------------
    # CALCULATIONS
    # --------------------------------------------------------

    fspl = calculate_fspl(
        distance,
        frequency
    )

    received_power = calculate_received_power(
        transmit_power,
        distance,
        frequency
    )

    noise_power = calculate_noise_power(
        bandwidth,
        noise_figure
    )

    snr = calculate_snr(
        received_power,
        noise_power
    )

    margin = calculate_link_margin(
        snr,
        required_snr
    )

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    st.subheader("Wireless Link Results")

    col1, col2 = st.columns(2)

    col1.metric("FSPL", f"{fspl:.2f} dB")

    col2.metric(
        "Received Power",
        f"{received_power:.2f} dBm"
    )

    col3, col4 = st.columns(2)

    col3.metric("SNR", f"{snr:.2f} dB")

    col4.metric(
        "Link Margin",
        f"{margin:.2f} dB"
    )

    st.write(
        "Estimated receiver noise:",
        f"{noise_power:.2f} dBm"
    )

    st.write(
        "Educational SNR Quality:",
        interpret_link_quality(snr)
    )

    if margin >= 0:

        st.success(
            "Assumed SNR requirement satisfied."
        )

    else:

        st.warning(
            "Assumed SNR requirement not satisfied."
        )

    st.caption(
        "Ideal free-space model with zero antenna gains "
        "and zero additional losses. Requirements and "
        "quality classifications are illustrative."
    )

    # --------------------------------------------------------
    # GRAPHS
    # --------------------------------------------------------

    st.subheader("Wireless Performance vs Distance")

    graph_distances = list(range(1, 101))

    graph_fspl = [
        calculate_fspl(d, frequency)
        for d in graph_distances
    ]

    graph_power = [
        calculate_received_power(
            transmit_power,
            d,
            frequency
        )
        for d in graph_distances
    ]

    graph_snr = [
        calculate_snr(power, noise_power)
        for power in graph_power
    ]

    graph_margin = [
        calculate_link_margin(value, required_snr)
        for value in graph_snr
    ]

    graphs = [
        ("FSPL", graph_fspl, "Path Loss (dB)"),
        ("Received Power", graph_power, "Power (dBm)"),
        ("SNR", graph_snr, "SNR (dB)"),
        ("Link Margin", graph_margin, "Margin (dB)")
    ]

    for title, values, y_label in graphs:

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            graph_distances,
            values,
            label=title
        )

        ax.axvline(
            distance,
            linestyle="--",
            label="Selected Distance"
        )

        if title == "Link Margin":

            ax.axhline(
                0,
                linestyle=":",
                label="Zero Margin"
            )

        ax.set_title(f"{title} vs Distance")
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel(y_label)
        ax.grid(True)
        ax.legend()

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# MODULE 3: NETWORK QUALITY MONITOR
# ============================================================

elif selected_module == "Network Monitor":

    st.header("Network Quality Monitor")

    st.write(
        "Simulate packet delivery between an airport ground "
        "station and a monitoring center."
    )

    packets = st.slider(
        "Number of Packets",
        min_value=100,
        max_value=1000,
        value=100,
        step=100,
        key="network_packets"
    )

    latency = st.slider(
        "Base One-way Latency (ms)",
        min_value=10,
        max_value=200,
        value=40,
        key="network_latency"
    )

    delay_std = st.slider(
        "Delay Variation (ms)",
        min_value=0,
        max_value=100,
        value=10,
        key="network_delay_std"
    )

    loss = st.slider(
        "Packet Loss Probability (%)",
        min_value=0,
        max_value=30,
        value=2,
        key="network_loss"
    )

    duration = st.slider(
        "Observation Duration (seconds)",
        min_value=1,
        max_value=60,
        value=10,
        key="network_duration"
    )

    packet_size = st.number_input(
        "Packet Size (bytes)",
        min_value=1,
        value=1000,
        key="network_packet_size"
    )

    if st.button(
        "Run Network Simulation",
        key="network_run"
    ):

        result = simulate_network(
            num_packets=packets,
            base_latency_ms=latency,
            jitter_std_ms=delay_std,
            loss_probability=loss / 100,
            packet_size_bytes=packet_size,
            duration_seconds=duration
        )

        st.subheader("Network Performance")

        col1, col2 = st.columns(2)

        col1.metric(
            "Average Latency",
            f"{result['average_latency_ms']:.2f} ms"
        )

        col2.metric(
            "Jitter",
            f"{result['jitter_ms']:.2f} ms"
        )

        col3, col4 = st.columns(2)

        col3.metric(
            "Packet Loss",
            f"{result['packet_loss_percent']:.2f}%"
        )

        col4.metric(
            "Throughput",
            f"{result['throughput_mbps']:.4f} Mbps"
        )

        st.write(
            "Packets Sent:",
            result["packets_sent"]
        )

        st.write(
            "Packets Received:",
            result["packets_received"]
        )

        st.write(
            "Packets Lost:",
            result["packets_lost"]
        )

        # ----------------------------------------------------
        # PACKET DELAY GRAPH
        # ----------------------------------------------------

        delays = result["received_delays"]

        if delays:

            fig, ax = plt.subplots(figsize=(9, 4))

            ax.plot(
                delays,
                label="Received Packet Delay"
            )

            ax.set_title("Simulated Packet Delay")
            ax.set_xlabel("Received Packet Index")
            ax.set_ylabel("Delay (ms)")
            ax.grid(True)
            ax.legend()

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

        else:

            st.warning(
                "No packets were received."
            )

        st.caption(
            "Synthetic packet-network simulation. "
            "The results are not live airport network measurements."
        )


# ============================================================
# MODULE 4: AIRCRAFT SURVEILLANCE SIMULATOR
# ============================================================

elif selected_module == "Aircraft Surveillance Simulator":

    st.header("Aircraft Surveillance Simulator")

    st.info(
        "This simulator generates synthetic aircraft "
        "position data rather than receiving real "
        "radar or ADS-B transmissions."
    )

    # --------------------------------------------------------
    # EXPERIMENT 1: AIRCRAFT INFORMATION
    # --------------------------------------------------------

    st.subheader("Experiment 1: Aircraft Information")

    aircraft_id = st.text_input(
        "Aircraft Identifier",
        value="AN101",
        key="aircraft_id"
    )

    latitude = st.number_input(
        "Initial Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=27.70,
        format="%.5f",
        key="aircraft_lat"
    )

    longitude = st.number_input(
        "Initial Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=85.35,
        format="%.5f",
        key="aircraft_lon"
    )

    altitude = st.number_input(
        "Altitude (meters)",
        min_value=0,
        max_value=20000,
        value=3000,
        key="aircraft_alt"
    )

    speed = st.slider(
        "Ground Speed (km/h)",
        min_value=0,
        max_value=900,
        value=360,
        step=10,
        key="aircraft_speed"
    )

    heading = st.slider(
        "Track Direction (degrees)",
        min_value=0,
        max_value=359,
        value=90,
        key="aircraft_heading"
    )

    st.caption(
        "0° = North, 90° = East, "
        "180° = South, 270° = West."
    )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 2: AIRCRAFT MOVEMENT
    # --------------------------------------------------------

    st.subheader("Experiment 2: Aircraft Movement")

    time_step = st.slider(
        "Position Update Interval (seconds)",
        min_value=5,
        max_value=60,
        value=10,
        step=5,
        key="aircraft_time_step"
    )

    updates = st.slider(
        "Number of Updates",
        min_value=1,
        max_value=30,
        value=6,
        key="aircraft_updates"
    )

    total_seconds = time_step * updates

    travel_distance = (
        speed * total_seconds / 3600
    )

    st.write(
        "Simulation Duration:",
        f"{total_seconds} seconds"
    )

    st.write(
        "Expected Travel Distance:",
        f"{travel_distance:.2f} km"
    )

    if st.button(
        "Simulate Aircraft Movement",
        key="aircraft_simulate"
    ):

        try:

            aircraft = create_aircraft(
                aircraft_id=aircraft_id,
                latitude=latitude,
                longitude=longitude,
                altitude_m=altitude,
                speed_kmh=speed,
                heading_deg=heading
            )

            trajectory = []

            for step in range(updates + 1):

                if step > 0:

                    aircraft = update_aircraft_position(
                        aircraft,
                        time_step
                    )

                trajectory.append({
                    "time_seconds": step * time_step,
                    "aircraft_id": aircraft["aircraft_id"],
                    "latitude": aircraft["latitude"],
                    "longitude": aircraft["longitude"],
                    "altitude_m": aircraft["altitude_m"],
                    "speed_kmh": aircraft["speed_kmh"],
                    "heading_deg": aircraft["heading_deg"]
                })

            trajectory_df = pd.DataFrame(trajectory)

            # ------------------------------------------------
            # EXPERIMENT 3: TRACKING RESULTS
            # ------------------------------------------------

            st.divider()

            st.subheader("Experiment 3: Tracking Results")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Aircraft ID",
                aircraft_id
            )

            col2.metric(
                "Ground Speed",
                f"{speed} km/h"
            )

            col3.metric(
                "Track Direction",
                f"{heading}°"
            )

            col4, col5, col6 = st.columns(3)

            col4.metric(
                "Altitude",
                f"{altitude} m"
            )

            col5.metric(
                "Travel Distance",
                f"{travel_distance:.2f} km"
            )

            col6.metric(
                "Elapsed Time",
                f"{total_seconds} sec"
            )

            st.write(
                "Final Latitude:",
                f"{aircraft['latitude']:.5f}°"
            )

            st.write(
                "Final Longitude:",
                f"{aircraft['longitude']:.5f}°"
            )

            # ------------------------------------------------
            # EXPERIMENT 4: AIRCRAFT POSITION MAP
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "Experiment 4: Aircraft Position Visualization"
            )

            st.map(
                trajectory_df,
                latitude="latitude",
                longitude="longitude"
            )

            st.subheader("Aircraft Position Update History")

            st.dataframe(
                trajectory_df,
                use_container_width=True
            )

            # Latitude versus time
            fig, ax = plt.subplots(figsize=(9, 4))

            ax.plot(
                trajectory_df["time_seconds"],
                trajectory_df["latitude"],
                "o-"
            )

            ax.set_title("Aircraft Latitude vs Time")
            ax.set_xlabel("Elapsed Time (seconds)")
            ax.set_ylabel("Latitude")
            ax.grid(True)

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            # Longitude versus time
            fig, ax = plt.subplots(figsize=(9, 4))

            ax.plot(
                trajectory_df["time_seconds"],
                trajectory_df["longitude"],
                "o-"
            )

            ax.set_title("Aircraft Longitude vs Time")
            ax.set_xlabel("Elapsed Time (seconds)")
            ax.set_ylabel("Longitude")
            ax.grid(True)

            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

            st.success(
                "Aircraft surveillance simulation completed."
            )

            st.caption(
                "Synthetic aircraft positions using constant "
                "ground speed, direction, and altitude."
            )

        except ValueError as error:

            st.error(
                f"Invalid aircraft settings: {error}"
            )


# ============================================================
# MODULE 5: RELIABILITY AND FAILOVER
# ============================================================

elif selected_module == "Reliability and Failover":

    st.header("Reliability and Failover Simulator")

    st.write(
        "Study primary-link failure, backup-link selection, "
        "failover recovery time, and service availability."
    )

    # --------------------------------------------------------
    # EXPERIMENT 1: LINK SELECTION
    # --------------------------------------------------------

    st.subheader(
        "Experiment 1: Primary and Backup Link Selection"
    )

    primary_available = st.checkbox(
        "Primary Link Available",
        value=True,
        key="reliability_primary_available"
    )

    backup_available = st.checkbox(
        "Backup Link Available",
        value=True,
        key="reliability_backup_available"
    )

    selection = simulate_failover(
        primary_available=primary_available,
        backup_available=backup_available
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Active Link",
        selection["active_link"]
    )

    col2.metric(
        "System Status",
        selection["status"]
    )

    if selection["status"] == "Communication Unavailable":

        st.error(
            "Neither the primary nor backup link is available."
        )

    elif selection["status"] == "Failover Active":

        st.warning(
            "The primary link has failed. "
            "The backup link has been selected."
        )

    else:

        st.success(
            "The primary communication link is operational."
        )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 2: RECOVERY TIME AND AVAILABILITY
    # --------------------------------------------------------

    st.subheader(
        "Experiment 2: Failover Recovery Time and Availability"
    )

    st.caption(
        "The recovery-time experiment assumes an available "
        "backup link, independent of the checkboxes above."
    )

    total_time = st.slider(
        "Observation Duration (seconds)",
        min_value=10,
        max_value=300,
        value=60,
        step=10,
        key="reliability_total_time"
    )

    failure_time = st.slider(
        "Primary Failure Time (seconds)",
        min_value=0,
        max_value=total_time,
        value=min(30, total_time),
        key="reliability_failure_time"
    )

    failover_delay = st.slider(
        "Backup Activation Delay (seconds)",
        min_value=0,
        max_value=60,
        value=5,
        key="reliability_failover_delay"
    )

    if st.button(
        "Run Failover Simulation",
        key="run_reliability_simulation"
    ):

        result = simulate_recovery(
            total_time=total_time,
            failure_time=failure_time,
            failover_delay=failover_delay
        )

        # ----------------------------------------------------
        # RECOVERY RESULTS
        # ----------------------------------------------------

        st.subheader("Recovery and Availability Results")

        col1, col2 = st.columns(2)

        col1.metric(
            "Communication Downtime",
            f"{result['downtime']:.2f} s"
        )

        col2.metric(
            "Observed Availability",
            f"{result['availability']:.2f}%"
        )

        col3, col4 = st.columns(2)

        col3.metric(
            "Primary Failure Time",
            f"{result['failure_time']} s"
        )

        col4.metric(
            "Backup Recovery Time",
            f"{result['recovery_time']} s"
        )

        st.write(
            "Communication Uptime:",
            f"{result['uptime']:.2f} seconds"
        )

        # ----------------------------------------------------
        # EXPERIMENT 3: FAILOVER TIMELINE
        # ----------------------------------------------------

        st.subheader(
            "Experiment 3: Failover Timeline"
        )

        fig = plot_failover_timeline(result)

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "Educational deterministic failover model. "
            "It assumes the backup link becomes operational "
            "after the selected delay. Observed availability "
            "is calculated for this simulation period only, "
            "not as a long-term network reliability estimate."
        )


# ============================================================
# END OF APPLICATION
# ============================================================

else:

    st.info(
        f"{selected_module} is currently under development."
    )
