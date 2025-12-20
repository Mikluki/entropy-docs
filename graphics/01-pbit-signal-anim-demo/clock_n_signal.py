import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.animation import FuncAnimation


def generate_pbit_data(
    duration=30,  # seconds
    sampling_rate=1000,  # samples per second
    clock_freq=2,  # Hz
    voltage_change_interval=3,  # seconds - change voltage every 4 seconds
):
    """Generate clock signal and pbit response data with randomly changing voltages"""
    # Time vector
    t = np.linspace(0, duration, int(duration * sampling_rate))

    # Create dataframe
    df = pd.DataFrame({"time": t})

    # Generate clock signal (square wave)
    df["clock_signal"] = np.where(np.sin(2 * np.pi * clock_freq * t) > 0, 1, 0)

    # Generate voltage signal (changes every voltage_change_interval seconds)
    voltage = np.zeros_like(t)
    df["voltage"] = voltage  # Initialize voltage column

    # Assign random voltages for each interval
    voltage_intervals = int(duration / voltage_change_interval)
    for i in range(voltage_intervals):
        start_idx = int(i * voltage_change_interval * sampling_rate)
        end_idx = int((i + 1) * voltage_change_interval * sampling_rate)
        if end_idx > len(t):
            end_idx = len(t)

        # Random voltage between -2.5 and 2.5
        random_voltage = random.uniform(-2.5, 2.5)
        df.loc[start_idx : end_idx - 1, "voltage"] = random_voltage

    # Find the clock high periods
    clock_high_starts = []
    clock_high_ends = []

    current_state = 0
    for i, val in enumerate(df["clock_signal"]):
        if val == 1 and current_state == 0:  # Rising edge
            clock_high_starts.append(i)
            current_state = 1
        elif val == 0 and current_state == 1:  # Falling edge
            clock_high_ends.append(i)
            current_state = 0

    # Make sure we have the same number of starts and ends
    if len(clock_high_starts) > len(clock_high_ends):
        clock_high_ends.append(len(t))  # Add end of array if last period is cut off

    print(f"Found {len(clock_high_starts)} clock high periods")

    # Generate pbit response
    pbit_response = np.zeros_like(t)

    responses_generated = 0
    for start_idx, end_idx in zip(clock_high_starts, clock_high_ends):
        # Get the voltage at this clock period
        period_voltage = df.loc[start_idx, "voltage"]

        # Calculate probability using tanh
        p_one = 0.5 * (1 + np.tanh(period_voltage))

        # Decide if there will be a response in this clock period
        if np.random.random() < p_one:
            responses_generated += 1

            # Place the peak at the middle of the clock high period
            peak_pos = start_idx + (end_idx - start_idx) // 2

            # Create a peak (Gaussian shape)
            width = 20  # Width of the peak
            idx_range = np.arange(
                max(0, peak_pos - width), min(len(t), peak_pos + width)
            )
            peak_height = 1.0  # Full height
            sigma = width / 3  # Make peak width reasonable
            peak = peak_height * np.exp(-0.5 * ((idx_range - peak_pos) / sigma) ** 2)

            # Assign peak to response
            pbit_response[idx_range] = peak

    print(
        f"Generated {responses_generated} responses out of {len(clock_high_starts)} clock periods"
    )

    # Add to dataframe
    df["pbit_response"] = pbit_response

    # Calculate probability column (for reference)
    df["probability"] = 0.5 * (1 + np.tanh(df["voltage"]))

    # Save to CSV
    filename = "pbit_data.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

    return filename


