
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from modules.fec_awgn_experiment import run_fec_awgn
from modules.ber_snr_analysis_new import run_ber_snr_analysis


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

st.info("Version 0.1 | Educational Simulation")
st.write("Welcome to AeroLink Nepal!")


# ============================================================
# ENGINEERING MODULE SELECTION
# ============================================================

st.header("Engineering Modules")

modules = [
    "Digital Communication",
    "Network Monitor",
    "Wireless Link Analyzer",
    "Aircraft Surveillance Simulator",
    "Reliability and Failover"
]

selected_module = st.selectbox(
    "Choose a module:",
    modules,
    key="engineering_module_selection"
)

st.success(f"Selected Module: {selected_module}")


# ============================================================
# MODULE 1: DIGITAL COMMUNICATION
# ============================================================

if selected_module == "Digital Communication":

    st.header("Digital Communication Simulator")

    st.write(
        "Explore BPSK modulation, AWGN noise, "
        "Bit Error Rate, and Forward Error Correction."
    )

    # --------------------------------------------------------
    # EXPERIMENT 1: BPSK THROUGH AWGN
    # --------------------------------------------------------

    st.subheader("Experiment 1: BPSK Through AWGN")

    number_of_bits = st.slider(
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

    st.write("Transmitted bits:", number_of_bits)
    st.write("Selected Eb/N0:", ebn0_db, "dB")

    if st.button(
        "Run BPSK Simulation",
        key="run_bpsk_button"
    ):

        # Generate random bits
        bits = np.random.randint(0, 2, number_of_bits)

        # BPSK mapping: 0 -> -1, 1 -> +1
        symbols = 2 * bits - 1

        # Convert Eb/N0 from dB
        ebn0_linear = 10 ** (ebn0_db / 10)

        # AWGN standard deviation
        noise_std = np.sqrt(1 / (2 * ebn0_linear))

        noise = np.random.normal(
            0,
            noise_std,
            number_of_bits
        )

        received = symbols + noise

        # Hard-decision demodulation
        detected_bits = (received > 0).astype(int)

        errors = int(np.count_nonzero(bits != detected_bits))
        ber = errors / number_of_bits

        st.subheader("BPSK Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Transmitted Bits", number_of_bits)
        col2.metric("Bit Errors", errors)
        col3.metric("BER", f"{ber:.6f}")

        # Plot first 30 symbols
        sample_count = min(30, number_of_bits)

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            symbols[:sample_count],
            "o-",
            label="Transmitted"
        )

        ax.plot(
            received[:sample_count],
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

        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 2: FEC PERFORMANCE UNDER AWGN
    # --------------------------------------------------------

    st.subheader("Experiment 2: FEC Performance Under AWGN")

    st.write(
        "Study repetition-3 FEC coding through a noisy "
        "BPSK communication channel."
    )

    fec_bits = st.slider(
        "Number of information bits",
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        key="fec_awgn_bits"
    )

    fec_esn0 = st.slider(
        "Channel Es/N0 (dB)",
        min_value=0,
        max_value=10,
        value=0,
        key="fec_awgn_esn0"
    )

    if st.button(
        "Run FEC + AWGN Experiment",
        key="run_fec_awgn_button"
    ):

        results = run_fec_awgn(
            num_bits=fec_bits,
            esn0_db=fec_esn0
        )

        st.subheader("FEC + AWGN Results")

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
            ["Before FEC Decoding", "After FEC Decoding"],
            [
                results["coded_ber"],
                results["decoded_ber"]
            ]
        )

        ax.set_title("BER Before and After FEC Decoding")
        ax.set_ylabel("Bit Error Rate")
        ax.set_ylim(
            0,
            max(
                results["coded_ber"],
                results["decoded_ber"],
                0.001
            ) * 1.2
        )
        ax.grid(True, axis="y", alpha=0.3)

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "The coded-bit and decoded information-bit BER "
            "use different denominators. This comparison "
            "demonstrates decoding, not a fair comparison "
            "of coded versus uncoded energy efficiency."
        )

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 3: MANUAL FEC DEMONSTRATION
    # --------------------------------------------------------

    st.subheader("Experiment 3: Forward Error Correction (FEC)")

    st.write(
        "Demonstration of repetition-3 encoding "
        "and majority-vote decoding."
    )

    message = st.text_input(
        "Enter binary information:",
        value="10110",
        key="fec_binary_message"
    )

    if st.button(
        "Run FEC Simulation",
        key="fec_run_button"
    ):

        if not message or any(bit not in "01" for bit in message):

            st.error(
                "Please enter only binary digits (0 and 1)."
            )

        else:

            original_bits = np.array(
                [int(bit) for bit in message]
            )

            # FEC encoding
            encoded_bits = np.repeat(original_bits, 3)

            # Flip one bit in every three-bit group
            received_bits = encoded_bits.copy()

            error_positions = np.arange(
                1,
                len(encoded_bits),
                3
            )

            received_bits[error_positions] ^= 1

            # Majority-vote decoding
            groups = received_bits.reshape(-1, 3)

            decoded_bits = (
                groups.sum(axis=1) >= 2
            ).astype(int)

            errors_before = int(np.count_nonzero(
                encoded_bits != received_bits
            ))

            errors_after = int(np.count_nonzero(
                original_bits != decoded_bits
            ))

            st.subheader("FEC Demonstration Results")

            st.write("Original message:", message)

            st.write(
                "Encoded bits:",
                "".join(map(str, encoded_bits))
            )

            st.write(
                "Received bits:",
                "".join(map(str, received_bits))
            )

            st.write(
                "Decoded message:",
                "".join(map(str, decoded_bits))
            )

            col1, col2 = st.columns(2)

            col1.metric("Coded Bit Errors", errors_before)
            col2.metric("Errors After FEC", errors_after)

    st.divider()

    # --------------------------------------------------------
    # EXPERIMENT 4: BER VS SNR ANALYSIS
    # --------------------------------------------------------

    st.subheader("Experiment 4: BER vs SNR Analysis")

    st.write(
        "Study how Bit Error Rate changes with Eb/N0 "
        "for BPSK transmission over AWGN."
    )

    snr_bits = st.slider(
        "Number of bits for BER analysis",
        min_value=10000,
        max_value=500000,
        value=100000,
        step=10000,
        key="ber_snr_bits"
    )

    if st.button(
        "Run BER vs SNR Analysis",
        key="run_ber_snr_button"
    ):

        snr_values, ber_values = run_ber_snr_analysis(
            num_bits=snr_bits
        )

        st.subheader("BER vs Eb/N0 Results")

        for snr, ber in zip(snr_values, ber_values):
            st.write(
                f"Eb/N0: {snr} dB | BER: {ber:.6f}"
            )

        snr_array = np.asarray(snr_values, dtype=float)
        ber_array = np.asarray(ber_values, dtype=float)

        positive_mask = ber_array > 0

        fig, ax = plt.subplots(figsize=(9, 5))

        if np.any(positive_mask):

            ax.semilogy(
                snr_array[positive_mask],
                ber_array[positive_mask],
                "o-",
                label="Simulated BPSK BER"
            )

            ax.legend()

        else:

            st.warning(
                "No bit errors were observed at the "
                "selected SNR values."
            )

        ax.set_title("BER vs Eb/N0 for BPSK over AWGN")
        ax.set_xlabel("Eb/N0 (dB)")
        ax.set_ylabel("Bit Error Rate (BER)")
        ax.grid(True, which="both", alpha=0.3)

        st.pyplot(fig)
        plt.close(fig)

        st.caption(
            "Zero observed BER values are omitted from "
            "the logarithmic plot because log(0) "
            "is undefined."
        )


