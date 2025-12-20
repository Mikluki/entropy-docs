from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray


def logist(
    J: NDArray[np.floating] | float, J0: float = 1, a: float = 1
) -> NDArray[np.floating] | float:
    """
    Logistic function

    Parameters
    ----------
    J : array-like or float
        Input current value(s)
    J0 : float, optional
        Threshold current or decision boundary parameter for the sigmoid function
    a : float, optional
        Scale factor. Default is 1.

    Returns
    -------
    float or array-like
        Logistic function output
    """
    return 1 / (1 + np.exp(-a * (J - J0)))


def s_wire(
    J: NDArray[np.floating], N_cycl: int = 1, J0: float = 1, a: float = 1
) -> NDArray[np.floating]:
    """
    S-wire simulation

    Parameters
    ----------
    J : array-like
        Input current values
    N_cycl : int, optional
        Number of cycles in simulation mode. Default is 1.
    J0 : float, optional
        Threshold current or decision boundary parameter for the sigmoid function
    a : float, optional
        Scale factor. Default is 1.

    Returns
    -------
    array-like
        Simulation results
    """
    s = np.zeros_like(J)
    for Ji, Jt in enumerate(J.flat):
        p = (np.tanh(a * (Jt - J0) / 2) + 1) / 2
        s.flat[Ji] = (
            np.sum(np.random.choice([0, 1], size=N_cycl, replace=True, p=[1 - p, p]))
            / N_cycl
        )
    return s


def sigmoid(
    J: NDArray[np.floating] | float,
    sim: bool = False,
    N_cycl: int = 1,
    J0: float = 1,
    a: float = 1,
) -> NDArray[np.floating] | float:
    """
    Returns sigmoid value depending on current J in two modes:
        ideal mode through logistic function calculation (sim=False) and
        s-wire simulation mode, where the value equals the fraction of ones over N_cycl (sim=True)

    Parameters
    ----------
    J : float or array-like
        Current supplied to s-wire
    sim : bool, optional
        Mode selection. Default is False.
    N_cycl : int, optional
        Number of cycles in simulation mode. Default is 1.
    J0 : float, optional
        Threshold current or decision boundary parameter for the sigmoid function
    a : float, optional
        Scale factor. Default is 1.

    Returns
    -------
    float or array-like
        Sigmoid value
    """
    if sim:
        s = s_wire(J, N_cycl=N_cycl, J0=J0, a=a)  # pyright: ignore
    else:
        s = logist(J, J0=J0, a=a)
    return s


def gen_data(
    n_samples: int = 250, xm: float = 1, phi: float = np.pi / 6, xcross: float = 0.5
) -> Tuple[NDArray[np.floating], NDArray[np.integer]]:
    """
    Function creates a set of two-dimensional data and assigns them one of two classes

    Parameters
    ----------
    N_samples : int, optional
        Number of points. Default is 250.
    xm : float, optional
        Amplitude. Default is 1.
    phi : float, optional
        Angle of inclination of the line separating classes. Default is np.pi/6.
    xcross : float, optional
        Depth of class mixing near the separating line. Default is 0.5.

    Returns
    -------
    x : np.array of shape (N,2)
        Point locations
    y : np.array of int (0 and 1)
        Class labels
    """
    x = (2 * np.random.rand(n_samples, 2) - 1) * xm
    y = np.array(
        [1 if (xj * np.cos(phi) + xi * np.sin(phi)) > 0 else 0 for xi, xj in x]
    ).astype(int)
    dx = (2 * np.random.rand(n_samples) - 1) * xm * xcross
    x[:, 0] = (x[:, 0] + dx * np.cos(phi)) / (1 + xcross * np.abs(np.cos(phi)))
    x[:, 1] = (x[:, 1] + dx * np.sin(phi)) / (1 + xcross * np.abs(np.sin(phi)))
    return x, y


if __name__ == "__main__":
    # Generate training data
    n_samples = 400
    xm = 1
    phi = 11 * np.pi / 12
    xcross = 0.5
    x, y = gen_data(n_samples=n_samples, xm=xm, phi=phi, xcross=xcross)

    # Sigmoid parameters
    sim = True
    N_cycl = 1
    J0 = 1
    a = 1

    # Gradient descent
    N = 250  # Number of iterations in gradient descent
    w = np.zeros((N + 1, 2))  # Weight array
    w0 = 0.5  # Initial weight
    w[0] = np.full(shape=2, fill_value=w0)
    w[0] = np.random.rand(2)  # Choose random initial weights
    alpha = 0.02  # Learning rate

    for i in range(N):
        s = sigmoid(np.sum(x * w[i], axis=1) / xm + J0, sim=sim, N_cycl=N_cycl, J0=J0)
        gradL = -np.sum(
            x * (y[:, np.newaxis] - s[:, np.newaxis]), axis=0  # pyright: ignore
        )
        w[i + 1] = w[i] - alpha * gradL

    # Results presentation
    plt.figure(figsize=(12, 4))

    # Weight values as a function of the number of gradient descent steps
    plt.subplot(1, 2, 1)
    plt.plot(w)
    plt.xlabel("Number of gradient descent steps")
    plt.ylabel("Weight values")
    if sim:
        plt.text(
            0,
            0.95 * np.max(w),  # pyright: ignore
            rf"$N_{{cycl}}$={N_cycl}",
            fontsize="x-large",  # pyright: ignore
        )
    else:
        plt.text(0, 0.95 * np.max(w), "Sigmoid", fontsize="x-large")  # pyright: ignore

    # Training and test data, colors are inverted between them for clarity
    # Heat map of probability of belonging to class 1 depending on coordinates
    # with a large number of s-wire measurements
    plt.subplot(1, 2, 2)
    xtest = np.linspace(-xm, xm, 101)  # Test data field
    xmesh = (
        xtest[:, np.newaxis] * w[-1][0] + xtest[np.newaxis, :] * w[-1][1]
    )  # Test data field
    cm = plt.pcolormesh(
        xtest,
        xtest,
        sigmoid(xmesh / xm + J0, sim=False, J0=J0, a=1),
        cmap="coolwarm_r",
        vmin=0,
        vmax=1,
    )  # Heat map
    plt.scatter(x[:, 1], x[:, 0], c=y, cmap="seismic", edgecolor="k")  # Training data
    plt.plot(
        xtest * np.sin(phi), -xtest * np.cos(phi), c="k"
    )  # Original line along which data separation occurred
    plt.colorbar(cm, label="Probability")

    plt.show()
