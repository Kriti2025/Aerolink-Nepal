
import numpy as np

rng = np.random.default_rng(42)

# Original information
num_bits = 10000
bits = rng.integers(0, 2, num_bits)

# Repetition-3 FEC encoding
encoded_bits = np.repeat(bits, 3)

# BPSK mapping
symbols = 2 * encoded_bits - 1

# Set noise condition using Es/N0 for each coded symbol
esn0_db = 0
esn0_linear = 10 ** (esn0_db / 10)

noise_std = np.sqrt(1 / (2 * esn0_linear))

# AWGN channel
noise = rng.normal(0, noise_std, len(symbols))
received_symbols = symbols + noise

# Hard-decision BPSK demodulation
received_bits = (received_symbols > 0).astype(int)

# FEC majority-vote decoder
groups = received_bits.reshape(-1, 3)
decoded_bits = (groups.sum(axis=1) >= 2).astype(int)

# Calculate error rates
coded_errors = np.count_nonzero(
    encoded_bits != received_bits
)
decoded_errors = np.count_nonzero(
    bits != decoded_bits
)

coded_ber = coded_errors / len(encoded_bits)
decoded_ber = decoded_errors / num_bits

print("Original information bits:", num_bits)
print("Transmitted coded bits:", len(encoded_bits))
print("Es/N0:", esn0_db, "dB")
print("Coded-bit error rate:", coded_ber)
print("Decoded information-bit error rate:", decoded_ber)
print("Decoded information-bit errors:", decoded_errors)
