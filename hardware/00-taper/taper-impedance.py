import matplotlib.pyplot as plt
import numpy as np


def klopfenstein_taper_profile(L, f_c, Z1, Z2, n_points=200, v=3e8):
    """
    Compute the Klopfenstein impedance profile Z(x) from x=0..L
    given:
        L      = total length of taper (meters)
        f_c    = highest design freq (Hz)
        Z1, Z2 = end impedances (Ohms) at x=0, x=L
        v      = phase velocity (m/s)
    Returns arrays x[], Zx[] of length n_points.
    """
    # Intrinsic reflection coefficient
    gamma_0 = (Z2 - Z1) / (Z2 + Z1)  # can be near 1 if Z1 << Z2

    # Phase constant at f_c
    beta_c = 2 * np.pi * f_c / v

    # Klopfenstein parameter B
    B = L * beta_c  # typically L * (2πf_c/v)

    # Reflection plateau
    gamma_m = gamma_0 / np.cosh(B)  # for small B, gamma_m ~ gamma_0

    # Discretize x from 0 to L
    x_arr = np.linspace(0, L, n_points)

    # Compute gamma(x)
    gamma_x = gamma_m * np.cosh(B * (L / 2 - x_arr)) / np.cosh(B * L / 2)

    # Compute Z(x)
    Zx = Z1 * np.sqrt((1 + gamma_x) / (1 - gamma_x))

    return x_arr, Zx


if __name__ == "__main__":
    # Parameters
    L = 0.03  # 3 cm
    f_c = 1e8  # 100 MHz
    Z1 = 0.1  # extremely low impedance
    Z2 = 50.0  # standard 50 ohms
    c = 3e8  # speed of light in vacuum (m/s)

    # Generate the taper profile
    x_vals, Z_vals = klopfenstein_taper_profile(L, f_c, Z1, Z2, n_points=200, v=c)

    # Plot the profile
    plt.figure(figsize=(6, 4))
    plt.plot(1000 * x_vals, Z_vals, "b-")
    plt.title("3 cm Klopfenstein Taper from 0.1 Ω to 50 Ω (f_c=100 MHz)")
    plt.xlabel("x (mm)")
    plt.ylabel("Z(x) (Ω)")
    plt.grid(True)
    plt.show()
