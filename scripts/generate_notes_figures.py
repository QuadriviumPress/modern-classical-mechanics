"""Regenerate introductory mechanics diagrams used in the course notes."""

import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "mcm-matplotlib"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Polygon, Rectangle, Wedge


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "images" / "notes"

BLUE = "#377eb8"
RED = "#d73027"
BLACK = "#202020"


def save(fig, relative_path):
    path = OUT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, bbox_inches="tight", pad_inches=0.08, facecolor="white")
    plt.close(fig)


def arrow(ax, start, end, *, color=BLACK, label=None, label_offset=(0, 0), **kwargs):
    ax.annotate(
        "", xy=end, xytext=start,
        arrowprops={"arrowstyle": "->", "lw": 2, "color": color, **kwargs},
    )
    if label:
        midpoint = (np.asarray(start) + np.asarray(end)) / 2
        ax.text(*(midpoint + label_offset), label, color=color, fontsize=15, ha="center")


def vector_components():
    fig, ax = plt.subplots(figsize=(4.4, 4.8))
    ax.set_aspect("equal")
    arrow(ax, (0, 0), (4.2, 0))
    arrow(ax, (0, 0), (0, 5.0))
    ax.text(4.28, -0.08, r"$x$", fontsize=14)
    ax.text(-0.12, 5.12, r"$y$", fontsize=14)
    endpoint = np.array([3.0, 4.0])
    arrow(ax, (0, 0), endpoint, color=RED, label=r"$\vec{A}$", label_offset=(-0.42, 0.18))
    ax.plot([endpoint[0], endpoint[0]], [0, endpoint[1]], "--", color=RED, lw=1.2)
    ax.plot([0, endpoint[0]], [endpoint[1], endpoint[1]], "--", color=RED, lw=1.2)
    ax.plot([endpoint[0], endpoint[0] - 0.35], [0, 0], color=BLACK, lw=1)
    ax.plot([endpoint[0], endpoint[0]], [0, 0.35], color=BLACK, lw=1)
    ax.add_patch(Arc((0, 0), 1.5, 1.5, theta1=0, theta2=53.1, lw=1.2))
    ax.text(0.92, 0.32, r"$\theta$", fontsize=14)
    ax.text(1.45, -0.47, r"$A_x = A\cos\theta$", color=RED, fontsize=13, ha="center")
    ax.text(3.3, 2.0, r"$A_y = A\sin\theta$", color=RED, fontsize=13, rotation=90, va="center")
    ax.set(xlim=(-0.55, 4.5), ylim=(-0.8, 5.35))
    ax.axis("off")
    save(fig, "week2/2dvector.png")


def dot_product():
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.set_aspect("equal")
    arrow(ax, (0, 0), (0, 4.5), label=r"$\vec{b}$", label_offset=(-0.36, 0.15))
    arrow(ax, (0, 0), (3.8, 2.0), label=r"$\vec{a}$", label_offset=(0.2, 0.18))
    ax.add_patch(Wedge((0, 0), 0.95, 27.8, 90, facecolor="#cdecc9", edgecolor="none"))
    ax.add_patch(Arc((0, 0), 1.9, 1.9, theta1=27.8, theta2=90, fill=False, lw=1.1))
    ax.text(0.55, 1.18, r"$\phi$", fontsize=16)
    ax.set(xlim=(-0.7, 4.45), ylim=(-0.55, 4.9))
    ax.axis("off")
    save(fig, "week2/Dot-product.png")


def falling_ball():
    fig, ax = plt.subplots(figsize=(3.0, 3.15))
    ax.set_aspect("equal")
    ball = (0, 1.75)
    ax.add_patch(Circle(ball, 0.38, facecolor=RED, edgecolor=BLACK, lw=1.2))
    ax.plot([0, 0], [0.32, 1.32], color=BLACK, lw=1.8)
    arrow(ax, (1.15, 2.55), (1.15, 0.32), label=r"$+y$", label_offset=(0.38, 0.02))
    arrow(ax, ball, (0, 0.55), color=BLACK)
    ax.text(-0.18, 1.03, r"$\vec{W}=m\vec{g}$", fontsize=16, ha="right")
    ax.set(xlim=(-1.3, 2.0), ylim=(0, 3.0))
    ax.axis("off")
    save(fig, "week3/1d-ball-fbd.png")


def spring(ax, x0, x1, y=0, coils=8, amplitude=0.18):
    lead = 0.25
    xs = [x0, x0 + lead]
    ys = [y, y]
    coil_x = np.linspace(x0 + lead, x1 - lead, 2 * coils + 1)
    for index, x in enumerate(coil_x):
        xs.append(x)
        ys.append(y if index in (0, len(coil_x) - 1) else y + amplitude * (-1) ** index)
    xs.extend([x1 - lead, x1])
    ys.extend([y, y])
    ax.plot(xs, ys, color=BLACK, lw=1.7)


