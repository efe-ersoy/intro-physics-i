import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# --- Physical constants ---
G = 6.67430e-11  # gravitational constant [m^3/kg/s^2]
M_earth = 5.972e24  # mass of Earth [kg]
GM = G * M_earth
R_earth_real = 6.371e6  # Earth radius [m]
T_earth = 24 * 3600  # Earth's rotation period [s]

# --- Geostationary orbit ---
T_geo = T_earth
r_geo_real = (GM * (T_geo / (2 * np.pi)) ** 2) ** (1 / 3)

# --- Define orbits ---
r_close_real = 4 ** (-1 / 3) * r_geo_real  # too close, faster orbit
r_geo_real = r_geo_real  # geostationary orbit
r_far_real = 4 ** (1 / 3) * r_geo_real  # too far, slower orbit


# Compute periods from physics
def orbital_period(r):
    return 2 * np.pi * np.sqrt(r**3 / GM)


T_close = orbital_period(r_close_real)
T_geo = orbital_period(r_geo_real)
T_far = orbital_period(r_far_real)

# --- Scaling for plotting ---
R_earth = 5.0  # scaled Earth radius in plot
scale = R_earth / R_earth_real

r_close = r_close_real * scale
r_geo = r_geo_real * scale
r_far = r_far_real * scale

# --- Time setup ---
frames = 500
interval = 30
sim_time = 3 * T_earth  # simulate for 1.5 Earth days
times = np.linspace(0, sim_time, frames)


# --- Position functions ---
def sat_pos(r, T, t):
    theta = 2 * np.pi * t / T
    return r * np.cos(theta), r * np.sin(theta)


def earth_marker(t):
    # Position of a reference point on equator (longitude marker)
    theta = 2 * np.pi * t / T_earth
    return R_earth * np.cos(theta), R_earth * np.sin(theta)


# --- Set up figure ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect("equal")
ax.set_xlim(-1.5 * r_far, 1.5 * r_far)
ax.set_ylim(-1.5 * r_far, 1.5 * r_far)
ax.set_title("Geostationary Orbit Demo (scaled)")

# Draw Earth
earth = plt.Circle((0, 0), R_earth, color="lightblue", zorder=1)
ax.add_patch(earth)

# Satellites
(sat_close,) = ax.plot([], [], "ro", label=f"Too close (T={T_close / 3600:.1f} h)")
(sat_geo,) = ax.plot([], [], "go", label=f"Geostationary (T={T_geo / 3600:.1f} h)")
(sat_far,) = ax.plot([], [], "bo", label=f"Too far (T={T_far / 3600:.1f} h)")

# Earth reference marker
(marker,) = ax.plot([], [], "kx", markersize=10, label="Reference point")
ax.legend(loc="upper right")


# --- Update function ---
def update(frame):
    t = times[frame]

    # Satellite positions
    x1, y1 = sat_pos(r_close, T_close, t)
    x2, y2 = sat_pos(r_geo, T_geo, t)
    x3, y3 = sat_pos(r_far, T_far, t)
    sat_close.set_data([x1], [y1])
    sat_geo.set_data([x2], [y2])
    sat_far.set_data([x3], [y3])

    # Earth reference point
    xm, ym = earth_marker(t)
    marker.set_data([xm], [ym])

    return sat_close, sat_geo, sat_far, marker


ani = animation.FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)
plt.show()
