import numpy as np


def main():
    r_source = 50
    r_load = 0.1
    working_frequency = 10**6

    impedance_ratio = r_source / r_load
    Q = np.sqrt(impedance_ratio)

    omega_0 = 2 * np.pi * working_frequency

    L = Q * r_load / omega_0
    C1 = Q / r_source / omega_0
    C2 = Q / r_load / omega_0

    unit_conversion_dict = {"nF": 10**9, "muH": 10**6}
    c_units = "nF"
    l_units = "muH"
    print(f"Q factor = {Q:.2f}")
    print(f"C1 = {C1* unit_conversion_dict.get(c_units):.1f} [{c_units}]")
    print(f"L  = {L* unit_conversion_dict.get(l_units):.3f} [{l_units}]")
    print(f"C2 = {C2* unit_conversion_dict.get(c_units):.0f} [{c_units}]")


def main2():
    r_source = 50
    r_load = 0.1

    working_frequency = 10**6

    Q = np.sqrt(r_source / r_load - 1)

    omega_0 = 2 * np.pi * working_frequency

    L1 = Q * r_source / omega_0
    C1 = Q / r_source / omega_0
    r_virtual = r_source / (Q**2 + 1)
    L2 = Q * r_virtual / omega_0
    C2 = Q / r_virtual / omega_0
    L = L1 + L2

    unit_conversion_dict = {
        "nF": 10**9,
        "muF": 10**6,
        "nH": 10**9,
        "muH": 10**6,
    }
    c_units = "nF"
    l_units = "nH"
    print(f"Q factor = {Q:.2f}")
    print(f"C1 = {C1* unit_conversion_dict.get(c_units):.1f} [{c_units}]")
    print(f"L  = {L* unit_conversion_dict.get(l_units):.3f} [{l_units}]")
    print(f"C2 = {C2* unit_conversion_dict.get(c_units):.0f} [{c_units}]")


main2()