def simple_harmonic_oscillator():
    fig, ax = plt.subplots(figsize=(5.1, 3.2))
    ax.plot([-0.2, 5.5], [0, 0], color=BLACK, lw=1.5)
    ax.plot([0, 0], [-0.45, 1.0], color=BLACK, lw=2.5)
    for y in np.linspace(-0.4, 0.95, 8):
        ax.plot([-0.2, 0], [y - 0.1, y + 0.1], color=BLACK, lw=1)
    spring(ax, 0, 2.75, y=0.4)
    ax.add_patch(Rectangle((2.75, 0.0), 1.35, 0.82, facecolor="#55a7d9", edgecolor=BLACK, lw=1.2))
    ax.text(3.42, 0.41, r"$m$", fontsize=16, ha="center", va="center")
    ax.plot([2.75, 2.75], [0, -0.42], "--", color="0.35", lw=1)
    ax.text(2.6, -0.67, r"$x_0$", fontsize=13)
    ax.text(1.32, 0.82, r"$k$", fontsize=15)
    arrow(ax, (-0.1, -0.02), (5.15, -0.02))
    ax.text(5.22, -0.14, r"$x$", fontsize=14)
    ax.set(xlim=(-0.55, 5.5), ylim=(-0.9, 1.28))
    ax.axis("off")
    save(fig, "week3/sho_horizontal.png")


def drag_coordinate_system():
    fig, ax = plt.subplots(figsize=(4.5, 4.2))
    ax.set_aspect("equal")
    arrow(ax, (0, 0), (4.15, 0), label=r"$+x$", label_offset=(0.08, -0.32))
    arrow(ax, (0, 0), (0, 4.15), label=r"$+y$", label_offset=(-0.32, 0.08))
    particle = np.array([2.0, 2.3])
    ax.add_patch(Circle(particle, 0.13, color=BLUE))
    arrow(ax, particle, (3.4, 1.12), color=BLUE, label=r"$\vec{v}$", label_offset=(0.15, -0.12))
    ax.set(xlim=(-0.55, 4.55), ylim=(-0.55, 4.55))
    ax.axis("off")
    save(fig, "week4/2d-falling-ball.png")


def drag_free_body_diagram():
    fig, ax = plt.subplots(figsize=(4.5, 4.2))
    ax.set_aspect("equal")
    arrow(ax, (0, 0), (4.15, 0), label=r"$+x$", label_offset=(0.08, -0.32))
    arrow(ax, (0, 0), (0, 4.15), label=r"$+y$", label_offset=(-0.32, 0.08))
    particle = np.array([2.0, 2.3])
    ax.add_patch(Circle(particle, 0.13, color=BLUE))
    arrow(ax, particle, (1.05, 3.32), color=BLUE, label=r"$\vec{F}_{\mathrm{drag}}$", label_offset=(-0.18, 0.18))
    arrow(ax, particle, (2.0, 0.92), color=BLUE, label=r"$\vec{F}_{\mathrm{gravity}}$", label_offset=(0.65, -0.02))
    ax.set(xlim=(-0.55, 4.75), ylim=(-0.55, 4.55))
    ax.axis("off")
    save(fig, "week4/2d-falling-ball-fbd.png")


def discrete_force_intervals():
    fig, ax = plt.subplots(figsize=(7.2, 3.7))
    x = np.array([0.5, 1.7, 3.0, 4.5, 6.2])
    heights = np.array([1.2, 2.25, 1.65, 2.55])
    ax.annotate("", xy=(6.8, 0), xytext=(0.1, 0), arrowprops={"arrowstyle": "->", "lw": 1.8})
    ax.annotate("", xy=(0.25, 3.15), xytext=(0.25, 0), arrowprops={"arrowstyle": "->", "lw": 1.8})
    for left, right, height in zip(x[:-1], x[1:], heights):
        ax.add_patch(Rectangle((left, 0), right - left, height, fill=False, edgecolor=BLUE, lw=2))
        ax.plot((left + right) / 2, height, "o", color=BLACK, ms=4)
        ax.text((left + right) / 2, height + 0.18, r"$F(x_i)$", fontsize=12, ha="center")
    for point, label in zip(x, [r"$x_0$", r"$x_1$", r"$x_2$", r"$\cdots$", r"$x_n$"]):
        ax.text(point, -0.3, label, fontsize=12, ha="center")
    ax.annotate("", xy=(x[1], 0.4), xytext=(x[0], 0.4), arrowprops={"arrowstyle": "<->", "lw": 1.1})
    ax.text((x[0] + x[1]) / 2, 0.53, r"$\Delta x_i$", fontsize=12, ha="center")
    ax.text(6.85, -0.08, r"$x$", fontsize=14)
    ax.text(0.02, 3.18, r"$F(x)$", fontsize=14)
    ax.set(xlim=(0, 7.1), ylim=(-0.55, 3.45))
    ax.axis("off")
    save(fig, "week5/discrete-force-intervals.png")


