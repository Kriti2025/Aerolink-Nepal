
# ✈️ AeroLink Nepal

## Airport Communication & Surveillance Network Simulator

AeroLink Nepal is a Python-based educational engineering simulator developed to study digital communication, wireless propagation, network performance, aircraft surveillance, and communication system reliability.

The project uses Streamlit to provide an interactive interface for running experiments, visualizing engineering calculations, and investigating how communication-system parameters affect performance.

**Project Type:** Educational Simulation  
**Programming Language:** Python  
**User Interface:** Streamlit  
**Domain:** Electronics and Communication Engineering  
**Version:** 0.2 (Educational Prototype)

---

## 1. Project Overview

Airport communication and surveillance systems depend on reliable transmission of information between aircraft, ground stations, and monitoring facilities.

AeroLink Nepal demonstrates selected engineering concepts related to these systems through numerical simulations.

The project covers:

- Digital modulation and noise
- Bit Error Rate (BER)
- Forward Error Correction (FEC)
- Wireless free-space path loss
- Received signal power and SNR
- Packet latency, jitter, loss and throughput
- Synthetic aircraft position tracking
- Link redundancy and failover
- Integrated aircraft-to-ground communication analysis

This project does not use real aircraft surveillance data or operational aviation communication equipment.

---

## 2. Project Objectives

The main objectives are:

1. Simulate digital communication using BPSK and AWGN.
2. Investigate the relationship between Eb/N0 and BER.
3. Demonstrate basic error correction using repetition coding.
4. Analyze wireless link performance using free-space path loss and a simplified link budget.
5. Simulate packet transmission and network quality metrics.
6. Generate synthetic aircraft positions and movement.
7. Study communication failures and backup-link recovery.
8. Connect aircraft movement, radio propagation, estimated communication errors and packet delivery.
9. Visualize results using an interactive Streamlit dashboard.
10. Validate selected engineering relationships using automated Python tests.

---

## 3. Technologies Used

### Python
Used for numerical calculations, simulations and project logic.

### Streamlit
Provides the interactive web dashboard.

### NumPy
Supports numerical operations, random data generation and array processing.

### Pandas
Organizes simulation results into tables.

### Matplotlib
Generates engineering graphs and visualizations.

### unittest
Provides automated tests for selected engineering calculations and system behaviors.

### Git and GitHub
Used for version control and project management.

---

## 4. Engineering Modules

### Module 1: Digital Communication

This module demonstrates:

- Binary Phase Shift Keying (BPSK)
- Additive White Gaussian Noise (AWGN)
- Bit Error Rate (BER)
- Repetition-3 Forward Error Correction
- BER versus Eb/N0 analysis

The experiments show how channel noise influences the probability of incorrect bit detection.

### Module 2: Wireless Link Analyzer

This module calculates:

- Free-Space Path Loss (FSPL)
- Received signal power
- Receiver noise power
- Signal-to-Noise Ratio (SNR)
- Link margin

It also displays how these quantities change with distance.

The wireless analysis assumes an idealized propagation environment and uses illustrative system parameters.

### Module 3: Network Quality Monitor

This module simulates packet delivery and evaluates:

- Packet latency
- Jitter
- Packet loss
- Throughput
- Successful and unsuccessful packet transmission

It uses a synthetic network model rather than measurements from a live airport network.

### Module 4: Aircraft Surveillance Simulator

This module generates fictional aircraft information, including:

- Aircraft identifier
- Latitude and longitude
- Altitude
- Ground speed
- Track direction
- Position updates over time

It displays synthetic positions on a map and visualizes coordinate changes.

The model assumes constant speed, direction and altitude.

### Module 5: Reliability and Failover

This module investigates communication redundancy using primary and backup links.

It demonstrates:

- Primary-link selection
- Backup-link activation
- Communication unavailability
- Recovery time
- Service downtime
- Observed availability

The failover model uses a deterministic recovery delay.

### Module 6: Integrated System Simulation

This module connects several previously independent engineering calculations.

The integrated workflow includes:

1. Generating synthetic aircraft movement
2. Calculating horizontal distance
3. Estimating three-dimensional slant range
4. Calculating free-space path loss
5. Estimating received power and SNR
6. Estimating theoretical BPSK bit-error probability
7. Simulating packet delivery
8. Modeling primary-link failure and backup recovery
9. Displaying results through tables, maps and graphs

This module uses simplified mathematical relationships and assumptions to demonstrate system-level interactions.

---

## 5. Project Structure

