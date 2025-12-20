"""
CST Data Analysis and Visualization Tool

This module provides tools for analyzing and visualizing CST simulation data,
including impedance calculations and absorption coefficients.
"""

import re
import weakref
from dataclasses import dataclass
from itertools import cycle
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# Constants
FONT_SIZE = 20
DEFAULT_LINEWIDTH = 4
DEFAULT_FIGURE_SIZE = (12, 10)


def calculate_absorption_coefficient(
    real_z: np.ndarray, imaginary_z: np.ndarray, z_target_ohm: float
) -> np.ndarray:
    """
    Calculate the absorption coefficient from complex impedance values.

    Args:
        real_z: Array of real impedance values
        imaginary_z: Array of imaginary impedance values
        z_target_kohm: Target impedance in kilo-ohms

    Returns:
        Array of absorption coefficient values
    """
    z = real_z + 1j * imaginary_z
    z_target = z_target_ohm
    return 1 - np.abs((z - z_target) / (z + z_target))


def calculate_s11_coefficient(absorption_coef: np.ndarray) -> np.ndarray:
    """
    Calculate the S11 coefficient from absorption coefficient.

    Args:
        absorption_coef: Array of absorption coefficient values

    Returns:
        Array of S11 coefficient values in dB
    """
    return 20 * np.log10(1 - absorption_coef)


def lighten_color(color: np.ndarray, factor: float = 0.3) -> np.ndarray:
    """
    Create a lighter version of a color.

    Args:
        color: Original color (rgba array)
        factor: Lightening factor (0 to 1, higher means lighter)

    Returns:
        Lightened color array
    """
    lighter = color.copy()
    lighter[:3] = 1 - factor * (1 - lighter[:3])
    return lighter


class ColorManager:
    """Manages color cycling for multiple plots."""

    def __init__(
        self, n_initial_colors: int = 10, colormap: cm = cm.rainbow  # pyright: ignore
    ):
        self.colormap = colormap
        self.n_colors = n_initial_colors
        self._generate_colors()

    def _generate_colors(self):
        """Generate color array from colormap."""
        self.colors = self.colormap(np.linspace(0, 1, self.n_colors))  # pyright: ignore
        self.color_cycle = cycle(self.colors)

    def get_next_color(self):
        """Get next color in cycle."""
        return next(self.color_cycle)

    def regenerate_colors(self, n_colors: int):
        """Regenerate color pool with new size."""
        self.n_colors = n_colors
        self._generate_colors()


@dataclass
class CSTFiles:
    """Container for CST data file paths."""

    z_file: Path
    s_db_file: Optional[Path] = None
    s_linear_file: Optional[Path] = None


def parse_frequency_unit(header: str) -> str:
    """
    Extract frequency unit from CST file header.

    Args:
        header: Header line from CST file

    Returns:
        Frequency unit (e.g., 'MHz', 'GHz')
    """
    match = re.search(r'Frequency\s*/\s*(\w+)"', header)
    if not match:
        raise ValueError(f"Could not parse frequency unit from header: {header}")
    return match.group(1)


def frequency_conversion_factor(from_unit: str, to_unit: str = "MHz") -> float:
    """
    Calculate conversion factor between frequency units.

    Args:
        from_unit: Source frequency unit
        to_unit: Target frequency unit (default: MHz)

    Returns:
        Conversion factor
    """
    units = {"Hz": 1, "kHz": 1e3, "MHz": 1e6, "GHz": 1e9, "THz": 1e12}

    if from_unit not in units or to_unit not in units:
        raise ValueError(f"Unsupported frequency units: {from_unit} -> {to_unit}")

    return units[from_unit] / units[to_unit]


def create_plot(
    xlabel: str,
    ylabel: str,
    title: Optional[str] = None,
) -> tuple[Figure, Axes]:
    """
    Create a new figure and axes with standard styling.

    Args:
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Optional plot title

    Returns:
        Tuple of (figure, axes)
    """
    plt.style.use("article_1x1.mplstyle")
    plt.rcParams.update(
        {
            "font.size": FONT_SIZE,
            "lines.markersize": 0,
            "lines.linewidth": DEFAULT_LINEWIDTH,
            "axes.grid": True,
            "lines.marker": ".",
            "axes.autolimit_mode": "round_numbers",
            "figure.max_open_warning": 0,
        }
    )

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=DEFAULT_FIGURE_SIZE)
    ax.set_xlabel(xlabel, fontsize=FONT_SIZE * 1.2)
    ax.set_ylabel(ylabel, fontsize=FONT_SIZE * 1.2)
    if title:
        ax.set_title(title, fontsize=FONT_SIZE * 1.2)
    return fig, ax


