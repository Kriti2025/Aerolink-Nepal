
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from modules.fec_awgn_experiment import run_fec_awgn
from modules.ber_snr_analysis_new import run_ber_snr_analysis

from modules.wireless_link import (
    calculate_fspl,
    calculate_received_power,
    calculate_noise_power,
    calculate_snr,
    calculate_link_margin,
    interpret_link_quality,
)

from modules.network_monitor import simulate_network

from modules.aircraft_surveillance import (
    create_aircraft,
    update_aircraft_position,
)

from modules.reliability import (
    simulate_failover,
    simulate_recovery,
    plot_failover_timeline,
)

from modules.integrated_simulation import (
    run_integrated_simulation,
    plot_integrated_results,
)


# ============================================================
# AEROLINK NEPAL - MAIN APPLICATION
# ============================================================

st.set_page_config(
    page_title="AeroLink Nepal",
    page_icon="✈️",
    layout="wide",
)

st.title("✈️ AeroLink Nepal")

st.subheader(
    "Airport Communication & Surveillance Network Simulator"
)

st.info("Version 0.2 | Educational Engineering Simulation")

st.write(
    "Explore digital communication, wireless propagation, "
    "network quality, aircraft surveillance, reliability, "
    "and integrated system performance."
)


# ============================================================
# ENGINEERING MODULE SELECTION
# ============================================================

modules = [
    "Digital Communication",
    "Wireless Link Analyzer",
    "Network Monitor",
    "Aircraft Surveillance Simulator",
    "Reliability and Failover",
    "Integrated System Simulation",
]

selected_module = st.selectbox(
    "Choose an Engineering Module",
    modules,
    key="main_module_selector",
)


# ============================================================
# MODULE 1: DIGITAL COMMUNICATION
# ============================================================

