"""Regenerate the schematic figures used by the homework activities."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, FancyArrowPatch, PathPatch, Rectangle
from matplotlib.path import Path as MplPath


OUT = Path(__file__).resolve().parents[1] / "content/images/activities"


def save(fig, name):
    fig.savefig(OUT / name, dpi=180, bbox_inches="tight", pad_inches=0.08,
                facecolor="white")
    plt.close(fig)


def triangle():
    fig, ax = plt.subplots(figsize=(7, 4.3))
    A, B, C = np.array([0.4, 0.35]), np.array([4.8, 3.65]), np.array([6.5, 0.35])
    ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], color="black", lw=2)
    for point, label, offset in [(A, "A", (-0.18, -0.18)), (B, "B", (-0.02, 0.14)),
                                 (C, "C", (0.08, -0.18))]:
        ax.plot(*point, "ko", ms=5)
        ax.text(*(point + offset), label, fontsize=16, family="serif", fontstyle="italic")
    ax.text(2.35, 2.0, "c", fontsize=16, family="serif", fontstyle="italic")
    ax.text(5.7, 2.0, "a", fontsize=16, family="serif", fontstyle="italic")
    ax.text(3.45, 0.02, "b", fontsize=16, family="serif", fontstyle="italic")
    ax.add_patch(Arc(A, 0.8, 0.8, angle=0, theta1=0, theta2=37, lw=1.2))
    ax.add_patch(Arc(B, 0.9, 0.9, angle=0, theta1=250, theta2=305, lw=1.2))
    ax.add_patch(Arc(C, 0.8, 0.8, angle=0, theta1=143, theta2=180, lw=1.2))
    ax.text(1.05, 0.57, r"$\alpha$", fontsize=14)
    ax.text(4.45, 3.0, r"$\beta$", fontsize=14)
    ax.text(5.72, 0.65, r"$\gamma$", fontsize=14)
    ax.set(xlim=(0, 7), ylim=(0, 4.2), aspect="equal")
    ax.axis("off")
    save(fig, "1.15-triangle.png")


def kid_toy():
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    ax.plot([-1.9, 1.9], [0, 0], color="black", lw=1.2)
    ax.add_patch(Rectangle((-1.25, 1.2), 2.5, 2.6, fill=False, lw=1.5))
    theta = np.linspace(np.pi, 2 * np.pi, 200)
    ax.plot(1.25 * np.cos(theta), 1.2 + 1.2 * np.sin(theta), color="black", lw=1.5)
    ax.plot([0, 0], [0, 1.85], color="black", lw=1.0)
    ax.plot(0, 1.85, "ko", ms=5)
    ax.text(-0.78, 2.05, "CM", fontsize=14, family="serif")
    ax.text(-0.12, 1.35, "O", fontsize=14, family="serif", fontstyle="italic")
    ax.annotate("", xy=(0, 0.08), xytext=(0, 1.28), arrowprops=dict(arrowstyle="->", lw=1))
    ax.text(-0.12, 0.7, "R", fontsize=14, family="serif", fontstyle="italic")
    ax.annotate("", xy=(1.75, 1.85), xytext=(1.75, 0.03), arrowprops=dict(arrowstyle="<->", lw=1))
    ax.text(1.88, 0.9, "h", fontsize=14, family="serif", fontstyle="italic")
    ax.set(xlim=(-2.1, 2.2), ylim=(-0.2, 4.1), aspect="equal")
    ax.axis("off")
    save(fig, "5.2-kid_toy.png")


def curved_path():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    verts = [(0.2, 0.35), (1.7, -0.1), (2.4, 0.0), (2.8, 1.2),
             (3.2, 2.2), (3.7, 2.2), (3.9, 1.0), (4.0, 0.5),
             (4.5, -0.1), (5.8, -0.2), (6.4, 0.2), (6.8, 1.2),
             (7.2, 2.2), (7.7, 2.2), (7.9, 1.0), (8.0, 0.5),
             (8.6, -0.1), (9.5, 0.0), (9.9, 0.15)]
    codes = [MplPath.MOVETO] + [MplPath.CURVE4] * (len(verts) - 1)
    ax.add_patch(PathPatch(MplPath(verts, codes), fill=False, lw=2, color="black"))
    ax.annotate("", xy=(2.55, 0.18), xytext=(1.0, 0.24),
                arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(1.7, 0.42, "s", fontsize=16, family="serif", fontstyle="italic")
    ax.text(0.05, 0.2, "O", fontsize=16, family="serif", fontstyle="italic")
    ax.set(xlim=(-0.1, 10.2), ylim=(-0.4, 2.6), aspect="equal")
    ax.axis("off")
    save(fig, "5.3-curved_path.png")


def apparatus():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    center, radius = np.array([0.0, 0.0]), 2.35
    ax.add_patch(Circle(center, radius, fill=False, lw=1.8))
    angle = np.deg2rad(-38)
    mass = radius * np.array([np.cos(angle), np.sin(angle)])
    ax.plot([0, mass[0]], [0, mass[1]], color="black", lw=1.5)
    ax.plot([0, 0], [0, -2.8], "k--", lw=1)
    ax.plot(0, 0, "ko", ms=6)
    ax.add_patch(Circle(mass, 0.22, facecolor="0.7", edgecolor="black", lw=1))
    ax.plot([-radius, -radius], [0, -2.45], color="black", lw=1.3)
    ax.add_patch(Circle((-radius, -2.62), 0.16, facecolor="0.7", edgecolor="black", lw=1))
    ax.text(0.98, -0.95, "R", fontsize=16, family="serif", fontstyle="italic")
    ax.text(mass[0] + 0.25, mass[1] - 0.05, "M", fontsize=16, family="serif", fontstyle="italic")
    ax.text(-2.85, -2.75, "m", fontsize=16, family="serif", fontstyle="italic")
    ax.annotate("", xy=(0, -0.48), xytext=(0, -1.05),
                arrowprops=dict(arrowstyle="<->", connectionstyle="arc3,rad=0.5", lw=1))
    ax.set(xlim=(-2.9, 2.9), ylim=(-3.0, 2.8), aspect="equal")
    ax.axis("off")
    save(fig, "5.4-apparatus.png")


def paths():
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    O, P, Q = np.array([0.0, 0.0]), np.array([1.0, 1.0]), np.array([1.0, 0.0])
    ax.annotate("", xy=(0, 1.15), xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate("", xy=(1.2, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.plot([0, 1], [0, 1], color="black", lw=2, label="c")
    t = np.linspace(0, 1, 200)
    ax.plot(t, t**2, color="black", lw=2, label="b")
    ax.plot([1, 1], [0, 1], color="black", lw=2, label="a")
    for start, end in [(0.34, 0.43), (0.43, 0.53), (0.7, 0.78)]:
        x = np.array([start, end]); y = x
        ax.add_patch(FancyArrowPatch((x[0], y[0]), (x[1], y[1]), arrowstyle="->", mutation_scale=12, lw=1))
    ax.add_patch(FancyArrowPatch((0.42, 0.42**2), (0.52, 0.52**2), arrowstyle="->", mutation_scale=12, lw=1))
    ax.add_patch(FancyArrowPatch((1, 0.38), (1, 0.52), arrowstyle="->", mutation_scale=12, lw=1))
    ax.text(-0.08, -0.08, "O", fontsize=15, family="serif", fontstyle="italic")
    ax.text(0.98, 1.08, "P", fontsize=15, family="serif", fontstyle="italic")
    ax.text(0.98, -0.08, "Q", fontsize=15, family="serif", fontstyle="italic")
    ax.text(0.34, 0.38, "c", fontsize=15, family="serif", fontstyle="italic")
    ax.text(0.55, 0.24, "b", fontsize=15, family="serif", fontstyle="italic")
    ax.text(1.12, 0.38, "a", fontsize=15, family="serif", fontstyle="italic")
    ax.text(-0.08, 1.25, "y", fontsize=15, family="serif", fontstyle="italic")
    ax.text(1.28, -0.08, "x", fontsize=15, family="serif", fontstyle="italic")
    ax.set(xlim=(-0.15, 1.35), ylim=(-0.15, 1.35), aspect="equal")
    ax.axis("off")
    save(fig, "particle-paths-between-two-points.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    triangle()
    kid_toy()
    curved_path()
    apparatus()
    paths()
