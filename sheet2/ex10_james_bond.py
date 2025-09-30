import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -----------------------------
# Parameters
# -----------------------------
g = 9.81  # gravity (m/s^2)

# Stage and Bond setup
stage_height = 4.0  # m
x0_bond = 0.0
y0_bond = stage_height

# Boat setup
boat_length = 5.0  # m
boat_height = 0.5  # m
boat_x0 = 10.0  # m from stage
boat_speed = 30 / 3.6  # km/h -> m/s

# Simulation setup
dt = 0.02  # time step
T_max = 2.0  # simulation max time (s)


# -----------------------------
# Functions
# -----------------------------
def bond_trajectory(v0_kmh):
    """Return x(t), y(t) arrays for Bond's trajectory."""
    v0_ms = v0_kmh / 3.6  # convert km/h to m/s
    vx = v0_ms
    vy = 0

    t = np.arange(0, T_max, dt)
    x = x0_bond + vx * t
    y = y0_bond + vy * t - 0.5 * g * t**2
    return t, x, y


def boat_position(t):
    """Return x_left(t), x_right(t), y_bottom, y_top for boat."""
    x_left = boat_x0 + boat_speed * t
    x_right = x_left + boat_length
    return x_left, x_right, 0, boat_height


# -----------------------------
# Animation Function
# -----------------------------
def animate_jump(v0_kmh):
    t_vals, x_vals, y_vals = bond_trajectory(v0_kmh)

    fig, ax = plt.subplots()
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 6)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"James Bond jumping with v0 = {v0_kmh} km/h")

    # Objects
    (bond_dot,) = ax.plot([], [], "ro", label="007")
    (traj_line,) = ax.plot([], [], "r--", lw=1)
    boat_patch = plt.Rectangle(
        (boat_x0, 0), boat_length, boat_height, fc="blue", alpha=0.6, label="Boat"
    )
    ax.add_patch(boat_patch)
    status_text = ax.text(
        0.5, 0.9, "", transform=ax.transAxes, ha="center", fontsize=12, color="darkred"
    )

    ax.legend()

    # State variables
    stopped = {"done": False}

    def init():
        bond_dot.set_data([], [])
        traj_line.set_data([], [])
        boat_patch.set_xy((boat_x0, 0))
        status_text.set_text("")
        return bond_dot, traj_line, boat_patch, status_text

    def update(frame):
        if stopped["done"]:
            return bond_dot, traj_line, boat_patch, status_text

        t = t_vals[frame]
        x, y = x_vals[frame], y_vals[frame]

        # Update Bond
        bond_dot.set_data([x], [y])
        traj_line.set_data(x_vals[:frame], y_vals[:frame])

        # Update boat
        x_left, x_right, _, top = boat_position(t)
        boat_patch.set_xy((x_left, 0))

        # --- Stop conditions ---
        if (x_left <= x <= x_right) and (0 <= y <= top):
            status_text.set_text("Success! 007 landed on the boat.")
            stopped["done"] = True
        elif y <= 0:
            status_text.set_text("Missed! 007 fell into the water.")
            stopped["done"] = True

        return bond_dot, traj_line, boat_patch, status_text

    ani = animation.FuncAnimation(
        fig,
        update,
        frames=len(t_vals),
        init_func=init,
        blit=True,
        interval=dt * 1000,
        repeat=False,
    )
    plt.show()


# -----------------------------
# Example Run
# -----------------------------
if __name__ == "__main__":
    # Try different velocities to test
    animate_jump(v0_kmh=80)