if selected_module == "Digital Communication":

    st.header("Digital Communication Simulator")

    st.write(
        "Study BPSK modulation, AWGN noise, "
        "Bit Error Rate and Forward Error Correction."
    )

    # --------------------------------------------------------
    # EXPERIMENT 1: BPSK THROUGH AWGN
    # --------------------------------------------------------

    st.subheader("Experiment 1: BPSK Through AWGN")

    num_bits = st.slider(
        "Number of transmitted bits",
        100, 10000, 1000,
        step=100,
        key="bpsk_bits",
    )

    ebn0_db = st.slider(
        "Eb/N0 (dB)",
        0, 12, 6,
        key="bpsk_ebn0",
    )

    if st.button("Run BPSK Simulation", key="bpsk_run"):

        bits = np.random.randint(0, 2, num_bits)
        symbols = 2 * bits - 1

        ebn0_linear = 10 ** (ebn0_db / 10)

        noise_std = np.sqrt(
            1 / (2 * ebn0_linear)
        )

        noise = np.random.normal(
            0, noise_std, num_bits
        )

        received = symbols + noise
        detected = (received > 0).astype(int)

        errors = int(
            np.count_nonzero(bits != detected)
        )

        ber = errors / num_bits

        c1, c2, c3 = st.columns(3)

        c1.metric("Transmitted Bits", num_bits)
        c2.metric("Bit Errors", errors)
        c3.metric("BER", f"{ber:.6f}")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            symbols[:30],
            "o-",
            label="Transmitted",
        )

        ax.plot(
            received[:30],
            "x--",
            label="Received",
        )

        ax.axhline(
            0,
            linestyle=":",
            label="Decision Boundary",
        )

        ax.set_title("BPSK Through AWGN")
        ax.set_xlabel("Symbol Index")
        ax.set_ylabel("Amplitude")

        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 2: FEC UNDER AWGN
    # --------------------------------------------------------

    st.subheader("Experiment 2: FEC Under AWGN")

    fec_bits = st.slider(
        "Number of information bits",
        1000, 50000, 10000,
        step=1000,
        key="fec_bits",
    )

    fec_esn0 = st.slider(
        "Channel Es/N0 (dB)",
        0, 10, 0,
        key="fec_esn0",
    )

    if st.button("Run FEC + AWGN", key="fec_awgn_run"):

        result = run_fec_awgn(
            num_bits=fec_bits,
            esn0_db=fec_esn0,
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Coded-Bit BER",
            f"{result['coded_ber']:.6f}",
        )

        c2.metric(
            "Decoded Information BER",
            f"{result['decoded_ber']:.6f}",
        )

        st.write(
            "Information bits:",
            result["num_bits"]
        )

        st.write(
            "Coded bits:",
            result["coded_bits"]
        )

        st.write(
            "Coded-bit errors:",
            result["coded_errors"]
        )

        st.write(
            "Errors after FEC:",
            result["decoded_errors"]
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            ["Before Decoding", "After Decoding"],
            [
                result["coded_ber"],
                result["decoded_ber"],
            ],
        )

        ax.set_title("BER Before and After FEC")
        ax.set_ylabel("Bit Error Rate")

        ax.grid(True, axis="y", alpha=0.3)

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "These BER measurements have different "
            "denominators and do not alone demonstrate "
            "an energy-efficiency improvement."
        )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 3: REPETITION-3 FEC
    # --------------------------------------------------------

    st.subheader("Experiment 3: Repetition-3 FEC")

    message = st.text_input(
        "Enter binary information",
        value="10110",
        key="fec_message",
    )

    if st.button(
        "Run FEC Demonstration",
        key="fec_demo_run",
    ):

        if not message or any(
            ch not in "01" for ch in message
        ):
            st.error("Enter only binary digits 0 and 1.")

        else:

            original = np.array([
                int(ch) for ch in message
            ])

            encoded = np.repeat(original, 3)

            received = encoded.copy()

            received[1::3] ^= 1

            decoded = (
                received.reshape(-1, 3).sum(axis=1) >= 2
            ).astype(int)

            st.write("Original:", message)

            st.write(
                "Encoded:",
                "".join(map(str, encoded)),
            )

            st.write(
                "Received:",
                "".join(map(str, received)),
            )

            st.write(
                "Decoded:",
                "".join(map(str, decoded)),
            )

            c1, c2 = st.columns(2)

            c1.metric(
                "Coded Errors",
                int(np.count_nonzero(encoded != received)),
            )

            c2.metric(
                "Errors After FEC",
                int(np.count_nonzero(original != decoded)),
            )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 4: BER VS Eb/N0
    # --------------------------------------------------------

    st.subheader("Experiment 4: BER vs Eb/N0")

    analysis_bits = st.slider(
        "Bits for BER Analysis",
        10000, 500000, 100000,
        step=10000,
        key="ber_analysis_bits",
    )

    if st.button(
        "Run BER Analysis",
        key="ber_analysis_run",
    ):

        snr_values, ber_values = run_ber_snr_analysis(
            num_bits=analysis_bits
        )

        for snr_value, ber_value in zip(
            snr_values, ber_values
        ):
            st.write(
                f"Eb/N0 = {snr_value} dB | "
                f"BER = {ber_value:.6f}"
            )

        snr_array = np.asarray(snr_values, dtype=float)
        ber_array = np.asarray(ber_values, dtype=float)

        valid = ber_array > 0

        fig, ax = plt.subplots(figsize=(9, 4))

        if np.any(valid):

            ax.semilogy(
                snr_array[valid],
                ber_array[valid],
                "o-",
                label="Simulated BER",
            )

            ax.legend()

        else:
            st.warning("No bit errors were observed.")

        ax.set_title("BER vs Eb/N0")
        ax.set_xlabel("Eb/N0 (dB)")
        ax.set_ylabel("Bit Error Rate")

        ax.grid(True, which="both")

        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# MODULE 2: WIRELESS LINK ANALYZER
# ============================================================

