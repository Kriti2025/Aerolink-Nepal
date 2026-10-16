
import streamlit as st

st.set_page_config(
    page_title="AeroLink Nepal",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AeroLink Nepal")
st.subheader("Airport Communication & Surveillance Network Simulator")

st.info("Version 0.1 | Educational Simulation")

st.write("Welcome to AeroLink Nepal!")

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


if selected_module == "Digital Communication":
    st.subheader("Digital Communication Simulator")

    st.write(
        "Explore BPSK modulation, AWGN noise, "
        "Bit Error Rate, and Forward Error Correction."
    )

    number_of_bits = st.slider(
        "Number of transmitted bits",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100
    )

    ebn0_db = st.slider(
        "Eb/N0 (dB)",
        min_value=0,
        max_value=12,
        value=6
    )

    st.write("Transmitted bits:", number_of_bits)
    st.write("Selected Eb/N0:", ebn0_db, "dB")
    
    if st.button("Run BPSK Simulation"):

        import numpy as np
        import matplotlib.pyplot as plt

        # Generate random binary data
        bits = np.random.randint(0, 2, number_of_bits)

        # BPSK modulation
        symbols = 2 * bits - 1

        # Convert Eb/N0 from dB to linear scale
        ebn0_linear = 10 ** (ebn0_db / 10)

        # Calculate the AWGN standard deviation
        noise_std = np.sqrt(1 / (2 * ebn0_linear))

        # Pass transmitted symbols through AWGN
        noise = np.random.normal(
            0, noise_std, number_of_bits
        )
        received = symbols + noise

        # BPSK receiver
        detected_bits = (received > 0).astype(int)

        # Calculate bit errors
        errors = np.count_nonzero(bits != detected_bits)
        ber = errors / number_of_bits

        st.subheader("Simulation Results")

        col1, col2, col3 = st.columns(3)

        col1.metric("Transmitted Bits", number_of_bits)
        col2.metric("Bit Errors", errors)
        col3.metric("BER", f"{ber:.6f}")

        # Plot first 30 symbols
        sample_count = min(30, number_of_bits)

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            symbols[:sample_count],
            "o-", label="Transmitted"
        )

        ax.plot(
            received[:sample_count],
            "x--", label="Received"
        )

        ax.axhline(
            0, color="red", linestyle=":",
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

    st.subheader("Forward Error Correction (FEC)")

    st.write(
        "Demonstration of repetition-3 encoding "
        "and majority-vote decoding."
    )

    message = st.text_input(
        "Enter binary information:",
        value="10110"
    )

    if st.button("Run FEC Simulation"):

        if not message or any(bit not in "01" for bit in message):
            st.error("Please enter only binary digits (0 and 1).")

        else:
            import numpy as np

            original_bits = np.array(
                [int(bit) for bit in message]
            )

            # FEC encoding
            encoded_bits = np.repeat(original_bits, 3)

            # Simulate one error in every three-bit group
            received_bits = encoded_bits.copy()
            error_positions = np.arange(
                1, len(encoded_bits), 3
            )

            received_bits[error_positions] ^= 1

            # FEC decoding using majority voting
            groups = received_bits.reshape(-1, 3)

            decoded_bits = (
                groups.sum(axis=1) >= 2
            ).astype(int)

            errors_before = np.count_nonzero(
                encoded_bits != received_bits
            )

            errors_after = np.count_nonzero(
                original_bits != decoded_bits
            )

            st.write("Original message:", message)
            st.write("Encoded bits:", encoded_bits.tolist())
            st.write("Received bits:", received_bits.tolist())
            st.write("Decoded message:", "".join(
                map(str, decoded_bits)
            ))

            col1, col2 = st.columns(2)

            col1.metric("Coded Bit Errors", errors_before)
            col2.metric("Errors After FEC", errors_after)
    
    st.divider()

    st.subheader("Forward Error Correction (FEC)")

    st.write(
        "Demonstration of repetition-3 encoding "
        "and majority-vote decoding."
    )

    
message = st.text_input(
    "Enter binary information:",
    value="10110",
    key="fec_binary_message"
)

if st.button("Run FEC Simulation", key="fec_run_button"):

        if not message or any(bit not in "01" for bit in message):
            st.error("Please enter only binary digits (0 and 1).")

        else:
            import numpy as np

            original_bits = np.array(
                [int(bit) for bit in message]
            )

            # FEC encoding
            encoded_bits = np.repeat(original_bits, 3)

            # Simulate one error in every three-bit group
            received_bits = encoded_bits.copy()
            error_positions = np.arange(
                1, len(encoded_bits), 3
            )

            received_bits[error_positions] ^= 1

            # FEC decoding using majority voting
            groups = received_bits.reshape(-1, 3)

            decoded_bits = (
                groups.sum(axis=1) >= 2
            ).astype(int)

            errors_before = np.count_nonzero(
                encoded_bits != received_bits
            )

            errors_after = np.count_nonzero(
                original_bits != decoded_bits
            )

            st.write("Original message:", message)
            st.write("Encoded bits:", encoded_bits.tolist())
            st.write("Received bits:", received_bits.tolist())
            st.write("Decoded message:", "".join(
                map(str, decoded_bits)
            ))

            col1, col2 = st.columns(2)

            col1.metric("Coded Bit Errors", errors_before)
            col2.metric("Errors After FEC", errors_after)

    
     

else:
    st.write("This module is currently under development.")

