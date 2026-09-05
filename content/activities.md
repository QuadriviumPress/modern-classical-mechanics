# Activities

Every week of the course opens with an activity notebook — a hands-on simulation or thought experiment, worked in Python, that motivates the formal notes that follow. These aren't optional extras; they're where most of the actual modeling happens. Below is the full set, grouped by topic, plus the homework sets that apply them.

## Weekly activities

| Week | Activity | What you'll do |
| --- | --- | --- |
| 1 | [Overture: What is Classical Physics?](notebooks/01_start.ipynb) | Survey where classical mechanics shows up in current research and industry. |
| 2 | [Computing as a tool for science](notebooks/02_start.ipynb) | Use the Euler method to discretize Newton's second law and step a trajectory forward numerically. |
| 3 | [What is Mathematical Modeling?](notebooks/03_start.ipynb) | Build a model of a physical system from assumptions to equations. |
| 4 | [Why does fluid drag complicate things?](notebooks/04_start.ipynb) | Add drag to the equations of motion and see how it changes a trajectory. |
| 5 | [Conservation Laws](notebooks/05_start.ipynb) | Track energy through a simulation and check where it is (and isn't) conserved. |
| 6 | [Stability and Equilibria](notebooks/06_start.ipynb) | Find equilibrium points and test whether small perturbations grow or decay. |
| 7 | [Nonlinear Dynamics](notebooks/07_start.ipynb) | Plot phase portraits for nonlinear first-order ODEs and locate critical points. |
| 8 | [Oscillations](notebooks/08_start.ipynb) | Model a simple oscillator and compare the numerical solution to the analytic one. |
| 9 | [Driven Oscillators and Resonance](notebooks/09_start.ipynb) | Drive an oscillator at different frequencies and find the resonance peak. |
| 10 | [Chaotic Dynamics](notebooks/10_start.ipynb) | Use `scipy.integrate.solve_ivp` to simulate a damped, driven pendulum and look for sensitivity to initial conditions. |
| 11 | [Calculus of Variations](notebooks/11_start.ipynb) | Explore what it means for a path to minimize a functional. |
| 12 | [The Principle of Least Action](notebooks/12_start.ipynb) | Derive equations of motion from stationary action instead of forces. |
| 13 | [Lagrangian Mechanics](notebooks/13_start.ipynb) | Apply the Lagrangian formulation to a system with constraints. |

Each activity has a matching **notes** notebook with the formal derivation — for example, [Week 10's notes](notebooks/10_notes.ipynb) work through the same damped driven pendulum in more depth.

## Homework

Eight problem sets apply each week's tools to new systems: [Homework 1](notebooks/hw1.ipynb), [2](notebooks/hw2.ipynb), [3](notebooks/hw3.ipynb), [4](notebooks/hw4.ipynb), [5](notebooks/hw5.ipynb), [6](notebooks/hw6.ipynb), [7](notebooks/hw7.ipynb), and [8](notebooks/hw8.ipynb).

## Adding an activity

Activities live as Jupyter notebooks in [`content/notebooks/`](notebooks). To add one:

1. Add a new `.ipynb` file there, following the style of an existing `*_start.ipynb` notebook (a motivating question or system, then Python code that simulates or explores it).
2. Register it in the `project.toc` list in [`myst.yml`](../myst.yml) so it appears in the site navigation.
3. Open a pull request — see [About](about.md) for how contributions work.