def path_integral_work():
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    t = np.linspace(0, 1, 300)
    x = 0.4 + 6.3 * t
    y = 0.7 + 0.4 * np.sin(2 * np.pi * t) + 1.45 * t
    ax.plot(x, y, color=BLACK, lw=2)
    sample = np.array([0.08, 0.28, 0.49, 0.7, 0.9])
    for index, value in enumerate(sample):
        point = np.array([0.4 + 6.3 * value, 0.7 + 0.4 * np.sin(2 * np.pi * value) + 1.45 * value])
        tangent = np.array([6.3, 0.8 * np.pi * np.cos(2 * np.pi * value) + 1.45])
        tangent /= np.linalg.norm(tangent)
        normal = np.array([-tangent[1], tangent[0]])
        ax.plot(*point, "o", color=RED, ms=4)
        arrow(ax, point, point + 0.48 * tangent, color=RED)
        arrow(ax, point, point + 0.6 * normal, color=BLUE)
        if index in (1, 3):
            ax.text(*(point + 0.7 * normal), r"$\vec{F}_i$", color=BLUE, fontsize=13)
            ax.text(*(point + 0.5 * tangent + np.array([0.05, -0.22])), r"$\Delta\vec{r}_i$", color=RED, fontsize=12)
    ax.text(0.12, 0.45, r"$\vec{r}_0$", fontsize=13)
    ax.text(6.82, 2.15, r"$\vec{r}_n$", fontsize=13)
    ax.text(3.25, 2.62, r"$C$", fontsize=15)
    ax.set(xlim=(-0.1, 7.35), ylim=(0.1, 3.2))
    ax.axis("off")
    save(fig, "week5/path-integral-work.png")


def lattice_chain():
    fig, ax = plt.subplots(figsize=(7.2, 2.8))
    ax.annotate("", xy=(6.8, 0), xytext=(0.2, 0), arrowprops={"arrowstyle": "->", "lw": 1.7})
    atoms = np.linspace(1.45, 5.85, 8)
    for position in atoms:
        ax.add_patch(Circle((position, 0), 0.11, facecolor="0.75", edgecolor=BLACK, lw=1))
    ax.add_patch(Circle((0.6, 0), 0.14, facecolor=RED, edgecolor=BLACK, lw=1))
    ax.annotate("", xy=(2.08, -0.32), xytext=(1.45, -0.32), arrowprops={"arrowstyle": "<->", "lw": 1})
    ax.text(1.77, -0.62, r"$b$", fontsize=13, ha="center")
    ax.text(0.45, 0.34, "electron", fontsize=12, ha="center")
    ax.text(0.6, -0.55, r"$x_0=0$, $v_0=0$", fontsize=12, ha="center")
    ax.text(6.86, -0.12, r"$x$", fontsize=14)
    ax.set(xlim=(0, 7.15), ylim=(-0.95, 1.15))
    ax.axis("off")
    save(fig, "week5/lattice-chain.png")


def closed_path_work():
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    start, end = np.array([0.55, 0.65]), np.array([6.35, 2.0])
    t = np.linspace(0, 1, 300)
    upper = np.column_stack((start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t + 1.0 * np.sin(np.pi * t)))
    lower = np.column_stack((start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t - 0.8 * np.sin(np.pi * t)))
    ax.plot(upper[:, 0], upper[:, 1], color=BLUE, lw=2)
    ax.plot(lower[:, 0], lower[:, 1], color=RED, lw=2)
    for curve, fraction, label, color, offset in [
        (upper, 0.28, r"$C_1$", BLUE, (0.0, 0.25)),
        (upper, 0.73, r"$C_2$", BLUE, (0.0, 0.25)),
        (lower, 0.28, r"$C_3$", RED, (0.0, -0.35)),
        (lower, 0.73, r"$C_4$", RED, (0.0, -0.35)),
    ]:
        index = int(fraction * (len(curve) - 1))
        point, next_point = curve[index], curve[index + 6]
        arrow(ax, point, next_point, color=color)
        ax.text(*(point + offset), label, color=color, fontsize=13, ha="center")
    ax.plot(*start, "ko", ms=4)
    ax.plot(*end, "ko", ms=4)
    ax.text(*(start + np.array([-0.15, -0.32])), r"$A$", fontsize=13)
    ax.text(*(end + np.array([0.08, 0.12])), r"$B$", fontsize=13)
    ax.text(3.15, 2.95, r"$\oint_C \vec{F}\cdot d\vec{r}=0$", fontsize=15)
    ax.set(xlim=(0, 7.1), ylim=(-0.65, 3.45))
    ax.axis("off")
    save(fig, "week5/closed-path-work.png")


def driven_oscillator():
    fig, ax = plt.subplots(figsize=(7.4, 2.9))
    ax.plot([0.35, 6.9], [0, 0], color=BLACK, lw=1.4)
    ax.plot([0.6, 0.6], [0, 1.8], color=BLACK, lw=2.5)
    for y in np.linspace(0.1, 1.7, 8):
        ax.plot([0.4, 0.6], [y - 0.12, y + 0.12], color=BLACK, lw=1)
    spring(ax, 0.6, 3.1, y=0.9, coils=7, amplitude=0.18)
    ax.text(1.7, 1.3, r"$k$", color=BLUE, fontsize=15)
    ax.add_patch(Rectangle((3.1, 0.4), 1.05, 1.0, facecolor="#e95b54", edgecolor=BLACK, lw=1.2))
    ax.text(3.63, 0.88, r"$m$", fontsize=16, ha="center", va="center")
    ax.plot([4.15, 4.65], [0.9, 0.9], color=BLACK, lw=2)
    ax.add_patch(Rectangle((4.65, 0.55), 0.27, 0.7, facecolor="#75b879", edgecolor=BLACK, lw=1.1))
    ax.plot([4.92, 5.4], [0.9, 0.9], color=BLACK, lw=2)
    ax.text(4.75, 1.42, r"$b$", color="#3b8a3e", fontsize=15)
    ax.add_patch(Circle((5.85, 0.9), 0.33, fill=False, edgecolor=BLACK, lw=1.4))
    ax.plot([5.4, 5.52], [0.9, 0.9], color=BLACK, lw=2)
    ax.plot([5.85, 6.1], [0.9, 1.15], color=BLACK, lw=1.3)
    arrow(ax, (6.8, 0.9), (6.2, 0.9), label=r"$F(t)$", label_offset=(0, 0.25))
    ax.text(5.85, 0.2, "driver", fontsize=11, ha="center")
    ax.set(xlim=(0.05, 7.15), ylim=(-0.35, 2.15))
    ax.axis("off")
    save(fig, "week9/driven_oscillator.png")