elif selected_module == "Wireless Link Analyzer":

    st.header("Wireless Channel Analyzer")

    st.write(
        "Analyze an idealized aircraft-to-ground "
        "radio communication link."
    )

    distance = st.slider(
        "Aircraft Distance (km)",
        1, 100, 10,
        key="wireless_distance",
    )

    frequency = st.number_input(
        "Frequency (MHz)",
        min_value=1.0,
        value=120.0,
        key="wireless_frequency",
    )

    transmit_power = st.slider(
        "Transmit Power (dBm)",
        0, 50, 30,
        key="wireless_power",
    )

    bandwidth = st.number_input(
        "Receiver Bandwidth (Hz)",
        min_value=1,
        value=25000,
        key="wireless_bandwidth",
    )

    noise_figure = st.slider(
        "Noise Figure (dB)",
        0, 20, 5,
        key="wireless_noise_figure",
    )

    required_snr = st.slider(
        "Assumed Required SNR (dB)",
        0, 30, 10,
        key="wireless_required_snr",
    )

    # WIRELESS CALCULATIONS

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

    st.subheader("Wireless Link Results")

    c1, c2 = st.columns(2)

    c1.metric(
        "FSPL",
        f"{fspl:.2f} dB"
    )

    c2.metric(
        "Received Power",
        f"{received_power:.2f} dBm"
    )

    c3, c4 = st.columns(2)

    c3.metric(
        "SNR",
        f"{snr:.2f} dB"
    )

    c4.metric(
        "Link Margin",
        f"{margin:.2f} dB"
    )

    st.write(
        "Estimated receiver noise:",
        f"{noise_power:.2f} dBm"
    )

    st.write(
        "Educational SNR quality:",
        interpret_link_quality(snr)
    )

    if margin >= 0:
        st.success("Assumed SNR requirement satisfied.")
    else:
        st.warning("Assumed SNR requirement not satisfied.")

    st.caption(
        "Ideal free-space model with zero antenna gains "
        "and additional losses. Thresholds are illustrative."
    )

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
        ("Link Margin", graph_margin, "Margin (dB)"),
    ]

    for title, values, label in graphs:

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            graph_distances,
            values,
            label=title,
        )

        ax.axvline(
            distance,
            linestyle="--",
            label="Selected Distance",
        )

        if title == "Link Margin":
            ax.axhline(
                0,
                linestyle=":",
                label="Zero Margin",
            )

        ax.set_title(f"{title} vs Distance")
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel(label)

        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# MODULE 3: NETWORK MONITOR
# ============================================================

elif selected_module == "Network Monitor":

    st.header("Network Quality Monitor")

    st.write(
        "Simulate packet delivery between a ground station "
        "and an airport monitoring center."
    )

    packets = st.slider(
        "Number of Packets",
        100, 1000, 100,
        step=100,
        key="network_packets",
    )

    latency = st.slider(
        "Base One-way Latency (ms)",
        10, 200, 40,
        key="network_latency",
    )

    delay_std = st.slider(
        "Delay Variation (ms)",
        0, 100, 10,
        key="network_delay_std",
    )

    loss = st.slider(
        "Packet Loss Probability (%)",
        0, 30, 2,
        key="network_loss",
    )

    duration = st.slider(
        "Observation Duration (seconds)",
        1, 60, 10,
        key="network_duration",
    )

    packet_size = st.number_input(
        "Packet Size (bytes)",
        min_value=1,
        value=1000,
        key="network_packet_size",
    )

    if st.button(
        "Run Network Simulation",
        key="network_run",
    ):

        result = simulate_network(
            num_packets=packets,
            base_latency_ms=latency,
            jitter_std_ms=delay_std,
            loss_probability=loss / 100,
            packet_size_bytes=packet_size,
            duration_seconds=duration,
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Average Latency",
            f"{result['average_latency_ms']:.2f} ms"
        )

        c2.metric(
            "Jitter",
            f"{result['jitter_ms']:.2f} ms"
        )

        c3, c4 = st.columns(2)

        c3.metric(
            "Packet Loss",
            f"{result['packet_loss_percent']:.2f}%"
        )

        c4.metric(
            "Throughput",
            f"{result['throughput_mbps']:.4f} Mbps"
        )

        st.write(
            "Sent:",
            result["packets_sent"]
        )

        st.write(
            "Received:",
            result["packets_received"]
        )

        st.write(
            "Lost:",
            result["packets_lost"]
        )

        delays = result["received_delays"]

        if delays:

            fig, ax = plt.subplots(figsize=(9, 4))

            ax.plot(delays)

            ax.set_title("Simulated Packet Delay")
            ax.set_xlabel("Received Packet Index")
            ax.set_ylabel("Delay (ms)")

            ax.grid(True)

            st.pyplot(fig)
            plt.close(fig)

        else:
            st.warning("No packets were received.")

        st.caption(
            "Synthetic packet-network simulation, "
            "not live airport network monitoring."
        )


