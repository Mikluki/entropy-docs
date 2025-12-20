import re

import matplotlib.pyplot as plt
import numpy as np

PLOT_STYLE = "article_1x1.mplstyle"


def parse_and_plot(
    csv_name,
    figsize=(16, 12),
    markersize=0,
    xlabel=None,
    ylabel=None,
    xcoef=1.0,
    ycoef=1.0,
    lw=5,
):
    """
    Parse data file and create a plot with properly formatted axis labels.

    Args:
        csv_name (str): Path to the data file
    """
    # Read the file
    with open(csv_name, "r") as file:
        lines = file.readlines()

    # Extract metadata from the second commented line
    metadata_line = lines[1].strip()

    if not xlabel:
        ox_match = re.search(r"ox: ([^\[]+)\[([^\]]+)\]", metadata_line)
        if ox_match:
            # Handle name and symbol splitting by dash
            x_name_symbol = ox_match.group(1).strip()
            x_unit = ox_match.group(2).strip()

            if "-" in x_name_symbol:
                parts = x_name_symbol.split("-", 1)
                x_name = parts[0].strip()
                x_symbol = parts[1].strip()
                xlabel = f"{x_name}, {x_symbol} ({x_unit})"
            else:
                xlabel = f"{x_name_symbol} ({x_unit})"
        else:
            xlabel = "X-axis"

    if not ylabel:
        # Extract y-axis metadata
        oy_match = re.search(r"oy: ([^\[]+)\[([^\]]+)\]", metadata_line)
        if oy_match:
            # Handle name and symbol splitting by dash
            y_name_symbol = oy_match.group(1).strip()
            y_unit = oy_match.group(2).strip()

            if "-" in y_name_symbol:
                parts = y_name_symbol.split("-", 1)
                y_name = parts[0].strip()
                y_symbol = parts[1].strip()
                ylabel = f"{y_name}, {y_symbol} ({y_unit})"
            else:
                ylabel = f"{y_name_symbol} ({y_unit})"
        else:
            ylabel = "Y-axis"

    # Parse data
    x_data = []
    y_data = []

    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            values = line.split()
            if len(values) >= 2:
                try:
                    x = float(values[0].replace("E", "e"))  # Handle scientific notation
                    y = float(values[1].replace("E", "e"))
                    x_data.append(float(x))
                    y_data.append(float(y))
                except ValueError:
                    print(f"Warning: Could not parse line: {line}")

    x_data = np.array(x_data)
    y_data = np.array(y_data)

    # Create the plot
    plt.style.use(PLOT_STYLE)
    plt.figure(figsize=figsize)
    plt.plot(x_data * xcoef, y_data * ycoef, "o-", markersize=markersize, lw=lw)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # # Set title using the filename (without extension)
    # title = csv_name.split("/")[-1].split(".")[0].replace("_", " ").title()
    # plt.title(title)

    # Format x-axis for scientific notation if needed
    if max(x_data) < 1e-3 or max(x_data) > 1e3:
        plt.ticklabel_format(axis="x", style="sci", scilimits=(-3, 3))

    # Add grid for better readability
    plt.grid(True, linestyle="--", alpha=0.7)

    # Save the plot
    output_file = f"plot_{csv_name.split('.')[0]}.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Plot saved as: {output_file}")


if __name__ == "__main__":
    # parse_and_plot(
    #     "fig-1.csv",
    #     xlabel="Ток, I (uA)",
    #     xcoef=1e6,
    #     ylabel="Сопротивление, R (KОм)",
    #     ycoef=1e-3,
    # )
    #
    # parse_and_plot(
    #     "fig-2.csv",
    #     xlabel="Время, t (мс)",
    #     xcoef=1e6,
    #     # ylabel="Сопротивление, R (KОм)",
    #     # ycoef=1e-3,
    # )

    parse_and_plot("fig-3.csv", lw=2)

    parse_and_plot("fig-4.csv", lw=2)
