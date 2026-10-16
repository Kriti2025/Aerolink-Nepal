
import numpy as np

# Original message
original_bits = np.array([1, 0, 1, 1, 0])

# FEC encoding: repeat each bit three times
encoded_bits = np.repeat(original_bits, 3)

# Simulate bit errors during transmission
received_bits = encoded_bits.copy()

# Flip selected bits to model a noisy channel
error_positions = [1, 7, 13]

for position in error_positions:
    received_bits[position] ^= 1

# FEC decoding: majority voting
groups = received_bits.reshape(-1, 3)

decoded_bits = (groups.sum(axis=1) >= 2).astype(int)

# Calculate errors
channel_errors = np.count_nonzero(
    encoded_bits != received_bits
)

decoded_errors = np.count_nonzero(
    original_bits != decoded_bits
)

print("Original bits: ", original_bits)
print("Encoded bits:  ", encoded_bits)
print("Received bits: ", received_bits)
print("Decoded bits:  ", decoded_bits)
print("Channel bit errors:", channel_errors)
print("Errors after FEC:", decoded_errors)
