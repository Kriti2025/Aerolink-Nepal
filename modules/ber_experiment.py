
import numpy as np
import matplotlib.pyplot as plt
from math import erfc, sqrt

# Reproducible random numbers
rng = np.random.default_rng(42)

# Number of transmitted bits
num_bits = 100000

# Generate random bits (0 and 1)
bits = rng.integers(0, 2, num_bits)

# BPSK mapping: 0 -> -1, 1 -> +1
symbols = 2 * bits - 1

# Eb/N0 values in decibels
ebn0_db_values = np.arange(0, 11, 2)

simulated_ber = []
theoretical_ber = []

for ebn0_db in ebn0_db_values:

    # Convert dB to linear scale
    ebn0_linear = 10 ** (ebn0_db / 10)

    # AWGN standard deviation
    noise_std = np.sqrt(1 / (2 * ebn0_linear))

    # Generate Gaussian noise
    noise = rng.normal(0, noise_std, num_bits)

    # Receive noisy BPSK symbols
    received = symbols + noise

    # Recover binary bits
    detected_bits = (received > 0).astype(int)

    # Calculate BER
    errors = np.count_nonzero(bits != detected_bits)
    ber = errors / num_bits

    simulated_ber.append(ber)

    # Theoretical coherent BPSK BER in AWGN
    theory = 0.5 * erfc(sqrt(ebn0_linear))
    theoretical_ber.append(theory)

    print(
        f"Eb/N0 = {ebn0_db:2d} dB | "
        f"Errors = {errors:5d} | "
        f"BER = {ber:.6f}"
    )

# Plot results
plt.figure(figsize=(9, 5))

# Zero BER cannot be displayed on a log axis
simulated = np.array(simulated_ber)
valid = simulated > 0

plt.semilogy(
    ebn0_db_values[valid],
    simulated[valid],
    "o-",
    label="Simulated BER"
)

plt.semilogy(
    ebn0_db_values,
    theoretical_ber,
    "s--",
    label="Theoretical BER"
)

plt.xlabel("Eb/N0 (dB)")
plt.ylabel("Bit Error Rate (BER)")
plt.title("BPSK BER Performance in AWGN")
plt.grid(True, which="both")
plt.legend()
plt.show()