# ============================================================
# MODULE 4: AIRCRAFT SURVEILLANCE SIMULATOR
# ============================================================

elif selected_module == "Aircraft Surveillance Simulator":

    st.header("Aircraft Surveillance Simulator")

    st.info(
        "Synthetic aircraft positions rather than "
        "real radar or ADS-B data."
    )

    st.subheader("Experiment 1: Aircraft Information")

    aircraft_id = st.text_input(
        "Aircraft Identifier",
        value="AN101",
        key="aircraft_id",
    )

    latitude = st.number_input(
        "Initial Latitude",
        -90.0, 90.0, 27.70,
        format="%.5f",
        key="aircraft_lat",
    )

    longitude = st.number_input(
        "Initial Longitude",
        -180.0, 180.0, 85.35,
        format="%.5f",
        key="aircraft_lon",
    )

    altitude = st.number_input(
        "Altitude (meters)",
        0, 20000, 3000,
        key="aircraft_alt",
    )

    speed = st.slider(
        "Ground Speed (km/h)",
        0, 900, 360,
        step=10,
        key="aircraft_speed",
    )

    heading = st.slider(
        "Track Direction (degrees)",
        0, 359, 90,
        key="aircraft_heading",
    )

    st.caption(
        "0° = North, 90° = East, "
        "180° = South, 270° = West."
    )

    st.divider()

    st.subheader("Experiment 2: Aircraft Movement")

    time_step = st.slider(
        "Position Update Interval (seconds)",
        5, 60, 10,
        step=5,
        key="aircraft_time_step",
    )

    updates = st.slider(
        "Number of Updates",
        1, 30, 6,
        key="aircraft_updates",
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
        key="aircraft_simulate",
    ):

        try:

            aircraft = create_aircraft(
                aircraft_id=aircraft_id,
                latitude=latitude,
                longitude=longitude,
                altitude_m=altitude,
                speed_kmh=speed,
                heading_deg=heading,
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
                    "heading_deg": aircraft["heading_deg"],
                })

            df = pd.DataFrame(trajectory)

            st.subheader("Experiment 3: Tracking Results")

            c1, c2, c3 = st.columns(3)

            c1.metric("Aircraft ID", aircraft_id)

            c2.metric(
                "Ground Speed",
                f"{speed} km/h"
            )

            c3.metric(
                "Track Direction",
                f"{heading}°"
            )

            c4, c5, c6 = st.columns(3)

            c4.metric(
                "Altitude",
                f"{altitude} m"
            )

            c5.metric(
                "Travel Distance",
                f"{travel_distance:.2f} km"
            )

            c6.metric(
                "Elapsed Time",
                f"{total_seconds} s"
            )

            st.write(
                "Final Latitude:",
                f"{aircraft['latitude']:.5f}°"
            )

            st.write(
                "Final Longitude:",
                f"{aircraft['longitude']:.5f}°"
            )

            st.subheader("Experiment 4: Aircraft Positions")

            st.map(
                df,
                latitude="latitude",
                longitude="longitude",
            )

            st.dataframe(
                df,
                use_container_width=True,
            )

            for field, label in [
                ("latitude", "Latitude"),
                ("longitude", "Longitude"),
            ]:

                fig, ax = plt.subplots(figsize=(9, 4))

                ax.plot(
                    df["time_seconds"],
                    df[field],
                    "o-",
                )

                ax.set_title(
                    f"Aircraft {label} vs Time"
                )

                ax.set_xlabel("Time (seconds)")
                ax.set_ylabel(label)

                ax.grid(True)

                st.pyplot(fig)
                plt.close(fig)

            st.success(
                "Aircraft simulation completed."
            )

            st.caption(
                "Constant speed, heading, and altitude; "
                "approximate geographic updates."
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
        "recovery time, and service availability."
    )

    st.subheader("Experiment 1: Link Selection")

    primary_available = st.checkbox(
        "Primary Link Available",
        value=True,
        key="reliability_primary_available",
    )

    backup_available = st.checkbox(
        "Backup Link Available",
        value=True,
        key="reliability_backup_available",
    )

    selection = simulate_failover(
        primary_available=primary_available,
        backup_available=backup_available,
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Active Link",
        selection["active_link"]
    )

    c2.metric(
        "System Status",
        selection["status"]
    )

    if selection["status"] == "Communication Unavailable":

        st.error(
            "Neither communication link is available."
        )

    elif selection["status"] == "Failover Active":

        st.warning(
            "Primary failed; backup link selected."
        )

    else:

        st.success(
            "Primary link is operational."
        )

    st.divider()

    st.subheader(
        "Experiment 2: Recovery Time and Availability"
    )

    st.caption(
        "This separate recovery experiment assumes "
        "the backup link is available."
    )

    total_time = st.slider(
        "Observation Duration (seconds)",
        10, 300, 60,
        step=10,
        key="reliability_total_time",
    )

    failure_time = st.slider(
        "Primary Failure Time (seconds)",
        0, total_time,
        min(30, total_time),
        key="reliability_failure_time",
    )

    failover_delay = st.slider(
        "Backup Activation Delay (seconds)",
        0, 60, 5,
        key="reliability_failover_delay",
    )

    if st.button(
        "Run Failover Simulation",
        key="run_reliability_simulation",
    ):

        result = simulate_recovery(
            total_time=total_time,
            failure_time=failure_time,
            failover_delay=failover_delay,
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Communication Downtime",
            f"{result['downtime']:.2f} s"
        )

        c2.metric(
            "Observed Availability",
            f"{result['availability']:.2f}%"
        )

        c3, c4 = st.columns(2)

        c3.metric(
            "Failure Time",
            f"{result['failure_time']} s"
        )

        c4.metric(
            "Backup Recovery Time",
            f"{result['recovery_time']} s"
        )

        st.write(
            "Communication Uptime:",
            f"{result['uptime']:.2f} seconds"
        )

        st.subheader(
            "Experiment 3: Failover Timeline"
        )

        fig = plot_failover_timeline(result)

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "Deterministic educational model. "
            "Observed availability is not long-term reliability."
        )