def animate_pbit_data(csv_file):
    """Create animation showing clock signal, pbit response, and probability distribution"""
    # Read data
    df = pd.read_csv(csv_file)

    # Create figure with 3 subplots
    fig = plt.figure(figsize=(12, 10))
    gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 1.5])

    # Create subplots
    ax1 = fig.add_subplot(gs[0])  # Clock signal
    ax2 = fig.add_subplot(gs[1])  # PBit response
    ax3 = fig.add_subplot(gs[2])  # Probability vs Voltage

    # Set up time-based subplots
    ax1.set_ylabel("Clock Signal")
    ax1.set_ylim(-0.1, 1.1)
    ax1.set_xticklabels([])  # Hide x labels on top plot

    ax2.set_ylabel("PBit Response")
    ax2.set_ylim(-0.1, 1.1)
    ax2.set_xlabel("Time (s)")

    # Set up voltage-probability subplot
    ax3.set_xlabel("Bias Voltage (V)")
    ax3.set_ylabel("Probability P(1)")
    ax3.set_xlim(-3, 3)
    ax3.set_ylim(0, 1)
    ax3.grid(True, linestyle="--", alpha=0.7)

    # Time window to display (in seconds)
    time_window = 4.0

    # Create tanh curve for the voltage-probability plot
    voltage_range = np.linspace(-3, 3, 1000)
    tanh_curve = 0.5 * (1 + np.tanh(voltage_range))
    ax3.plot(voltage_range, tanh_curve, "b-", lw=2, label="P(1) = 0.5(1+tanh(V))")

    # Add vertical line for current voltage (will be updated)
    voltage_line = ax3.axvline(
        x=0, color="r", linestyle="-", lw=2, label="Current Voltage"
    )

    # Add horizontal line for current probability (will be updated)
    prob_line = ax3.axhline(
        y=0.5, color="g", linestyle="--", lw=2, label="Current P(1)"
    )

    # Add a marker at the intersection
    (current_point,) = ax3.plot([0], [0.5], "ro", markersize=8)

    # Current probability text display
    prob_text = ax3.text(
        0.05,
        0.1,
        "P(1) = 0.5",
        transform=ax3.transAxes,
        bbox=dict(facecolor="white", alpha=0.8),
    )

    # Set up lines for time-based plots
    (clock_line,) = ax1.plot([], [], "b-", lw=2)
    (pbit_line,) = ax2.plot([], [], "r-", lw=2)

    # Add legends
    ax3.legend(loc="upper left")

    # Initialization function
    def init():
        clock_line.set_data([], [])
        pbit_line.set_data([], [])
        voltage_line.set_xdata([0, 0])
        prob_line.set_ydata([0.5, 0.5])
        current_point.set_data([0], [0.5])
        prob_text.set_text("P(1) = 0.5")
        return [
            clock_line,
            pbit_line,
            voltage_line,
            prob_line,
            current_point,
            prob_text,
        ]

    # Update function for animation
    def update(frame):
        # Calculate current time based on frame
        current_time = frame / 20  # Assuming 20 fps

        # Set visible window
        start_time = max(0, current_time - time_window / 2)
        end_time = start_time + time_window

        # Update x-limits for time plots
        ax1.set_xlim(start_time, end_time)
        ax2.set_xlim(start_time, end_time)

        # Get data for the visible window
        visible_df = df[(df["time"] >= start_time) & (df["time"] <= end_time)]

        if not visible_df.empty:
            # Get current voltage (from middle of visible window)
            middle_idx = len(visible_df) // 2
            if middle_idx < len(visible_df):
                current_voltage = visible_df.iloc[middle_idx]["voltage"]
                current_prob = 0.5 * (1 + np.tanh(current_voltage))

                # Update title with current voltage and probability
                fig.suptitle(
                    f"PBit Response",
                    fontsize=16,
                )

                # Update voltage line position
                voltage_line.set_xdata([current_voltage, current_voltage])

                # Update probability line position
                prob_line.set_ydata([current_prob, current_prob])

                # Update intersection point
                current_point.set_data([current_voltage], [current_prob])

                # Update probability text
                prob_text.set_text(f"P(1) = {current_prob:.4f}")

            # Update time plots with visible data
            t_data = visible_df["time"]
            clock_data = visible_df["clock_signal"]
            pbit_data = visible_df["pbit_response"]

            clock_line.set_data(t_data, clock_data)
            pbit_line.set_data(t_data, pbit_data)

        return [
            clock_line,
            pbit_line,
            voltage_line,
            prob_line,
            current_point,
            prob_text,
        ]

    # Create animation
    # More frames for smoother animation
    total_duration = df["time"].max()
    frames = int(total_duration * 20)  # 20 fps

    ani = FuncAnimation(
        fig, update, frames=frames, init_func=init, blit=True, interval=50
    )

    # Save and display
    ani.save("pbit_animation.gif", writer="pillow", fps=20)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)  # Make room for the title
    plt.show()

    print("Animation saved as pbit_animation.gif")


# Main execution
if __name__ == "__main__":
    # Generate data and save to CSV
    csv_file = "pbit_data.csv"
    # csv_file = None

    if csv_file is None:
        csv_file = generate_pbit_data(
            duration=30,  # seconds
            sampling_rate=1000,  # samples per second
            clock_freq=2,  # Hz
            voltage_change_interval=3,  # seconds - change voltage every 4 seconds
        )

    # Create animation from CSV
    animate_pbit_data(csv_file)
