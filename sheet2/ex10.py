import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
g = 9.81  # gravity [m/s^2]
h = 2.0  # total vertical drop from A to D [m]
l_incline = 3.0  # length of the incline [m]
angle = np.pi / 6  # 30° incline

# Derived quantities
v_final = np.sqrt(2 * g * h)  # final speed (same for both)

# Times for each path
# Path 1: small roll (A->B) then free fall (B->D)
# roll distance
h_roll = 0.5
v_B = np.sqrt(2 * g * h_roll)

# free fall from height (h - h_roll)
t_fall1 = np.sqrt(2 * (h - h_roll) / g)

# roll time on small incline (s = 0.5*a*t^2, with a = g*sin(theta))
a_roll = g * np.sin(angle)
t_roll1 = np.sqrt(2 * (h_roll) / a_roll)

T1 = t_roll1 + t_fall1

# Path 2: free fall (A->C) then roll on incline (C->D)
h_free = 1.0
v_C = np.sqrt(2 * g * h_free)

# free fall time
t_fall2 = np.sqrt(2 * h_free / g)

# rolling down incline of length l_incline with initial speed v_C
a_roll2 = g * np.sin(angle)
s_total = l_incline
# solve quadratic: s = v0*t + 0.5*a*t^2
coeff = [0.5 * a_roll2, v_C, -s_total]
sol = np.roots(coeff)
t_roll2 = np.max(sol)

T2 = t_fall2 + t_roll2

# Simulation timeline
t_max = max(T1, T2)
ts = np.linspace(0, t_max, 300)


# Speeds as function of time
def speed_path1(t):
    if t < t_roll1:
        return a_roll * t
    elif t < T1:
        tau = t - t_roll1
        return np.sqrt(v_B**2 + (g * tau) ** 2)
    else:
        return v_final


def speed_path2(t):
    if t < t_fall2:
        return g * t
    elif t < T2:
        tau = t - t_fall2
        return v_C + a_roll2 * tau
    else:
        return v_final


v1 = [speed_path1(t) for t in ts]
v2 = [speed_path2(t) for t in ts]

# --- Animation ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Left: paths
ax1.set_xlim(0, 4)
ax1.set_ylim(-h - 0.5, 0.5)
ax1.set_title("Paths A→B→D (red) and A→C→D (blue)")
ax1.plot([0, 1], [0, -h_roll], "r--")  # AB
ax1.plot([1, 2], [-h_roll, -h], "r--")  # BD
ax1.plot([0, 1], [0, -h_free], "b--")  # AC
ax1.plot([1, 3], [-h_free, -h], "b--")  # CD

(ball1,) = ax1.plot([], [], "ro", markersize=10)
(ball2,) = ax1.plot([], [], "bo", markersize=10)

# Right: speed vs time
ax2.set_xlim(0, t_max)
ax2.set_ylim(0, v_final * 1.2)
ax2.set_xlabel("time [s]")
ax2.set_ylabel("speed [m/s]")
ax2.set_title("Speed vs. time")
(line1,) = ax2.plot([], [], "r-", label="Path 1")
(line2,) = ax2.plot([], [], "b-", label="Path 2")
ax2.legend()

v1_data, v2_data, t_data = [], [], []


# Position functions (simplified schematic)
def pos_path1(t):
    if t < t_roll1:
        x = 1.0 * t / t_roll1
        y = -h_roll * (t / t_roll1)
    elif t < T1:
        tau = (t - t_roll1) / t_fall1
        x = 1 + (1 * tau)
        y = -h_roll - (h - h_roll) * tau
    else:
        x, y = 2, -h
    return x, y


def pos_path2(t):
    if t < t_fall2:
        tau = t / t_fall2
        x = 1.0 * tau
        y = -h_free * tau
    elif t < T2:
        tau = (t - t_fall2) / t_roll2
        x = 1 + 2 * tau
        y = -h_free - (h - h_free) * tau
    else:
        x, y = 3, -h
    return x, y


# Update function
def update(frame):
    t = ts[frame]
    # ball positions
    x1, y1 = pos_path1(t)
    x2, y2 = pos_path2(t)
    ball1.set_data([x1], [y1])
    ball2.set_data([x2], [y2])
    # speed data
    t_data.append(t)
    v1_data.append(speed_path1(t))
    v2_data.append(speed_path2(t))
    line1.set_data(t_data, v1_data)
    line2.set_data(t_data, v2_data)
    return ball1, ball2, line1, line2


ani = animation.FuncAnimation(fig, update, frames=len(ts), interval=30, blit=True)
plt.tight_layout()
plt.show()