def resonance_curve():
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    omega = np.linspace(0, 1.8, 600)
    beta = 0.08
    amplitude = 1 / np.sqrt((1 - omega**2) ** 2 + (2 * beta * omega) ** 2)
    ax.plot(omega, amplitude, color=RED, lw=2.5)
    peak = np.sqrt(1 - 2 * beta**2)
    ax.axvline(peak, color="0.35", lw=1.1, ls="--")
    ax.annotate("resonance", xy=(peak, amplitude.max()), xytext=(1.25, amplitude.max() * 0.8),
                arrowprops={"arrowstyle": "->", "lw": 1.1}, fontsize=13)
    ax.set(xlim=(0, 1.8), ylim=(0, amplitude.max() * 1.15), xlabel=r"Driving frequency, $\omega/\omega_0$", ylabel="Amplitude")
    ax.set_yticks([])
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.2)
    fig.tight_layout()
    save(fig, "week9/resonance.png")


def complex_conjugates():
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    ax.axhline(0, color=BLACK, lw=1.2)
    ax.axvline(0, color=BLACK, lw=1.2)
    z = np.array([2.7, 1.8])
    conjugate = np.array([2.7, -1.8])
    arrow(ax, (0, 0), z, color=BLUE)
    arrow(ax, (0, 0), conjugate, color=RED)
    ax.plot([z[0], z[0]], [conjugate[1], z[1]], "--", color="0.45", lw=1)
    ax.text(2.88, 1.9, r"$z=a+ib$", color=BLUE, fontsize=14)
    ax.text(2.88, -2.18, r"$z^*=a-ib$", color=RED, fontsize=14)
    ax.text(3.85, 0.2, "Real", fontsize=12)
    ax.text(0.15, 2.55, "Imaginary", fontsize=12, rotation=90)
    ax.text(1.25, 0.2, r"$a$", fontsize=13)
    ax.text(0.18, 1.0, r"$b$", fontsize=13)
    ax.text(0.18, -1.1, r"$-b$", fontsize=13)
    ax.set(xlim=(-0.5, 4.4), ylim=(-2.7, 2.9), aspect="equal")
    ax.axis("off")
    save(fig, "week8/conjugates_graph.png")


def snells_law():
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.axvspan(-0.2, 2.5, color="#f3dfad", alpha=0.75)
    ax.axvspan(2.5, 6.8, color="#bfe4f6", alpha=0.8)
    ax.plot([2.5, 2.5], [-0.2, 4.2], color=BLACK, lw=1.6)
    source, crossing, target = np.array([0.8, 0.8]), np.array([2.5, 2.0]), np.array([5.75, 3.35])
    ax.plot(*source, "o", color=RED, ms=7)
    ax.plot(*crossing, "o", color=BLACK, ms=5)
    ax.plot(*target, "o", color=BLUE, ms=7)
    ax.plot([source[0], crossing[0]], [source[1], crossing[1]], color=RED, lw=2)
    ax.plot([crossing[0], target[0]], [crossing[1], target[1]], color=BLUE, lw=2)
    ax.plot([2.1, 2.9], [2.0, 2.0], "--", color="0.35", lw=1)
    ax.add_patch(Arc(crossing, 0.9, 0.9, theta1=145, theta2=180, lw=1.1))
    ax.add_patch(Arc(crossing, 1.15, 1.15, theta1=0, theta2=22.5, lw=1.1))
    ax.text(1.94, 2.3, r"$\theta_1$", fontsize=13)
    ax.text(3.0, 2.33, r"$\theta_2$", fontsize=13)
    ax.text(0.66, 0.36, r"$\langle x_1,y_1\rangle$", fontsize=12)
    ax.text(5.0, 3.55, r"$\langle x_2,y_2\rangle$", fontsize=12)
    ax.text(0.85, 3.65, r"shore, $v_1$", fontsize=13)
    ax.text(4.45, 0.35, r"water, $v_2<v_1$", fontsize=13)
    ax.set(xlim=(-0.1, 6.7), ylim=(-0.1, 4.05), aspect="equal")
    ax.axis("off")
    save(fig, "week11/snells_shore.png")


