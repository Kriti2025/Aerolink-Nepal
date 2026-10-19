
import numpy as np


def run_ber_snr_analysis(num_bits=100000):

    rng = np.random.default_rng(42)

    # Generate random information bits
    bits = rng.integers(0, 2, num_bits)

    # Convert bits to BPSK symbols
    symbols = 2 * bits - 1

    # SNR values to analyze
    ebn0_values = np.arange(0, 11, 2)

    ber_results = []

    for ebn0_db in ebn0_values:

        # Convert Eb/N0 from dB to linear scale
        ebn0_linear = 10 ** (ebn0_db / 10)

        # Calculate noise standard deviation
        noise_std = np.sqrt(1 / (2 * ebn0_linear))

        # Add AWGN noise
        noise = rng.normal(
            0, noise_std, size=num_bits
        )

        received_symbols = symbols + noise

        # BPSK demodulation
        detected_bits = (
            received_symbols > 0
        ).astype(int)

        # Count errors
        bit_errors = np.count_nonzero(
            bits != detected_bits
        )

        # Calculate BER
        ber = bit_errors / num_bits

        ber_results.append(ber)

    return ebn0_values, ber_results


if __name__ == "__main__":

    snr, ber = run_ber_snr_analysis()

    for snr_value, ber_value in zip(snr, ber):
        print(
            f"Eb/N0: {snr_value} dB | BER: {ber_value:.6f}"
        )
