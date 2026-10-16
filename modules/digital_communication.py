
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Generate 10 random binary bits
bits = np.random.randint(0, 2, 10)

# Step 2: Convert binary bits into BPSK symbols
# 0 becomes -1 and 1 becomes +1
bpsk_symbols = 2 * bits - 1

# Step 3: Add Gaussian noise to BPSK symbols
noise_std = 0.5

noise = np.random.normal(
    loc=0,
    scale=noise_std,
    size=len(bpsk_symbols)
)

received_symbols = bpsk_symbols + noise

# Step 4: Recover bits at the receiver
received_bits = (received_symbols > 0).astype(int)

# Step 5: Calculate Bit Error Rate
errors = np.sum(bits != received_bits)
ber = errors / len(bits)

print("Received symbols:", received_symbols)
print("Recovered bits:", received_bits)
print("Number of bit errors:", errors)
print("BER:", ber)

# Step 6: Compare transmitted and received symbols
plt.figure(figsize=(10, 5))

plt.plot(bpsk_symbols, "o-", label="Transmitted")
plt.plot(received_symbols, "x--", label="Received")

plt.axhline(0, color="red", linestyle=":",
            label="Decision Boundary")

plt.xlabel("Symbol Index")
plt.ylabel("Amplitude")
plt.title("BPSK Transmission Through an AWGN Channel")
plt.legend()
plt.grid(True)

plt.show()

# Step 5: Recover binary bits from BPSK symbols
received_bits = (bpsk_symbols > 0).astype(int)

# Step 6: Compare transmitted and received bits
errors = np.sum(bits != received_bits)
ber = errors / len(bits)

print("Recovered bits:", received_bits)
print("Number of bit errors:", errors)
print("Bit Error Rate:", ber)