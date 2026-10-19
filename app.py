
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from modules.fec_awgn_experiment import run_fec_awgn
from modules.ber_snr_analysis_new import run_ber_snr_analysis


# ============================================================
# STREAMLIT PAGE CONFIGURATION
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
    modules
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

    # ========================================================
    # EXPERIMENT 1: BPSK THROUGH AWGN
    # ========================================================

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

        # Generate random information bits
        bits = np.random.randint(0, 2, number_of_bits)

        # BPSK modulation
        symbols = 2 * bits - 1

        # Convert Eb/N0 from dB to linear scale
        ebn0_linear = 10 ** (ebn0_db / 10)

        # Calculate AWGN standard deviation
        noise_std = np.sqrt(1 / (2 * ebn0_linear))

        # Add Gaussian noise
        noise = np.random.normal(
            0,
            noise_std,
            number_of_bits
        )

        received = symbols + noise

        # Hard-decision BPSK demodulation
        detected_bits = (received > 0).astype(int)

        # Calculate errors and BER
        errors = np.count_nonzero(bits != detected_bits)
        ber = errors / number_of_bits

        st.subheader("BPSK Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Transmitted Bits", number_of_bits)
        col2.metric("Bit Errors", int(errors))
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
            color="red",
            linestyle=":",
            label="Decision Boundary"
        )

        ax.set_title("BPSK Transmission Through AWGN")
        ax.set_xlabel("Symbol Index")
        ax.set_ylabel("Amplitude")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
        plt.close(fig)

    st.divider()

    # ========================================================
    # EXPERIMENT 2: FEC PERFORMANCE UNDER AWGN
    # ========================================================

    st.subheader(
        "Experiment 2: FEC Performance Under AWGN"
    )

    st.write(
        "Simulate repetition-3 error correction "
        "through a noisy BPSK channel."
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

        # BER comparison chart
        fig, ax = plt.subplots(figsize=(8, 4))

        ax.bar(
            ["Before FEC Decoding", "After FEC Decoding"],
            [
                results["coded_ber"],
                results["decoded_ber"]
            ]
        )

        ax.set_title(
            "BER Comparison: Before vs After FEC Decoding"
        )
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

    st.divider()

    # ========================================================
    # EXPERIMENT 3: MANUAL FEC DEMONSTRATION
    # ========================================================

    st.subheader(
        "Experiment 3: Forward Error Correction (FEC)"
    )

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

        if not message or any(
            bit not in "01" for bit in message
        ):
            st.error(
                "Please enter only binary digits (0 and 1)."
            )

        else:
            # Convert binary message to NumPy array
            original_bits = np.array(
                [int(bit) for bit in message]
            )

            # Repetition-3 encoding
            encoded_bits = np.repeat(original_bits, 3)

            # Introduce one bit error in every group
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

            # Count errors
            errors_before = np.count_nonzero(
                encoded_bits != received_bits
            )

            errors_after = np.count_nonzero(
                original_bits != decoded_bits
            )

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

            col1.metric(
                "Coded Bit Errors",
                int(errors_before)
            )

            col2.metric(
                "Errors After FEC",
                int(errors_after)
            )

    st.divider()

    # ========================================================
    # EXPERIMENT 4: BER VS SNR ANALYSIS
    # ========================================================

    st.subheader("Experiment 4: BER vs SNR Analysis")

    st.write(
        "Analyze how Bit Error Rate changes as Eb/N0 "
        "increases for BPSK communication over AWGN."
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

        # Run simulation from the modules folder
        snr_values, ber_values = run_ber_snr_analysis(
            num_bits=snr_bits
        )

        st.subheader("BER vs Eb/N0 Results")

        # Display numerical results
        for snr, ber in zip(snr_values, ber_values):
            st.write(
                f"Eb/N0: {snr} dB | BER: {ber:.6f}"
            )

        # Convert results for plotting
        snr_array = np.asarray(snr_values, dtype=float)
        ber_array = np.asarray(ber_values, dtype=float)

        # A logarithmic axis cannot display zero BER
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
                "selected SNR values. Try increasing "
                "the number of bits."
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
# OTHER ENGINEERING MODULES
# ============================================================

else:
    st.info(
        f"{selected_module} is currently under development."
    )
 