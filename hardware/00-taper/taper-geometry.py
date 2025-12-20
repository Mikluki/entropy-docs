import matplotlib.pyplot as plt
import numpy as np


##############################################################################
# 1) Klopfenstein Taper Function
##############################################################################
def klopfenstein_taper_profile(L, f_c, Z1, Z2, n_points=200, v=3e8):
    """
    Compute the Klopfenstein impedance profile Z(x) from x=0..L.

    Parameters:
    -----------
    L      : float
        Total length of taper (meters).
    f_c    : float
        'Cutoff' or highest design frequency (Hz).
    Z1     : float
        Impedance at x=0 (Ohms).
    Z2     : float
        Impedance at x=L (Ohms).
    n_points : int
        Number of discrete points along the taper to compute.
    v      : float
        Phase velocity in the line (m/s).

    Returns:
    --------
    x_arr : ndarray
        Array of length n_points, position along the taper [m].
    Zx    : ndarray
        Array of length n_points, characteristic impedance at each x.
    """
    gamma_0 = (Z2 - Z1) / (Z2 + Z1)  # Intrinsic reflection
    beta_c = 2 * np.pi * f_c / v  # Phase constant at f_c
    B = L * beta_c  # Klopfenstein parameter
    # Reflection "floor"
    gamma_m = gamma_0 / np.cosh(B)  # For small B, ~ gamma_0

    x_arr = np.linspace(0, L, n_points)
    # Reflection shape
    numer = np.cosh(B * ((L / 2) - x_arr))
    denom = np.cosh(B * (L / 2))
    gamma_x = gamma_m * (numer / denom)

    # Impedance at x
    Zx = Z1 * np.sqrt((1 + gamma_x) / (1 - gamma_x))
    return x_arr, Zx


##############################################################################
# 2) Microstrip Approx Functions
##############################################################################
def microstrip_eps_eff(u, eps_r):
    """
    Approximate effective dielectric constant for microstrip.
    u = w/h, eps_r = substrate dielectric constant
    """
    return 0.5 * (eps_r + 1) + 0.5 * (eps_r - 1) * (1 + 12.0 / u) ** -0.5


def microstrip_Z0(u, eps_r):
    """
    Returns approximate Z0 (Ohms) for microstrip (width/height = u),
    using piecewise formula.
    """
    eeff = microstrip_eps_eff(u, eps_r)
    if u <= 1.0:
        # Narrow line
        return (60.0 / np.sqrt(eeff)) * np.log(8.0 / u + 0.25 * u)
    else:
        # Wider line
        return (120.0 * np.pi / np.sqrt(eeff)) / (u + 1.393 + 0.667 * np.log(u + 1.444))


def invert_microstrip_Z0(Z_target, eps_r, tol=1e-5):
    """
    Numerically invert microstrip_Z0(...) to find u = w/h
    for the given target Z0, using binary search.
    """
    u_min = 1e-6
    u_max = 1e4
    for _ in range(100):
        u_mid = 0.5 * (u_min + u_max)
        Z_mid = microstrip_Z0(u_mid, eps_r)
        if Z_mid > Z_target:
            # Increase w/h => typically decreases Z0, so we go opposite
            u_min = u_mid
        else:
            u_max = u_mid
        if abs(Z_mid - Z_target) < tol:
            break
    return u_mid  # pyright: ignore


##############################################################################
# 3) MAIN: Compute Taper, then Convert to w(x)
##############################################################################
if __name__ == "__main__":
    # ============= USER PARAMETERS ==========================
    L = 0.03  # Taper length, meters (3 cm)
    f_c = 1e8  # Highest frequency = 100 MHz
    Z1 = 0.1  # Starting impedance (Ohms)
    Z2 = 50.0  # Ending impedance (Ohms)
    c = 3e8  # Propagation speed (m/s), if in air or similar
    n_points = 200  # How many discrete points along taper

    # Microstrip geometry parameters
    h = 1.0e-3  # Substrate thickness = 1 mm, for example
    eps_r = 4.4  # Dielectric constant, e.g. typical FR-4 ~4.3-4.7

    # 1) Get the Klopfenstein impedance profile
    x_vals, Z_vals = klopfenstein_taper_profile(L, f_c, Z1, Z2, n_points=n_points, v=c)

    # 2) For each Z(x), invert microstrip formula to get w/h => w
    w_vals = []
    for Z0 in Z_vals:
        # If the target Z0 is extremely low (< ~1 ohm),
        # the standard formula might not be very accurate,
        # but let's do it anyway for demonstration:
        u = invert_microstrip_Z0(Z0, eps_r, tol=1e-6)  # w/h
        w_vals.append(u * h)

    w_vals = np.array(w_vals)

    # 3) Output or plot: (x_vals, w_vals)
    #    We'll do a quick plot in Matplotlib, with x in mm, w in mm
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x_vals * 1000, w_vals * 1000, "b-o", label="Width profile")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("width w(x) (mm)")
    ax.set_title("Klopfenstein Taper Geometry\nfrom Z=%.3f Ω to Z=%.1f Ω" % (Z1, Z2))
    # ax.set_aspect("equal", adjustable="box")
    ax.grid(True)
    ax.legend()
    plt.show()

    # 4) If needed, write out x,y to a CSV for CAD
    # with open("taper_xy.csv","w") as f:
    #     f.write("x_mm,w_mm\n")
    #     for xx,ww in zip(x_vals, w_vals):
    #         f.write(f"{xx*1000:.6e},{ww*1000:.6e}\n")

    print("Done. If needed, see 'taper_xy.csv' for the x,y data.")
