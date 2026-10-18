
import numpy as np


def run_fec_awgn(num_bits=10000, esn0_db=0):
    """
    Simulate Repetition-3 FEC with BPSK over an AWGN channel.
    Return error counts and bit error rates.
    """

    # Validate inputs
    num_bits = int(num_bits)
    esn0_db = float(esn0_db)

    if num_bits <= 0:
        raise ValueError("num_bits must be greater than zero.")

    if not np.isfinite(esn0_db):
        raise ValueError("esn0_db must be a finite number.")

    rng = np.random.default_rng()

    # Step 1: Generate original information bits
    bits = rng.integers(0, 2, size=num_bits)

    # Step 2: Repetition-3 FEC encoding
    encoded_bits = np.repeat(bits, 3)

    # Step 3: BPSK modulation
    symbols = 2 * encoded_bits - 1

    # Step 4: Convert Es/N0 from dB to linear scale
    esn0_linear = 10 ** (esn0_db / 10)

    # Step 5: Calculate AWGN standard deviation
    noise_std = np.sqrt(1 / (2 * esn0_linear))

    # Step 6: Transmit symbols through AWGN channel
    noise = rng.normal(0, noise_std, size=len(symbols))
    received_symbols = symbols + noise

    # Step 7: Hard-decision BPSK demodulation
    received_bits = (received_symbols > 0).astype(int)

    # Step 8: Group received bits into sets of 3
    groups = received_bits.reshape(-1, 3)

    # Step 9: Majority-vote FEC decoding
    decoded_bits = (groups.sum(axis=1) >= 2).astype(int)

    # Step 10: Count bit errors
    coded_errors = np.count_nonzero(
        encoded_bits != received_bits
    )

    decoded_errors = np.count_nonzero(
        bits != decoded_bits
    )

    # Step 11: Calculate bit error rates
    coded_ber = coded_errors / len(encoded_bits)
    decoded_ber = decoded_errors / num_bits

    # Step 12: Return results
    return {
        "num_bits": num_bits,
        "coded_bits": len(encoded_bits),
        "coded_errors": int(coded_errors),
        "decoded_errors": int(decoded_errors),
        "coded_ber": float(coded_ber),
        "decoded_ber": float(decoded_ber)
    }


if __name__ == "__main__":
    results = run_fec_awgn()

    for name, value in results.items():
        print(f"{name}: {value}")