def brachistochrone():
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    start, end = np.array([0.45, 2.85]), np.array([6.25, 0.55])
    ax.plot([start[0], end[0]], [start[1], end[1]], color="0.45", lw=1.8, ls="--", label="straight path")
    theta = np.linspace(0, 2.42, 300)
    radius = 1.65
    x = radius * (theta - np.sin(theta))
    y = start[1] - radius * (1 - np.cos(theta))
    x *= (end[0] - start[0]) / x[-1]
    y = start[1] + (y - start[1]) * (start[1] - end[1]) / (start[1] - y[-1])
    ax.plot(start[0] + x, y, color=RED, lw=2.5, label="brachistochrone")
    ax.plot(*start, "ko", ms=5)
    ax.plot(*end, "ko", ms=5)
    ax.text(*(start + np.array([-0.18, 0.2])), r"$A$", fontsize=14)
    ax.text(*(end + np.array([0.1, -0.03])), r"$B$", fontsize=14)
    arrow(ax, (1.6, 2.6), (2.0, 2.18), color=RED)
    ax.text(3.1, 1.2, "fastest descent", color=RED, fontsize=13)
    ax.legend(frameon=False, loc="upper right", fontsize=11)
    ax.set(xlim=(0, 6.95), ylim=(0.1, 3.35))
    ax.axis("off")
    save(fig, "week11/brachistochrone.png")


def polar_coordinate_system():
    fig, ax = plt.subplots(figsize=(5.4, 4.8))
    ax.set_aspect("equal")
    arrow(ax, (0, 0), (4.35, 0), label=r"$\hat{x}$", label_offset=(0.05, -0.33))
    arrow(ax, (0, 0), (0, 4.35), label=r"$\hat{y}$", label_offset=(-0.33, 0.05))
    point = np.array([3.15, 2.55])
    arrow(ax, (0, 0), point, color=RED, label=r"$\vec r=r\hat r$", label_offset=(-0.15, 0.2))
    radial = point / np.linalg.norm(point)
    tangential = np.array([-radial[1], radial[0]])
    arrow(ax, point, point + np.array([0.65, 0]), color=BLUE, label=r"$\hat{x}$", label_offset=(0.04, -0.18))
    arrow(ax, point, point + np.array([0, 0.65]), color=BLUE, label=r"$\hat{y}$", label_offset=(0.2, 0.03))
    arrow(ax, point, point + 0.85 * radial, color="#3b8a3e", label=r"$\hat r$", label_offset=(0.05, 0.15))
    arrow(ax, point, point + 0.85 * tangential, color="#3b8a3e", label=r"$\hat\phi$", label_offset=(-0.05, 0.15))
    ax.add_patch(Arc((0, 0), 1.55, 1.55, theta1=0, theta2=np.degrees(np.arctan2(point[1], point[0])), lw=1.1))
    ax.text(0.95, 0.35, r"$\phi$", fontsize=14)
    ax.plot(*point, "o", color=BLACK, ms=4)
    ax.set(xlim=(-0.6, 4.7), ylim=(-0.6, 4.8))
    ax.axis("off")
    save(fig, "week12/coordinate-system.png")


def plane_pendulum():
    fig, ax = plt.subplots(figsize=(5.5, 4.2))
    pivot = np.array([0.0, 2.8])
    angle = np.deg2rad(32)
    length = 2.6
    bob = pivot + length * np.array([np.sin(angle), -np.cos(angle)])
    ax.plot([-2.0, 2.0], [pivot[1], pivot[1]], color=BLACK, lw=2.2)
    ax.plot([pivot[0], bob[0]], [pivot[1], bob[1]], color=BLACK, lw=1.8)
    ax.add_patch(Circle(bob, 0.18, facecolor=RED, edgecolor=BLACK, lw=1))
    ax.plot(*pivot, "ko", ms=5)
    ax.plot([pivot[0], pivot[0]], [pivot[1], -0.2], "--", color="0.45", lw=1)
    ax.add_patch(Arc(pivot, 1.2, 1.2, theta1=238, theta2=270, lw=1.1))
    ax.text(0.18, 2.05, r"$\phi$", fontsize=14)
    ax.text(0.55, 1.6, r"$l$", fontsize=14)
    arrow(ax, bob, bob + np.array([0, -0.95]), label=r"$m\vec g$", label_offset=(0.45, 0))
    arrow(ax, pivot, (2.0, pivot[1]), label=r"$x$", label_offset=(0.05, -0.28))
    arrow(ax, pivot, (pivot[0], 3.85), label=r"$y$", label_offset=(-0.28, 0.05))
    ax.text(*(bob + np.array([0.22, 0.1])), r"$m$", fontsize=14)
    ax.text(1.35, 2.95, r"$U=0$", fontsize=13)
    ax.set(xlim=(-2.1, 2.4), ylim=(-0.55, 4.15), aspect="equal")
    ax.axis("off")
    save(fig, "week12/plane-pendulum.png")


def atwood_machine():
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    center, radius = np.array([0.0, 2.55]), 0.65
    ax.add_patch(Circle(center, radius, fill=False, edgecolor=BLACK, lw=1.8))
    ax.plot([-2.1, 2.1], [3.28, 3.28], color=BLACK, lw=2.2)
    ax.plot([-radius, -radius], [2.55, 0.9], color=BLACK, lw=1.5)
    ax.plot([radius, radius], [2.55, 0.55], color=BLACK, lw=1.5)
    ax.add_patch(Rectangle((-1.08, 0.35), 0.86, 0.55, facecolor="#e95b54", edgecolor=BLACK, lw=1.1))
    ax.add_patch(Rectangle((0.22, 0.0), 0.86, 0.55, facecolor="#55a7d9", edgecolor=BLACK, lw=1.1))
    ax.text(-0.65, 0.63, r"$M$", fontsize=15, ha="center", va="center")
    ax.text(0.65, 0.28, r"$m$", fontsize=15, ha="center", va="center")
    arrow(ax, (-1.55, 0.25), (-1.55, 1.45), label=r"$+y_1$", label_offset=(-0.35, 0))
    arrow(ax, (1.55, 0.25), (1.55, 1.45), label=r"$+y_2$", label_offset=(0.35, 0))
    ax.text(-0.1, 2.5, r"$R$", fontsize=13)
    ax.set(xlim=(-2.4, 2.4), ylim=(-0.2, 3.7), aspect="equal")
    ax.axis("off")
    save(fig, "week13/atwood.png")


