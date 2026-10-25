
import math
import unittest

from modules.integrated_simulation import (
    calculate_distance_km,
    calculate_slant_range,
    calculate_bpsk_ber,
    calculate_packet_error_probability,
    determine_active_link,
    run_integrated_simulation,
)


class TestAeroLinkIntegratedSimulation(unittest.TestCase):

    # TEST 1: Identical positions have zero ground distance
    def test_horizontal_distance(self):
        distance = calculate_distance_km(
            27.70, 85.35,
            27.70, 85.35
        )
        self.assertAlmostEqual(distance, 0.0, places=6)

    # TEST 2: Known 3-4-5 triangle
    def test_slant_range(self):
        distance = calculate_slant_range(
            horizontal_distance_km=4,
            aircraft_altitude_m=3000,
            ground_altitude_m=0
        )
        self.assertAlmostEqual(distance, 5.0, places=6)

    # TEST 3: Greater altitude increases slant range
    def test_altitude_increases_range(self):
        low = calculate_slant_range(10, 1000)
        high = calculate_slant_range(10, 5000)
        self.assertGreater(high, low)

    # TEST 4: Higher SNR reduces theoretical BER
    def test_ber_decreases_with_snr(self):
        ber_low = calculate_bpsk_ber(0)
        ber_high = calculate_bpsk_ber(10)
        self.assertLess(ber_high, ber_low)

    # TEST 5: Packet error probability increases with BER
    def test_packet_error_probability(self):
        low = calculate_packet_error_probability(
            0.0001, 256
        )
        high = calculate_packet_error_probability(
            0.01, 256
        )
        self.assertGreater(high, low)

    # TEST 6: Normal operation selects primary link
    def test_primary_link(self):
        link = determine_active_link(
            current_time=10,
            primary_failure_time=30,
            backup_activation_delay=5
        )
        self.assertEqual(link, "Primary")

    # TEST 7: During failover communication is unavailable
    def test_failover_downtime(self):
        link = determine_active_link(
            current_time=32,
            primary_failure_time=30,
            backup_activation_delay=5
        )
        self.assertEqual(link, "Unavailable")

    # TEST 8: Backup works after recovery
    def test_backup_activation(self):
        link = determine_active_link(
            current_time=35,
            primary_failure_time=30,
            backup_activation_delay=5
        )
        self.assertEqual(link, "Backup")

    # TEST 9: Integrated simulation returns all updates
    def test_integrated_record_count(self):
        results = run_integrated_simulation(
            time_step=5,
            number_updates=12
        )
        self.assertEqual(len(results), 13)

    # TEST 10: All packet counts must balance
    def test_packet_accounting(self):
        results = run_integrated_simulation()

        for row in results:
            self.assertEqual(
                row["packets_sent"],
                row["packets_received"] + row["packets_lost"]
            )

    # TEST 11: Primary failure causes an outage sample
    def test_integrated_outage(self):
        results = run_integrated_simulation(
            time_step=5,
            number_updates=12,
            primary_failure_time=30,
            backup_activation_delay=5
        )

        row_at_30 = next(
            row for row in results
            if row["time_seconds"] == 30
        )

        self.assertEqual(
            row_at_30["active_link"],
            "Unavailable"
        )
        self.assertEqual(
            row_at_30["packets_received"],
            0
        )

    # TEST 12: Slant range is at least horizontal distance
    def test_integrated_distance(self):
        results = run_integrated_simulation()

        for row in results:
            self.assertGreaterEqual(
                row["distance_km"],
                row["horizontal_distance_km"]
            )


if __name__ == "__main__":
    unittest.main()
