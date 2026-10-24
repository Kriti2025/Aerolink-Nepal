
import matplotlib.pyplot as plt


# ============================================================
# AEROLINK NEPAL - RELIABILITY AND FAILOVER SIMULATOR
# ============================================================


# ============================================================
# EXPERIMENT 1: PRIMARY LINK FAILURE AND BACKUP SELECTION
# ============================================================

def simulate_failover(
    primary_available=True,
    backup_available=True
):
    """
    Select the active communication link.

    The primary link is preferred when available.
    """

    if primary_available:
        active_link = "Primary Link"
        status = "Operational"

    elif backup_available:
        active_link = "Backup Link"
        status = "Failover Active"

    else:
        active_link = "No Active Link"
        status = "Communication Unavailable"

    return {
        "active_link": active_link,
        "status": status
    }


# ============================================================
# EXPERIMENT 2: FAILOVER RECOVERY TIME AND AVAILABILITY
# ============================================================

def simulate_recovery(
    total_time=60,
    failure_time=30,
    failover_delay=5
):
    """
    Simulate a primary link failure and a backup takeover.

    Assumptions:
    - Primary link works before failure_time.
    - Primary link fails at failure_time.
    - Backup link becomes active after failover_delay.
    - Backup link remains available afterward.
    """

    if total_time <= 0:
        raise ValueError(
            "Total observation time must be positive."
        )

    if not 0 <= failure_time <= total_time:
        raise ValueError(
            "Failure time must be within observation period."
        )

    if failover_delay < 0:
        raise ValueError(
            "Failover delay cannot be negative."
        )

    # Time when the backup link becomes operational
    recovery_time = failure_time + failover_delay

    # Calculate downtime within the observation period
    downtime = min(
        failover_delay,
        total_time - failure_time
    )

    uptime = total_time - downtime

    availability = (
        uptime / total_time
    ) * 100

    return {
        "total_time": total_time,
        "failure_time": failure_time,
        "recovery_time": recovery_time,
        "failover_delay": failover_delay,
        "downtime": downtime,
        "uptime": uptime,
        "availability": availability
    }


# ============================================================
# EXPERIMENT 3: SERVICE AVAILABILITY GRAPH
# ============================================================

def plot_failover_timeline(result):
    """
    Visualize service status over the observation period.

    Service status:
    1 = Available
    0 = Unavailable
    """

    total_time = result["total_time"]
    failure_time = result["failure_time"]
    recovery_time = result["recovery_time"]

    # Key transition times
    times = [0, failure_time]

    if recovery_time < total_time:
        times.append(recovery_time)

    times.append(total_time)

    # Construct exact step intervals
    fig, ax = plt.subplots(figsize=(10, 4))

    if failure_time > 0:
        ax.hlines(
            1,
            0,
            failure_time,
            linewidth=3,
            label="Primary Link Active"
        )

    outage_end = min(recovery_time, total_time)

    if outage_end > failure_time:
        ax.hlines(
            0,
            failure_time,
            outage_end,
            linewidth=3,
            label="Communication Interrupted"
        )

    if recovery_time < total_time:
        ax.hlines(
            1,
            recovery_time,
            total_time,
            linewidth=3,
            label="Backup Link Active"
        )

    ax.axvline(
        failure_time,
        linestyle="--",
        label="Primary Failure"
    )

    if recovery_time <= total_time:
        ax.axvline(
            recovery_time,
            linestyle=":",
            label="Backup Recovery"
        )

    ax.set_title("Communication Availability During Failover")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Service Status")
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["Unavailable", "Available"])
    ax.set_xlim(0, total_time)
    ax.set_ylim(-0.3, 1.3)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="best")

    fig.tight_layout()

    return fig


# ============================================================
# MAIN PROGRAM: RUN ALL EXPERIMENTS
# ============================================================

if __name__ == "__main__":

    print("=" * 55)
    print("AEROLINK NEPAL")
    print("RELIABILITY AND FAILOVER SIMULATOR")
    print("=" * 55)

    # --------------------------------------------------------
    # EXPERIMENT 1: FAILOVER DECISION
    # --------------------------------------------------------

    print("\nEXPERIMENT 1: LINK FAILURE AND SELECTION")

    scenarios = [
        ("Normal Operation", True, True),
        ("Primary Failure", False, True),
        ("Both Links Failed", False, False)
    ]

    for name, primary, backup in scenarios:

        result = simulate_failover(
            primary_available=primary,
            backup_available=backup
        )

        print()
        print("Scenario:", name)
        print("Active Link:", result["active_link"])
        print("Status:", result["status"])

    # --------------------------------------------------------
    # EXPERIMENT 2: RECOVERY TIME
    # --------------------------------------------------------

    print("\nEXPERIMENT 2: FAILOVER RECOVERY ANALYSIS")

    recovery_result = simulate_recovery(
        total_time=60,
        failure_time=30,
        failover_delay=5
    )

    print(
        "Primary failure:",
        recovery_result["failure_time"],
        "seconds"
    )

    print(
        "Backup recovery:",
        recovery_result["recovery_time"],
        "seconds"
    )

    print(
        "Communication downtime:",
        recovery_result["downtime"],
        "seconds"
    )

    print(
        "Communication uptime:",
        recovery_result["uptime"],
        "seconds"
    )

    print(
        "Observed availability:",
        f"{recovery_result['availability']:.2f}%"
    )

    # --------------------------------------------------------
    # EXPERIMENT 3: VISUALIZATION
    # --------------------------------------------------------

    print("\nEXPERIMENT 3: FAILOVER TIMELINE")

    fig = plot_failover_timeline(recovery_result)
    plt.show()
    plt.close(fig)