def unraveled_string():
    fig, ax = plt.subplots(figsize=(7.0, 2.5))
    ax.plot([0.55, 6.5], [1.35, 1.35], color=BLACK, lw=1.7)
    ax.add_patch(Rectangle((0.35, 0.85), 0.65, 0.5, facecolor="#e95b54", edgecolor=BLACK, lw=1.1))
    ax.add_patch(Rectangle((6.05, 0.85), 0.65, 0.5, facecolor="#55a7d9", edgecolor=BLACK, lw=1.1))
    ax.text(0.68, 1.1, r"$M$", fontsize=14, ha="center", va="center")
    ax.text(6.38, 1.1, r"$m$", fontsize=14, ha="center", va="center")
    ax.annotate("", xy=(0.55, 0.42), xytext=(3.55, 0.42), arrowprops={"arrowstyle": "<->", "lw": 1.1})
    ax.annotate("", xy=(3.55, 0.42), xytext=(6.5, 0.42), arrowprops={"arrowstyle": "<->", "lw": 1.1})
    ax.text(2.05, 0.12, r"$y_1$", fontsize=14, ha="center")
    ax.text(5.0, 0.12, r"$y_2$", fontsize=14, ha="center")
    ax.annotate("", xy=(2.65, 1.82), xytext=(4.35, 1.82), arrowprops={"arrowstyle": "<->", "lw": 1.1})
    ax.text(3.5, 1.98, r"$\pi R$", fontsize=14, ha="center")
    ax.text(3.5, -0.38, r"$y_1 + \pi R + y_2 = l$", fontsize=16, ha="center")
    ax.set(xlim=(0, 7.1), ylim=(-0.65, 2.25))
    ax.axis("off")
    save(fig, "week13/string-unraveled.png")


def inclined_ramp_free_body():
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    angle = np.deg2rad(28)
    ramp_start, ramp_end = np.array([0.4, 0.45]), np.array([5.9, 0.45])
    ramp_top = ramp_start + np.array([4.8 * np.cos(angle), 4.8 * np.sin(angle)])
    ax.add_patch(Polygon([ramp_start, ramp_end, ramp_top], closed=True, facecolor="#f3f3f3", edgecolor=BLACK, lw=1.5))
    center = ramp_start + np.array([2.55 * np.cos(angle), 2.55 * np.sin(angle)]) + np.array([-0.22 * np.sin(angle), 0.22 * np.cos(angle)])
    side = 0.75
    tangent, normal = np.array([np.cos(angle), np.sin(angle)]), np.array([-np.sin(angle), np.cos(angle)])
    corners = [center + sign_t * side / 2 * tangent + sign_n * side / 2 * normal for sign_t, sign_n in [(-1, -1), (1, -1), (1, 1), (-1, 1)]]
    ax.add_patch(Polygon(corners, closed=True, facecolor="#55a7d9", edgecolor=BLACK, lw=1.2))
    ax.text(*center, r"$m$", fontsize=14, ha="center", va="center")
    arrow(ax, center, center + 1.05 * normal, label=r"$N$", label_offset=(-0.22, 0.1))
    arrow(ax, center, center - 1.15 * tangent, label=r"$f_s$", label_offset=(-0.05, 0.18))
    arrow(ax, center, center + np.array([0, -1.35]), label=r"$m\vec g$", label_offset=(0.42, -0.05))
    axis_origin = ramp_start + 0.72 * tangent + 0.08 * normal
    arrow(ax, axis_origin, axis_origin + 0.95 * tangent, label=r"$\hat x$", label_offset=(0, -0.2))
    arrow(ax, axis_origin, axis_origin + 0.95 * normal, label=r"$\hat y$", label_offset=(-0.2, 0.05))
    ax.add_patch(Arc(ramp_start, 1.1, 1.1, theta1=0, theta2=np.degrees(angle), lw=1.1))
    ax.text(1.0, 0.58, r"$\theta$", fontsize=13)
    ax.set(xlim=(-0.1, 6.2), ylim=(-1.05, 3.55), aspect="equal")
    ax.axis("off")
    save(fig, "week1/box_fbd.png")


def falling_object_drag():
    fig, ax = plt.subplots(figsize=(4.2, 4.2))
    ball = np.array([0.0, 1.8])
    ax.add_patch(Circle(ball, 0.32, facecolor="#55a7d9", edgecolor=BLACK, lw=1.2))
    arrow(ax, ball + np.array([0, 0.34]), ball + np.array([0, 1.45]), color=RED, label=r"$F_{\rm air}$", label_offset=(0.6, 0))
    arrow(ax, ball - np.array([0, 0.34]), ball - np.array([0, 1.45]), color=BLACK, label=r"$W=m g$", label_offset=(-0.56, 0))
    arrow(ax, (1.25, 2.75), (1.25, 0.25), label=r"$+y$", label_offset=(0.35, 0))
    ax.text(0, 2.35, r"$m$", fontsize=14, ha="center")
    ax.text(0, -0.18, "free-body diagram", fontsize=12, ha="center")
    ax.set(xlim=(-1.7, 2.0), ylim=(-0.5, 3.25), aspect="equal")
    ax.axis("off")
    save(fig, "week1/falling_object.png")


