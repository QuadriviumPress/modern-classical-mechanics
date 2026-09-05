# Activities

Every unit of the course opens with an activity notebook — a hands-on simulation or thought experiment, worked in Python, that motivates the formal notes that follow. These aren't optional extras; they're where most of the actual modeling happens. Below is the full set, grouped by topic, plus the homework sets that apply them.

## Unit activities

| Unit | Activity | What you'll do |
| --- | --- | --- |
| 1 | [Overture: What is Classical Physics?](notebooks/01_start.md) | Survey where classical mechanics shows up in current research and industry. |
| 2 | [Computing as a tool for science](notebooks/02_start.md) | Use the Euler method to discretize Newton's second law and step a trajectory forward numerically. |
| 3 | [What is Mathematical Modeling?](notebooks/03_start.md) | Build a model of a physical system from assumptions to equations. |
| 4 | [Why does fluid drag complicate things?](notebooks/04_start.md) | Add drag to the equations of motion and see how it changes a trajectory. |
| 5 | [Conservation Laws](notebooks/05_start.md) | Track energy through a simulation and check where it is (and isn't) conserved. |
| 6 | [Stability and Equilibria](notebooks/06_start.md) | Find equilibrium points and test whether small perturbations grow or decay. |
| 7 | [Nonlinear Dynamics](notebooks/07_start.md) | Plot phase portraits for nonlinear first-order ODEs and locate critical points. |
| 8 | [Oscillations](notebooks/08_start.md) | Model a simple oscillator and compare the numerical solution to the analytic one. |
| 9 | [Driven Oscillators and Resonance](notebooks/09_start.md) | Drive an oscillator at different frequencies and find the resonance peak. |
| 10 | [Chaotic Dynamics](notebooks/10_start.md) | Use `scipy.integrate.solve_ivp` to simulate a damped, driven pendulum and look for sensitivity to initial conditions. |
| 11 | [Calculus of Variations](notebooks/11_start.md) | Explore what it means for a path to minimize a functional. |
| 12 | [The Principle of Least Action](notebooks/12_start.md) | Derive equations of motion from stationary action instead of forces. |
| 13 | [Lagrangian Mechanics](notebooks/13_start.md) | Apply the Lagrangian formulation to a system with constraints. |

Each activity has a matching **notes** notebook with the formal derivation — for example, [Unit 10's notes](notebooks/10_notes.md) work through the same damped driven pendulum in more depth.

## Homework

Eight problem sets apply each unit's tools to new systems: [Homework 1](notebooks/hw1.md), [2](notebooks/hw2.md), [3](notebooks/hw3.md), [4](notebooks/hw4.md), [5](notebooks/hw5.md), [6](notebooks/hw6.md), [7](notebooks/hw7.md), and [8](notebooks/hw8.md).

## Adding an activity

Activities live as MyST Markdown notebooks in [`content/notebooks/`](notebooks). To add one:

1. Add a new `.md` file there, following the style of an existing `*_start.md` notebook (a motivating question or system, then Python code cells that simulate or explore it).
2. Register it in the `project.toc` list in [`myst.yml`](../myst.yml) so it appears in the site navigation.
3. Open a pull request on the [GitHub repository](https://github.com/QuadriviumPress/modern-classical-mechanics/pulls).
