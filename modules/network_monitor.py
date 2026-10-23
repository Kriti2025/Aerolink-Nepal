
import numpy as np


def simulate_network(
    num_packets=100,
    base_latency_ms=40,
    jitter_std_ms=10,
    loss_probability=0.02,
    packet_size_bytes=1000,
    duration_seconds=10
):
    rng = np.random.default_rng()

    if num_packets <= 0 or duration_seconds <= 0:
        raise ValueError("Packets and duration must be positive.")

    if base_latency_ms < 0 or jitter_std_ms < 0:
        raise ValueError("Delay parameters cannot be negative.")

    if not 0 <= loss_probability <= 1:
        raise ValueError("Loss probability must be between 0 and 1.")

    if packet_size_bytes <= 0:
        raise ValueError("Packet size must be positive.")

    # Simulate whether each packet arrives
    received_mask = rng.random(num_packets) >= loss_probability

    # Generate nonnegative one-way delays for received packets
    delays = np.maximum(
        0,
        rng.normal(
            base_latency_ms,
            jitter_std_ms,
            num_packets
        )
    )

    received_delays = delays[received_mask]

    packets_received = int(np.sum(received_mask))
    packets_lost = num_packets - packets_received

    loss_percent = packets_lost / num_packets * 100

    if packets_received > 0:
        average_latency = float(np.mean(received_delays))
    else:
        average_latency = 0.0

    # Simple jitter measure: mean absolute delay variation
    if packets_received > 1:
        jitter = float(np.mean(np.abs(np.diff(received_delays))))
    else:
        jitter = 0.0

    throughput_mbps = (
        packets_received * packet_size_bytes * 8
        / duration_seconds
        / 1_000_000
    )

    return {
        "packets_sent": num_packets,
        "packets_received": packets_received,
        "packets_lost": packets_lost,
        "packet_loss_percent": loss_percent,
        "average_latency_ms": average_latency,
        "jitter_ms": jitter,
        "throughput_mbps": throughput_mbps,
        "received_delays": received_delays.tolist()
    }


if __name__ == "__main__":
    results = simulate_network()

    for key, value in results.items():
        if key != "received_delays":
            print(f"{key}: {value}")