def modeling_framework():
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    boxes = {
        "Observations": (0.2, 2.7, "#e9e9e9"),
        "Physics framework": (2.65, 2.7, "#d7eafa"),
        "Model": (5.1, 2.7, "#f8d2cf"),
        "Analysis": (5.1, 1.0, "#f9e4bd"),
        "Predictions": (2.65, 1.0, "#d9eed5"),
    }
    for label, (x, y, color) in boxes.items():
        ax.add_patch(Rectangle((x, y), 1.85, 0.72, facecolor=color, edgecolor=BLACK, lw=1.1))
        ax.text(x + 0.925, y + 0.36, label, fontsize=12, ha="center", va="center", wrap=True)
    arrow(ax, (2.05, 3.06), (2.62, 3.06))
    arrow(ax, (4.5, 3.06), (5.07, 3.06))
    arrow(ax, (6.03, 2.68), (6.03, 1.75))
    arrow(ax, (5.07, 1.36), (4.5, 1.36))
    arrow(ax, (2.65, 1.36), (2.05, 2.72), connectionstyle="arc3,rad=0.28")
    ax.text(3.62, 3.58, "assumptions and idealizations", color=BLUE, fontsize=11, ha="center")
    ax.text(6.28, 2.1, "equations of motion", color="#b0581b", fontsize=11, rotation=90, va="center")
    ax.text(3.65, 0.52, "compare with observations", color="#3b8a3e", fontsize=11, ha="center")
    ax.set(xlim=(0, 7.2), ylim=(0.15, 4.0))
    ax.axis("off")
    save(fig, "week3/physics-modeling-framework.png")


def falling_ball_air_resistance():
    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    ball = np.array([0.0, 1.75])
    ax.add_patch(Circle(ball, 0.27, facecolor=RED, edgecolor=BLACK, lw=1.1))
    arrow(ax, ball + np.array([0, 0.3]), ball + np.array([0, 1.15]), color=BLUE, label=r"$\vec F_{\rm air}=-b\vec v$", label_offset=(0.78, 0))
    arrow(ax, ball - np.array([0, 0.3]), ball - np.array([0, 1.15]), label=r"$\vec W=m\vec g$", label_offset=(-0.7, 0))
    arrow(ax, (1.45, 2.7), (1.45, 0.35), label=r"$+y$", label_offset=(0.32, 0))
    ax.text(0.45, 2.0, r"$v$", color=BLUE, fontsize=14)
    ax.set(xlim=(-1.75, 2.05), ylim=(-0.1, 3.1), aspect="equal")
    ax.axis("off")
    save(fig, "week3/1d-ball-fbd-air.png")


def orbit_vector_question():
    fig, ax = plt.subplots(figsize=(5.6, 4.0))
    ax.set_aspect("equal")
    theta = np.linspace(0, 2 * np.pi, 300)
    ax.plot(2.4 * np.cos(theta), 1.35 * np.sin(theta), color="0.55", lw=1.1, ls="--")
    ax.add_patch(Circle((0, 0), 0.24, color="#f5b642"))
    earth = np.array([1.75, 0.9])
    ax.add_patch(Circle(earth, 0.13, color=BLUE))
    arrow(ax, (0, 0), earth, color=RED, label=r"$\vec r$", label_offset=(0, 0.2))
    arrow(ax, earth, (0.55, 0.28), color=RED, label=r"$\vec F_{\rm grav}$", label_offset=(-0.1, -0.25))
    ax.text(-0.35, -0.35, "Sun", fontsize=12)
    ax.text(*(earth + np.array([0.15, 0.15])), "Earth", fontsize=12)
    ax.set(xlim=(-2.8, 2.8), ylim=(-1.8, 1.8))
    ax.axis("off")
    save(fig, "week4/gravitational-orbit-vector-question.png")


def relative_position_vector():
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.set_aspect("equal")
    sun, earth = np.array([-1.15, -0.45]), np.array([2.0, 1.1])
    ax.add_patch(Circle(sun, 0.22, color="#f5b642"))
    ax.add_patch(Circle(earth, 0.13, color=BLUE))
    arrow(ax, (0, 0), sun, color="#b0581b", label=r"$\vec r_{\rm sun}$", label_offset=(-0.1, -0.28))
    arrow(ax, (0, 0), earth, color=BLUE, label=r"$\vec r_{\rm earth}$", label_offset=(0.2, 0.2))
    arrow(ax, sun, earth, color=RED, label=r"$\vec r=\vec r_{\rm earth}-\vec r_{\rm sun}$", label_offset=(0, 0.28))
    ax.plot(0, 0, "ko", ms=3)
    ax.text(*(sun + np.array([-0.15, -0.38])), "Sun", fontsize=12)
    ax.text(*(earth + np.array([0.1, 0.16])), "Earth", fontsize=12)
    ax.set(xlim=(-2.1, 2.9), ylim=(-1.35, 2.05))
    ax.axis("off")
    save(fig, "week4/earth-sun-relative-position-vector.png")


