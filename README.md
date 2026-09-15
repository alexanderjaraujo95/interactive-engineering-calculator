# Interactive Engineering Calculator

A Streamlit app with five engineering calculators, live graphs, input validation, and equation
explanations for every result.

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run engineering_calculator_app.py
```

This opens the app in your browser (usually at `http://localhost:8501`).

## What's inside

| Tab | What it does |
|---|---|
| Unit Converter | Length, mass, force, pressure/stress, energy, power, volume, area, velocity, angle, temperature |
| Stress & Strain | Axial stress, strain, elongation, factor of safety vs. yield, with a stress-strain plot |
| Beam Deflection | 4 standard beam/load cases (simply supported & cantilever, point & distributed loads), with the deflection curve plotted along the beam |
| Ideal Gas Law | Solves $PV = nRT$ for any one of P, V, T, n, with a Boyle's-law isotherm plot |
| Phase Identifier | Predicts solid/liquid/vapor/supercritical for water, CO₂, nitrogen, or ammonia from a P–T phase diagram (Clausius–Clapeyron estimate) |

Every tab flags invalid inputs (e.g. negative lengths, sub-absolute-zero temperatures, zero
denominators) before running the math, and includes an "Equations used" expander with the full
derivation in LaTeX.