# ============================================================
# MODULE 6: COMPLETE INTEGRATED SYSTEM SIMULATION
# ============================================================

elif selected_module == "Integrated System Simulation":

    st.header("Integrated Communication and Surveillance")

    st.write(
        "Study aircraft movement, 3D slant range, "
        "wireless propagation, BPSK error probability, "
        "packet delivery, and failover."
    )

    st.info(
        "This is an educational synthetic model. "
        "The results do not represent live airport data. "
        "Assumptions include independent bit errors, "
        "simplified receiver noise, and a working backup link."
    )

    # --------------------------------------------------------
    # SIMULATION SETTINGS
    # --------------------------------------------------------

    st.subheader("Simulation Settings")

    col1, col2 = st.columns(2)

    with col1:

        time_step = st.slider(
            "Update Interval (seconds)",
            1, 20, 5,
            key="integrated_time_step",
        )

        number_updates = st.slider(
            "Number of Updates",
            5, 60, 12,
            key="integrated_updates",
        )

        attenuation = st.slider(
            "Additional Attenuation (dB)",
            0, 80, 50,
            key="integrated_attenuation",
        )

    with col2:

        failure_time = st.slider(
            "Primary Failure Time (seconds)",
            0,
            time_step * number_updates,
            min(30, time_step * number_updates),
            key="integrated_failure_time",
        )

        backup_delay = st.slider(
            "Backup Activation Delay (seconds)",
            0, 30, 5,
            key="integrated_backup_delay",
        )

        packets_per_update = st.slider(
            "Packets Per Update",
            10, 1000, 100,
            step=10,
            key="integrated_packets",
        )

    st.caption(
        "The radio model uses a fixed ground station, "
        "constant aircraft motion, theoretical coherent "
        "BPSK BER, and a configurable attenuation value."
    )

    # --------------------------------------------------------
    # RUN COMPLETE INTEGRATED EXPERIMENTS
    # --------------------------------------------------------

    if st.button(
        "Run Complete Integrated Simulation",
        key="run_complete_integrated",
    ):

        try:

            results = run_integrated_simulation(
                time_step=time_step,
                number_updates=number_updates,
                additional_attenuation_db=attenuation,
                primary_failure_time=failure_time,
                backup_activation_delay=backup_delay,
                packets_per_update=packets_per_update,
            )

            df = pd.DataFrame(results)

            required_columns = [
                "time_seconds",
                "latitude",
                "longitude",
                "distance_km",
                "fspl_db",
                "received_power_dbm",
                "snr_db",
                "active_link",
                "packets_sent",
                "packets_received",
                "packets_lost",
                "packet_loss_percent",
            ]

            if df.empty or any(
                column not in df.columns
                for column in required_columns
            ):

                st.error(
                    "The integrated simulation did not "
                    "return the expected results."
                )

            else:

                st.success(
                    "Integrated simulation completed!"
                )

                # ------------------------------------------------
                # PACKET SUMMARY
                # ------------------------------------------------

                total_sent = int(
                    df["packets_sent"].sum()
                )

                total_received = int(
                    df["packets_received"].sum()
                )

                total_lost = int(
                    df["packets_lost"].sum()
                )

                delivery_percent = (
                    100 * total_received / total_sent
                )

                st.subheader(
                    "Aircraft and Communication Results"
                )

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Final Slant Range",
                    f"{df['distance_km'].iloc[-1]:.2f} km",
                )

                c2.metric(
                    "Packets Received",
                    total_received,
                )

                c3.metric(
                    "Overall Packet Delivery",
                    f"{delivery_percent:.2f}%",
                )

                c4, c5, c6 = st.columns(3)

                c4.metric(
                    "Packets Sent",
                    total_sent,
                )

                c5.metric(
                    "Packets Lost",
                    total_lost,
                )

                c6.metric(
                    "Backup Activation",
                    f"{failure_time + backup_delay} s",
                )

                # ------------------------------------------------
                # RESULTS TABLE
                # ------------------------------------------------

                st.subheader("Engineering Results Table")

                st.dataframe(
                    df,
                    use_container_width=True,
                )

                # ------------------------------------------------
                # AIRCRAFT MAP
                # ------------------------------------------------

                st.subheader("Aircraft Position Map")

                st.map(
                    df,
                    latitude="latitude",
                    longitude="longitude",
                )

                # ------------------------------------------------
                # INTEGRATED GRAPHS
                # ------------------------------------------------

                st.subheader(
                    "Integrated Performance Graphs"
                )

                figures = plot_integrated_results(results)

                for fig in figures:

                    st.pyplot(fig)
                    plt.close(fig)

                st.caption(
                    "Packet delivery is sampled at discrete "
                    "simulation updates. The model does not "
                    "yet include continuous packet traffic "
                    "or realistic network latency and jitter."
                )

                # ------------------------------------------------
                # ENGINEERING INTERPRETATION
                # ------------------------------------------------

                st.subheader("Engineering Interpretation")

                st.write(
                    "Aircraft movement changes the estimated "
                    "slant range, free-space path loss, "
                    "received power, and SNR."
                )

                st.write(
                    "The theoretical BPSK model estimates "
                    "bit-error probability from an assumed "
                    "relationship between SNR and Eb/N0."
                )

                st.write(
                    "The packet model uses the estimated "
                    "error probability to simulate successful "
                    "and unsuccessful packet delivery."
                )

                st.write(
                    "During the simulated failover interruption, "
                    "packets at unavailable observation points "
                    "are not delivered."
                )

        except (
            ValueError,
            TypeError,
            KeyError,
            ImportError,
        ) as error:

            st.error(
                f"Integrated simulation error: {error}"
            )