def orbit_polar_coordinates():
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    ax.set_aspect("equal")
    arrow(ax, (0, 0), (3.9, 0), label=r"$x$", label_offset=(0.03, -0.28))
    arrow(ax, (0, 0), (0, 3.3), label=r"$y$", label_offset=(-0.28, 0.03))
    earth = np.array([2.85, 1.8])
    ax.add_patch(Circle((0, 0), 0.23, color="#f5b642"))
    ax.add_patch(Circle(earth, 0.13, color=BLUE))
    arrow(ax, (0, 0), earth, color=RED, label=r"$\vec r$", label_offset=(-0.12, 0.18))
    arrow(ax, earth, earth - 0.9 * earth / np.linalg.norm(earth), color=RED, label=r"$\vec F_{\rm grav}$", label_offset=(0.55, 0.05))
    phi = np.degrees(np.arctan2(earth[1], earth[0]))
    ax.add_patch(Arc((0, 0), 1.35, 1.35, theta1=0, theta2=phi, lw=1.1))
    ax.text(0.9, 0.32, r"$\phi$", fontsize=14)
    ax.text(-0.3, -0.4, "Sun", fontsize=12)
    ax.text(*(earth + np.array([0.12, 0.14])), "Earth", fontsize=12)
    ax.set(xlim=(-0.65, 4.3), ylim=(-0.6, 3.7))
    ax.axis("off")
    save(fig, "week4/earth-sun-polar-coordinates.png")


def skateboard_free_body():
    fig, ax = plt.subplots(figsize=(4.6, 4.5))
    theta = np.linspace(np.deg2rad(-75), np.deg2rad(15), 200)
    radius = 3.1
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=BLACK, lw=2)
    angle = np.deg2rad(-40)
    point = radius * np.array([np.cos(angle), np.sin(angle)])
    ax.add_patch(Circle(point, 0.19, facecolor=RED, edgecolor=BLACK, lw=1))
    radial = point / np.linalg.norm(point)
    arrow(ax, point, point - 1.1 * radial, color="#3b8a3e", label=r"$\vec F_{\rm ramp}$", label_offset=(-0.35, 0.1))
    arrow(ax, point, point + np.array([0, -1.1]), label=r"$m\vec g$", label_offset=(0.38, -0.02))
    arrow(ax, (0, 0), point, color=RED, label=r"$\vec r$", label_offset=(-0.15, 0.18))
    ax.add_patch(Arc((0, 0), 1.2, 1.2, theta1=-40, theta2=0, lw=1.1))
    ax.text(0.72, -0.28, r"$\phi$", fontsize=14)
    ax.set(xlim=(-0.55, 3.5), ylim=(-3.25, 0.8), aspect="equal")
    ax.axis("off")
    save(fig, "week12/skateboard-free-body.png")


def parabolic_bowl():
    fig = plt.figure(figsize=(5.6, 4.7))
    ax = fig.add_subplot(projection="3d")
    rho = np.linspace(0, 2.0, 60)
    phi = np.linspace(0, 2 * np.pi, 80)
    rho, phi = np.meshgrid(rho, phi)
    x, y = rho * np.cos(phi), rho * np.sin(phi)
    z = 0.34 * rho**2
    ax.plot_wireframe(x, y, z, rstride=4, cstride=4, color=BLUE, linewidth=0.65)
    bead = np.array([1.15, 0.65, 0.34 * (1.15**2 + 0.65**2)])
    ax.scatter(*bead, color=RED, s=45, depthshade=False)
    ax.quiver(0, 0, 0, 2.25, 0, 0, color=BLACK, arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, 0, 2.25, 0, color=BLACK, arrow_length_ratio=0.08)
    ax.quiver(0, 0, 0, 0, 0, 1.75, color=BLACK, arrow_length_ratio=0.08)
    ax.plot([0, bead[0]], [0, bead[1]], [0, 0], "--", color="0.35", lw=1)
    ax.text(2.35, 0, 0, r"$x$", fontsize=13)
    ax.text(0, 2.35, 0, r"$y$", fontsize=13)
    ax.text(0, 0, 1.85, r"$z$", fontsize=13)
    ax.text(*(bead + np.array([0.12, 0.08, 0.1])), r"$m$", fontsize=13)
    ax.set(xlim=(-2.1, 2.1), ylim=(-2.1, 2.1), zlim=(0, 1.8))
    ax.set_axis_off()
    ax.view_init(elev=27, azim=-52)
    fig.tight_layout()
    save(fig, "week13/paraboloid.png")


if __name__ == "__main__":
    vector_components()
    dot_product()
    falling_ball()
    simple_harmonic_oscillator()
    drag_coordinate_system()
    drag_free_body_diagram()
    discrete_force_intervals()
    path_integral_work()
    lattice_chain()
    closed_path_work()
    driven_oscillator()
    resonance_curve()
    complex_conjugates()
    snells_law()
    brachistochrone()
    polar_coordinate_system()
    plane_pendulum()
    atwood_machine()
    unraveled_string()
    inclined_ramp_free_body()
    falling_object_drag()
    modeling_framework()
    falling_ball_air_resistance()
    orbit_vector_question()
    relative_position_vector()
    orbit_polar_coordinates()
    skateboard_free_body()
    parabolic_bowl()