class PlotExporter:
    """Handles exporting plots to files."""

    def __init__(self, export_dir: str = "plots"):
        self.export_dir = Path(export_dir)

    def save_plot(self, fig: Figure, fig_name: str = "plot.png"):
        """Save plot to file."""
        self.export_dir.mkdir(parents=True, exist_ok=True)
        png_path = self.export_dir / fig_name
        fig.savefig(png_path, bbox_inches="tight")
        print(f"Saved plot to {png_path}")


class CSTData:
    """Stores and processes CST simulation data."""

    color_manager = ColorManager()
    _instances = set()

    def __init__(
        self,
        cst_files: CSTFiles,
        network_name: str,
        z_source: float,
        z_load: float,
        target_freq_unit: str = "MHz",
    ):
        """
        Initialize CST data object.

        Args:
            cst_files: CSTFiles object containing paths to data files
            network_name: Name of the network (e.g., "Pi")
            z_source: Source impedance in Ohms
            z_load: Load impedance in Ohms
            target_freq_unit: Target frequency unit (default: MHz)
        """
        self.network_name = network_name
        self.z_source = z_source
        self.z_load = z_load
        self.target_freq_unit = target_freq_unit
        self.color = self.color_manager.get_next_color()
        self.label = f"{network_name} {z_source} -> {z_load}"

        print(f"Loading CST data for {network_name}...")
        data = self._load_cst_data(cst_files)

        self.frequency_range = data["frequency_range"]
        self.real_z = data["real_z"]
        self.imaginary_z = data["imaginary_z"]
        self.s_db = data.get("s_db")
        self.s_linear = data.get("s_linear")
        self.absorption_coef = data["absorption_coef"]
        self.s11_calc = data["s11_calc"]

        CSTData._instances.add(weakref.ref(self, CSTData._cleanup))

    @classmethod
    def _cleanup(cls, weak_ref):
        """Remove dead weak references."""
        cls._instances.discard(weak_ref)

    def plot_all(
        self, exporter: PlotExporter, titles: Optional[Dict[str, Optional[str]]] = None
    ):
        """
        Generate and save all available plots for the dataset.

        Args:
            exporter: PlotExporter instance for saving plots
            titles: Optional dictionary of plot titles with keys:
                   'impedance', 'absorption', 's_db', 's_linear'
                   Use None for a specific key to have no title
                   Use None for titles to have no titles at all
        """
        # Handle titles
        default_titles = {
            "impedance": f"{self.network_name} Impedance",
            "absorption": f"{self.network_name} Absorption",
            "s_db": f"{self.network_name} S-Parameters (dB)",
            "s_linear": f"{self.network_name} S-Parameters (linear)",
        }

        # If titles is None, use default_titles
        # If titles is {}, use no titles
        # If titles has some keys, override defaults for those keys
        if titles is None:
            plot_titles = default_titles
        else:
            plot_titles = {key: None for key in default_titles}  # Start with no titles
            if titles:  # If titles is not empty, use provided values
                plot_titles.update(titles)  # pyright: ignore

        # Plot impedance
        fig_z, ax_z = create_plot(
            xlabel=f"Frequency ({self.target_freq_unit})",
            ylabel="Impedance (Ω)",
            title=plot_titles.get("impedance"),
        )
        ax_z.plot(self.frequency_range, self.real_z, label="Real Z", color=self.color)
        ax_z.plot(
            self.frequency_range,
            self.imaginary_z,
            label="Imaginary Z",
            color=self.color,
            linestyle="--",
        )
        ax_z.legend()
        exporter.save_plot(fig_z, f"{self.network_name}-z")

        # Plot absorption coefficient
        fig_abs, ax_abs = create_plot(
            xlabel=f"Frequency ({self.target_freq_unit})",
            ylabel="Absorption Coefficient",
            title=plot_titles.get("absorption"),
        )
        ax_abs.plot(self.frequency_range, self.absorption_coef, color=self.color)
        exporter.save_plot(fig_abs, f"{self.network_name}-abs")

        # Plot S-parameters in dB
        if self.s_db is not None:
            fig_s_db, ax_s_db = create_plot(
                xlabel=f"Frequency ({self.target_freq_unit})",
                ylabel="S-Parameters (dB)",
                title=plot_titles.get("s_db"),
            )
            # Plot measured S11 with original color
            ax_s_db.plot(
                self.frequency_range,
                self.s_db,
                label="S11 (measured)",
                color=self.color,
            )
            # Plot calculated S11 with lighter color
            ax_s_db.plot(
                self.frequency_range,
                self.s11_calc,
                label="S11 (calculated)",
                color=lighten_color(self.color),
                linestyle=":",  # Using dotted line for better distinction
            )
            ax_s_db.legend()
            exporter.save_plot(fig_s_db, f"{self.network_name}-s-db")

        # Plot S-parameters linear
        if self.s_linear is not None:
            fig_s_lin, ax_s_lin = create_plot(
                xlabel=f"Frequency ({self.target_freq_unit})",
                ylabel="S-Parameters (linear)",
                title=plot_titles.get("s_linear"),
            )
            ax_s_lin.plot(self.frequency_range, self.s_linear, color=self.color)
            exporter.save_plot(fig_s_lin, f"{self.network_name}-s-linear")

    def _load_file_data(
        self, filepath: Path, columns: tuple[int, ...]
    ) -> Tuple[List[np.ndarray], str]:
        """
        Load numerical data from CST text file.

        Args:
            filepath: Path to the CST data file
            columns: Tuple of column indices to read

        Returns:
            Tuple of (list of numpy arrays containing data, frequency unit)
        """
        with open(filepath) as f:
            lines = f.readlines()
            if len(lines) < 2:
                raise ValueError(f"File {filepath} has insufficient lines")

            header = lines[1]
            print(f"Processing file {filepath.name}")
            print(f"Header: {header.strip()}")

            freq_unit = parse_frequency_unit(header)
            data_lines = lines[3:]

            return (
                [
                    np.array([float(line.strip().split()[col]) for line in data_lines])
                    for col in columns
                ],
                freq_unit,
            )

    def _load_cst_data(self, cst_files: CSTFiles) -> dict:
        """
        Load all CST format data files.

        Args:
            cst_files: CSTFiles object containing paths to data files

        Returns:
            Dictionary containing loaded and calculated data
        """
        # Load impedance data (required)
        (freq, re_z, im_z), freq_unit = self._load_file_data(
            cst_files.z_file, (0, 1, 2)
        )

        # Convert frequency to target unit
        freq_conv = frequency_conversion_factor(freq_unit, self.target_freq_unit)
        freq = freq * freq_conv

        data = {
            "frequency_range": freq,
            "real_z": re_z,
            "imaginary_z": im_z,
        }

        # Load S-parameter data (optional)
        if cst_files.s_db_file:
            (_, s_db), _ = self._load_file_data(cst_files.s_db_file, (0, 1))
            data["s_db"] = s_db

        if cst_files.s_linear_file:
            (_, s_linear), _ = self._load_file_data(cst_files.s_linear_file, (0, 1))
            data["s_linear"] = s_linear

        # Calculate derived quantities
        data["absorption_coef"] = calculate_absorption_coefficient(
            re_z, im_z, self.z_source
        )
        data["s11_calc"] = calculate_s11_coefficient(data["absorption_coef"])

        return data


def main():
    """Main execution function."""
    # Define file paths
    data_dir = Path("data-Pi-match")
    network_name = "Pi-match"

    cst_files = CSTFiles(
        z_file=data_dir / f"{network_name}-Z.txt",
        s_db_file=data_dir / f"{network_name}-S-db.txt",
        s_linear_file=data_dir / f"{network_name}-S-linear.txt",
    )

    # Create CST data object
    cst_data = CSTData(
        cst_files=cst_files,
        network_name=network_name,
        z_source=50,
        z_load=0.1,
        target_freq_unit="MHz",
    )

    # Generate all plots
    exporter = PlotExporter("plots-mnws")
    cst_data.plot_all(exporter, titles={})


if __name__ == "__main__":
    main()