# ============================================================
# MODULE 2: WIRELESS LINK ANALYZER
# ============================================================

elif selected_module == "Wireless Link Analyzer":

    from modules.wireless_link import (
        calculate_fspl,
        calculate_received_power,
        calculate_noise_power,
        calculate_snr,
        calculate_link_margin,
        interpret_link_quality
    )

    st.header("Wireless Channel Analyzer")

    st.write(
        "Explore a simulated aircraft-to-ground radio link. "
        "Analyze free-space path loss, received power, "
        "receiver noise, SNR and link margin."
    )

    st.subheader("Radio Link Parameters")

    distance_km = st.slider(
        "Aircraft distance (km)",
        min_value=1,
        max_value=100,
        value=10,
        key="wireless_distance_km"
    )

    frequency_mhz = st.number_input(
        "Operating frequency (MHz)",
        min_value=1.0,
        value=120.0,
        step=1.0,
        key="wireless_frequency_mhz"
    )

    transmit_power_dbm = st.slider(
        "Transmit power (dBm)",
        min_value=0,
        max_value=50,
        value=30,
        key="wireless_transmit_power_dbm"
    )

    bandwidth_hz = st.number_input(
        "Receiver noise bandwidth (Hz)",
        min_value=1,
        value=25000,
        step=1000,
        key="wireless_bandwidth_hz"
    )

    noise_figure_db = st.slider(
        "Receiver noise figure (dB)",
        min_value=0,
        max_value=20,
        value=5,
        key="wireless_noise_figure_db"
    )

    required_snr_db = st.slider(
        "Assumed required SNR (dB)",
        min_value=0,
        max_value=30,
        value=10,
        key="wireless_required_snr_db"
    )

    # --------------------------------------------------------
    # WIRELESS LINK CALCULATIONS
    # --------------------------------------------------------

    fspl_db = calculate_fspl(
        distance_km,
        frequency_mhz
    )

    received_power_dbm = calculate_received_power(
        transmit_power_dbm=transmit_power_dbm,
        distance_km=distance_km,
        frequency_mhz=frequency_mhz
    )

    noise_power_dbm = calculate_noise_power(
        bandwidth_hz=bandwidth_hz,
        noise_figure_db=noise_figure_db
    )

    snr_db = calculate_snr(
        received_power_dbm,
        noise_power_dbm
    )

    link_margin_db = calculate_link_margin(
        snr_db,
        required_snr_db
    )

    link_quality = interpret_link_quality(snr_db)

    # --------------------------------------------------------
    # WIRELESS LINK RESULTS
    # --------------------------------------------------------

    st.subheader("Calculated Wireless Link Results")

    col1, col2 = st.columns(2)

    col1.metric(
        "Free-space path loss",
        f"{fspl_db:.2f} dB"
    )

    col2.metric(
        "Received power",
        f"{received_power_dbm:.2f} dBm"
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "Signal-to-noise ratio",
        f"{snr_db:.2f} dB"
    )

    col4.metric(
        "SNR link margin",
        f"{link_margin_db:.2f} dB"
    )

    st.write(
        "Estimated receiver noise power:",
        f"{noise_power_dbm:.2f} dBm"
    )

    st.write(
        "Educational SNR interpretation:",
        link_quality
    )

    if link_margin_db >= 0:

        st.success(
            "The assumed SNR requirement is satisfied in this model."
        )

    else:

        st.warning(
            "The assumed SNR requirement is not satisfied in this model."
        )

    st.caption(
        "This is an educational free-space model with zero "
        "antenna gains and additional losses. The thresholds "
        "are illustrative, not aviation communication standards."
    )

    # --------------------------------------------------------
    # WIRELESS LINK GRAPHS
    # --------------------------------------------------------

    st.subheader("Wireless Link Performance vs Distance")

    graph_distances = list(range(1, 101))

    graph_fspl = [
        calculate_fspl(d, frequency_mhz)
        for d in graph_distances
    ]

    graph_received_power = [
        calculate_received_power(
            transmit_power_dbm,
            d,
            frequency_mhz
        )
        for d in graph_distances
    ]

    graph_snr = [
        calculate_snr(power, noise_power_dbm)
        for power in graph_received_power
    ]

    graph_margin = [
        calculate_link_margin(snr, required_snr_db)
        for snr in graph_snr
    ]

    wireless_graphs = [
        (
            "Free-space path loss",
            graph_fspl,
            "Path loss (dB)"
        ),
        (
            "Received power",
            graph_received_power,
            "Received power (dBm)"
        ),
        (
            "SNR",
            graph_snr,
            "SNR (dB)"
        ),
        (
            "Link margin",
            graph_margin,
            "Margin (dB)"
        )
    ]

    for graph_title, graph_values, y_label in wireless_graphs:

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            graph_distances,
            graph_values,
            label=graph_title
        )

        ax.axvline(
            distance_km,
            linestyle="--",
            label=f"Selected distance: {distance_km} km"
        )

        if graph_title == "Link margin":

            ax.axhline(
                0,
                linestyle=":",
                label="Zero margin"
            )

        ax.set_title(f"{graph_title} vs Distance")
        ax.set_xlabel("Aircraft-to-ground distance (km)")
        ax.set_ylabel(y_label)
        ax.grid(True, alpha=0.3)
        ax.legend()

        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)


