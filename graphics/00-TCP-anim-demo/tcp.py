import math
import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Set random seed for reproducibility
np.random.seed(42)


def generate_cities(num_cities, width=1000, height=1000):
    """Generate random city coordinates"""
    cities = np.random.randint(0, [width, height], size=(num_cities, 2))
    return cities


def calculate_distance(city1, city2):
    """Calculate Euclidean distance between two cities"""
    return np.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def calculate_route_length(route, cities):
    """Calculate the total length of a route"""
    total_distance = 0
    for i in range(len(route)):
        total_distance += calculate_distance(
            cities[route[i]], cities[route[(i + 1) % len(route)]]
        )
    return total_distance


def simulated_annealing(
    cities,
    initial_temp=1000,
    cooling_rate=0.995,
    stopping_temp=1e-8,
    stopping_iter=100000,
):
    """Solve TSP using simulated annealing"""
    num_cities = len(cities)

    # Initialize with a random route
    current_route = list(range(num_cities))
    random.shuffle(current_route)

    current_distance = calculate_route_length(current_route, cities)
    best_route = current_route.copy()
    best_distance = current_distance

    # Initialize temperature and iteration counters
    temp = initial_temp
    iteration = 1

    # Store routes and distances for animation
    routes_history = [best_route.copy()]
    distances_history = [best_distance]
    temps_history = [temp]

    # Simulated annealing loop
    while temp > stopping_temp and iteration < stopping_iter:
        # Create a new candidate route by swapping two random cities
        candidate_route = current_route.copy()
        i, j = sorted(random.sample(range(num_cities), 2))

        # Swap segment between i and j (2-opt move)
        candidate_route[i : j + 1] = reversed(candidate_route[i : j + 1])

        # Calculate new route distance
        candidate_distance = calculate_route_length(candidate_route, cities)

        # Decide whether to accept the new solution
        delta = candidate_distance - current_distance
        acceptance_probability = math.exp(-delta / temp) if delta > 0 else 1.0

        if acceptance_probability > random.random():
            current_route = candidate_route
            current_distance = candidate_distance

            # Update the best route if we found a better one
            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance

        # Cooling schedule
        temp *= cooling_rate
        iteration += 1

        # Save route history occasionally to reduce memory usage
        if iteration % 100 == 0 or temp < stopping_temp:
            routes_history.append(current_route.copy())
            distances_history.append(current_distance)
            temps_history.append(temp)  # pyright: ignore

    return best_route, best_distance, routes_history, distances_history, temps_history


def animate_tsp(
    cities,
    routes_history,
    distances_history,
    temps_history,
    milliseconds_between_frames,
):
    """Create an animation of the TSP solution process"""
    fig = plt.figure(figsize=(15, 8))
    gs = fig.add_gridspec(2, 2)
    ax1 = fig.add_subplot(gs[:, 0])  # Route plot (left, full height)
    ax2 = fig.add_subplot(gs[0, 1])  # Distance plot (top right)
    ax3 = fig.add_subplot(gs[1, 1])  # Temperature plot (bottom right)

    fig.suptitle("Traveling Salesman Problem - Simulated Annealing")

    # Plot the cities
    x = cities[:, 0]
    y = cities[:, 1]
    ax1.scatter(x, y, color="red", zorder=10)

    # For route lines
    (route_line,) = ax1.plot([], [], "b-", linewidth=1.5, alpha=0.7)

    # For distance progress
    iterations = list(range(len(distances_history)))
    ax2.plot(iterations, distances_history, "g-", alpha=0.5)
    (progress_line,) = ax2.plot([], [], "go-")
    ax2.set_xlabel("Iteration (scaled)")
    ax2.set_ylabel("Route Distance")
    ax2.set_title("Optimization Progress")

    # For temperature progress
    ax3.plot(iterations, temps_history, "r-", alpha=0.5)
    (temp_line,) = ax3.plot([], [], "ro-")
    ax3.set_xlabel("Iteration (scaled)")
    ax3.set_ylabel("Temperature")
    ax3.set_title("Cooling Schedule")
    ax3.set_yscale("log")

    # Add city labels
    for i, (x_pos, y_pos) in enumerate(cities):
        ax1.annotate(str(i), (x_pos, y_pos), xytext=(5, 5), textcoords="offset points")

    # Set fixed axis limits for the route plot
    x_margin = (max(x) - min(x)) * 0.1
    y_margin = (max(y) - min(y)) * 0.1
    ax1.set_xlim(min(x) - x_margin, max(x) + x_margin)
    ax1.set_ylim(min(y) - y_margin, max(y) + y_margin)
    ax1.set_title("City Route")

    # Text for current stats
    stats_text = ax1.text(
        0.02,
        0.02,
        "",
        transform=ax1.transAxes,
        fontsize=9,
        bbox=dict(facecolor="white", alpha=0.7),
    )

    # Animation update function
    def update(frame):
        route = routes_history[frame]

        # Get ordered coordinates for the route
        route_x = [cities[route[i], 0] for i in range(len(route))]
        route_y = [cities[route[i], 1] for i in range(len(route))]

        # Add the first city to close the loop
        route_x.append(cities[route[0], 0])
        route_y.append(cities[route[0], 1])

        # Update route line
        route_line.set_data(route_x, route_y)

        # Update progress indicators
        progress_line.set_data(iterations[: frame + 1], distances_history[: frame + 1])
        temp_line.set_data(iterations[: frame + 1], temps_history[: frame + 1])

        # Update stats text
        stats_text.set_text(
            f"Iteration: {frame * 100}\nDistance: {distances_history[frame]:.2f}\nTemperature: {temps_history[frame]:.4f}"
        )

        return route_line, progress_line, temp_line, stats_text

    # Create animation
    animation = FuncAnimation(
        fig,
        update,
        frames=len(routes_history),
        interval=milliseconds_between_frames,  # milliseconds between frames
        blit=True,
        repeat=True,
    )

    plt.tight_layout()
    return animation


def main():
    # Parameters
    num_cities = 25
    initial_temp = 1000
    cooling_rate = 0.995

    # Generate random cities
    cities = generate_cities(num_cities)

    print(f"Solving TSP for {num_cities} cities using simulated annealing...")

    # Solve using simulated annealing
    best_route, best_distance, routes_history, distances_history, temps_history = (
        simulated_annealing(
            cities, initial_temp=initial_temp, cooling_rate=cooling_rate
        )
    )

    print(f"Best route found with distance: {best_distance:.2f}")

    # Create animation
    animation = animate_tsp(
        cities,
        routes_history,
        distances_history,
        temps_history,
        milliseconds_between_frames=300,
    )

    # Save animation as a file (uncomment to save)
    animation.save("tsp_simulated_annealing.gif", writer="ffmpeg", fps=4, dpi=200)

    # Show the animation
    plt.show()


if __name__ == "__main__":
    main()