```text
Aero/
|
|-- app.py
|
|-- modules/
|   |-- __init__.py
|   |-- aircraft_surveillance.py
|   |-- ber_snr_analysis_new.py
|   |-- fec_awgn_experiment.py
|   |-- wireless_link.py
|   |-- network_monitor.py
|   |-- reliability.py
|   |-- integrated_simulation.py
|   |-- integrated_visualization.py
|
|-- tests/
|   |-- test_integrated_simulation.py
|
|-- docs/
|   |-- learning_journal.md
|
|-- results/
|
|-- README.md
|-- .gitignore
```

Additional experimental and supporting files may exist in the repository.

---

## 6. Installation and Setup

### Prerequisites

- Python 3
- pip
- VS Code or another Python editor
- Git (optional)

### Clone the repository

```bash
git clone https://github.com/Kriti2025/Aerolink-Nepal.git
cd Aerolink-Nepal
```

Note: If the repository is private, access permissions are required.

### Create a virtual environment

On Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install streamlit numpy pandas matplotlib
```

### Run the Streamlit application

```powershell
python -m streamlit run app.py
```

Open the local URL displayed by Streamlit in the terminal.

The default is commonly:

```text
http://localhost:8501
```

The port may differ if another application is already using it.

---

## 7. Running Simulations

Select an engineering module from the dropdown menu in the Streamlit application.

Adjust the available parameters and run the relevant experiment.

The dashboard presents numerical measurements, visualizations or tables depending on the selected module.

### Integrated Simulation

Select **Integrated System Simulation**.

Configure the simulation duration, attenuation, failure time, backup activation delay and packet count.

Click **Run Complete Integrated Simulation**.

The results include:

- Aircraft position updates
- Slant range
- Free-space path loss
- Received power
- Estimated SNR
- Bit-error probability
- Packet delivery statistics
- Active communication link
- Failover behavior

---

## 8. Running Automated Tests

The project contains automated engineering validation tests.

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

The tests check selected mathematical and logical relationships, including:

- Zero horizontal distance between identical coordinates
- Known slant-range calculations
- Slant range increasing with altitude
- Theoretical BPSK BER decreasing as SNR increases
- Packet error probability increasing with BER
- Primary and backup link selection
- Communication interruption during failover
- Integrated record counts
- Packet accounting consistency

Passing these tests supports the correctness of the tested behaviors but does not establish compliance with operational aviation requirements.

---

## 9. Important Engineering Formulas

### Free-Space Path Loss

FSPL(dB) = 32.44 + 20log10(d) + 20log10(f)

Where:

- d = distance in kilometers
- f = frequency in MHz

### Received Power

Pr(dBm) = Pt(dBm) + Gt(dBi) + Gr(dBi) - FSPL(dB) - Other Losses(dB)

### Signal-to-Noise Ratio

SNR(dB) = Received Power(dBm) - Noise Power(dBm)

### Approximate Slant Range

Slant Range = sqrt(Horizontal Distance² + Height Difference²)

This approximation assumes local flat-Earth geometry.

### Bit Error Rate

BER = Number of Incorrect Bits / Total Bits

### Observed Availability

Availability(%) = Uptime / Observation Time × 100

---

## 10. Assumptions and Limitations

AeroLink Nepal is an educational prototype.

Key limitations include:

- Aircraft positions are synthetic.
- No real radar or ADS-B receiver is connected.
- Aircraft movement uses simplified kinematic assumptions.
- Slant-range calculations use an approximate geometric model.
- The wireless channel primarily uses free-space propagation.
- Antenna patterns, terrain, weather and multipath propagation are not modeled comprehensively.
- BPSK BER calculations use theoretical AWGN assumptions.
- The integrated model uses a simplified relationship between receiver SNR and Eb/N0.
- Packet errors are assumed independent in the simplified model.
- Additional attenuation and backup-link penalties are hypothetical parameters.
- Failover recovery uses a deterministic delay.
- Packet delivery is sampled at discrete update times.
- Network latency and jitter are not yet fully integrated with the radio-to-packet simulation.
- Results are not suitable for operational aviation decisions.

---

## 11. Future Improvements

Possible improvements include:

- More realistic aircraft trajectories
- Accurate ground-station elevation and antenna positions
- More detailed radio propagation models
- Weather, fading and interference simulation
- Antenna gains and directionality
- Better Eb/N0 and receiver bandwidth modeling
- Integrated packet latency and jitter analysis
- More realistic backup-link behavior
- Exporting results to CSV
- Additional automated tests
- Improved technical visualization and documentation

---

## 12. Conclusion

AeroLink Nepal combines communication engineering concepts into an interactive educational simulator.

Its main contribution is showing how aircraft movement, radio propagation, digital communication errors, packet delivery and failover behavior can be represented and studied together under documented assumptions.

The project is intended for learning, experimentation and engineering analysis rather than real-world airport operations.

---

## 13. Repository

GitHub:

https://github.com/Kriti2025/Aerolink-Nepal