# ============================================================
# MODULE 3: NETWORK QUALITY MONITOR
# ============================================================

elif selected_module == "Network Monitor":

    from modules.network_monitor import simulate_network

    st.header("Network Quality Monitor")

    st.write(
        "Simulate data packet delivery between an airport "
        "ground station and a monitoring center."
    )

    st.subheader("Network Simulation Settings")

    # --------------------------------------------------------
    # NETWORK INPUT PARAMETERS
    # --------------------------------------------------------

    num_packets = st.slider(
        "Number of packets",
        min_value=100,
        max_value=1000,
        value=100,
        step=100,
        key="network_packets"
    )

    base_latency_ms = st.slider(
        "Base one-way latency (ms)",
        min_value=10,
        max_value=200,
        value=40,
        key="network_latency"
    )

    jitter_std_ms = st.slider(
        "Delay variation standard deviation (ms)",
        min_value=0,
        max_value=100,
        value=10,
        key="network_jitter_std"
    )

    loss_percent = st.slider(
        "Packet loss probability (%)",
        min_value=0,
        max_value=30,
        value=2,
        key="network_loss"
    )

    duration_seconds = st.slider(
        "Observation duration (seconds)",
        min_value=1,
        max_value=60,
        value=10,
        key="network_duration"
    )

    packet_size_bytes = st.number_input(
        "Packet size (bytes)",
        min_value=1,
        value=1000,
        step=100,
        key="network_packet_size"
    )

    # --------------------------------------------------------
    # RUN NETWORK SIMULATION
    # --------------------------------------------------------

    if st.button(
        "Run Network Simulation",
        key="run_network_simulation"
    ):

        results = simulate_network(
            num_packets=num_packets,
            base_latency_ms=base_latency_ms,
            jitter_std_ms=jitter_std_ms,
            loss_probability=loss_percent / 100,
            packet_size_bytes=packet_size_bytes,
            duration_seconds=duration_seconds
        )

        st.subheader("Network Performance Results")

        # ----------------------------------------------------
        # PERFORMANCE METRICS
        # ----------------------------------------------------

        col1, col2 = st.columns(2)

        col1.metric(
            "Average Latency",
            f"{results['average_latency_ms']:.2f} ms"
        )

        col2.metric(
            "Jitter",
            f"{results['jitter_ms']:.2f} ms"
        )

        col3, col4 = st.columns(2)

        col3.metric(
            "Packet Loss",
            f"{results['packet_loss_percent']:.2f}%"
        )

        col4.metric(
            "Throughput",
            f"{results['throughput_mbps']:.4f} Mbps"
        )

        st.write(
            "Packets sent:",
            results["packets_sent"]
        )

        st.write(
            "Packets received:",
            results["packets_received"]
        )

        st.write(
            "Packets lost:",
            results["packets_lost"]
        )

        # ----------------------------------------------------
        # PACKET DELAY GRAPH
        # ----------------------------------------------------

        st.subheader("Packet Delay Visualization")

        delays = results["received_delays"]

        if len(delays) > 0:

            fig, ax = plt.subplots(figsize=(9, 4))

            ax.plot(
                range(1, len(delays) + 1),
                delays,
                label="Received Packet Delay"
            )

            ax.set_title(
                "Simulated One-way Packet Delay"
            )

            ax.set_xlabel("Received Packet Index")
            ax.set_ylabel("Packet Delay (ms)")
            ax.grid(True)
            ax.legend()

            fig.tight_layout()

            st.pyplot(fig)
            plt.close(fig)

        else:

            st.warning(
                "No packets were received during this simulation."
            )

        st.caption(
            "The Network Quality Monitor generates simulated "
            "packet delays and losses. It does not measure "
            "real airport network traffic. Jitter is calculated "
            "as mean absolute delay variation, and throughput "
            "uses successfully delivered payload bits divided "
            "by the observation duration."
        )


# ============================================================
# OTHER ENGINEERING MODULES
# ============================================================

else:

    st.info(
        f"{selected_module} is currently under development."
    )
