"""
Interactive Engineering Calculator
===================================
A multi-tool Streamlit app covering:
  1. Unit Converter
  2. Stress & Strain Calculator
  3. Beam Deflection Calculator
  4. Ideal Gas Law Calculator
  5. Thermodynamic Phase Identifier

Run with:
    streamlit run engineering_calculator_app.py

Dependencies (see requirements.txt):
    streamlit, numpy, matplotlib
"""

import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Engineering Calculator", page_icon="⚙️", layout="wide")

R_GAS = 8.314  # J/(mol*K)  -- also equals kPa*L/(mol*K), which is convenient below

# ----------------------------------------------------------------------------
# ============================  UNIT CONVERTER  ==============================
# ----------------------------------------------------------------------------
UNIT_TABLES = {
    "Length": {
        "millimeter (mm)": 0.001, "centimeter (cm)": 0.01, "meter (m)": 1.0,
        "kilometer (km)": 1000.0, "inch (in)": 0.0254, "foot (ft)": 0.3048,
        "yard (yd)": 0.9144, "mile (mi)": 1609.344,
    },
    "Mass": {
        "gram (g)": 0.001, "kilogram (kg)": 1.0, "metric ton (t)": 1000.0,
        "pound (lb)": 0.45359237, "ounce (oz)": 0.0283495, "slug": 14.59390,
    },
    "Force": {
        "newton (N)": 1.0, "kilonewton (kN)": 1000.0, "pound-force (lbf)": 4.4482216,
        "kilogram-force (kgf)": 9.80665, "dyne": 1e-5,
    },
    "Pressure / Stress": {
        "pascal (Pa)": 1.0, "kilopascal (kPa)": 1e3, "megapascal (MPa)": 1e6,
        "gigapascal (GPa)": 1e9, "bar": 1e5, "atmosphere (atm)": 101325.0,
        "psi": 6894.757, "mmHg": 133.322,
    },
    "Energy": {
        "joule (J)": 1.0, "kilojoule (kJ)": 1e3, "calorie (cal)": 4.184,
        "kilocalorie (kcal)": 4184.0, "watt-hour (Wh)": 3600.0,
        "kilowatt-hour (kWh)": 3.6e6, "BTU": 1055.06, "foot-pound (ft*lb)": 1.35582,
    },
    "Power": {
        "watt (W)": 1.0, "kilowatt (kW)": 1e3, "horsepower (hp)": 745.7,
        "BTU/hour": 0.293071,
    },
    "Volume": {
        "cubic meter (m3)": 1.0, "liter (L)": 0.001, "milliliter (mL)": 1e-6,
        "cubic foot (ft3)": 0.0283168, "cubic inch (in3)": 1.6387e-5,
        "US gallon (gal)": 0.00378541,
    },
    "Area": {
        "square meter (m2)": 1.0, "square centimeter (cm2)": 1e-4,
        "square millimeter (mm2)": 1e-6, "square foot (ft2)": 0.0929030,
        "square inch (in2)": 0.00064516, "acre": 4046.86,
    },
    "Velocity": {
        "meter/second (m/s)": 1.0, "kilometer/hour (km/h)": 0.277778,
        "mile/hour (mph)": 0.44704, "foot/second (ft/s)": 0.3048,
        "knot": 0.514444,
    },
    "Angle": {
        "radian (rad)": 1.0, "degree (deg)": np.pi / 180.0,
    },
}


def temp_to_kelvin(value, unit):
    if unit == "Celsius (°C)":
        return value + 273.15
    if unit == "Fahrenheit (°F)":
        return (value - 32.0) * 5.0 / 9.0 + 273.15
    if unit == "Rankine (°R)":
        return value * 5.0 / 9.0
    return value  # Kelvin


def kelvin_to_temp(k, unit):
    if unit == "Celsius (°C)":
        return k - 273.15
    if unit == "Fahrenheit (°F)":
        return (k - 273.15) * 9.0 / 5.0 + 32.0
    if unit == "Rankine (°R)":
        return k * 9.0 / 5.0
    return k  # Kelvin


def unit_converter_tab():
    st.header("🔄 Unit Converter")
    st.write("Convert between common engineering units, grouped by physical quantity.")

    categories = list(UNIT_TABLES.keys()) + ["Temperature"]
    category = st.selectbox("Quantity type", categories)

    col1, col2, col3 = st.columns(3)

    if category == "Temperature":
        temp_units = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)", "Rankine (°R)"]
        with col1:
            value = st.number_input("Value to convert", value=25.0, format="%.6g")
        with col2:
            from_u = st.selectbox("From", temp_units, index=0)
        with col3:
            to_u = st.selectbox("To", temp_units, index=2)

        k = temp_to_kelvin(value, from_u)
        if k < 0:
            st.error("⚠️ That value is below absolute zero (0 K). Physically impossible — please check your input.")
        else:
            result = kelvin_to_temp(k, to_u)
            st.success(f"**{value:g} {from_u} = {result:,.6g} {to_u}**")

            # Graph: conversion function over a sensible range
            xs = np.linspace(value - 100, value + 100, 200)
            ys = [kelvin_to_temp(temp_to_kelvin(x, from_u), to_u) for x in xs]
            fig, ax = plt.subplots(figsize=(6, 3.2))
            ax.plot(xs, ys, color="#1f77b4")
            ax.scatter([value], [result], color="red", zorder=5, label="Your value")
            ax.set_xlabel(from_u)
            ax.set_ylabel(to_u)
            ax.set_title("How the input affects the converted result")
            ax.grid(alpha=0.3)
            ax.legend()
            st.pyplot(fig)
    else:
        table = UNIT_TABLES[category]
        units = list(table.keys())
        with col1:
            value = st.number_input("Value to convert", value=1.0, format="%.6g")
        with col2:
            from_u = st.selectbox("From", units, index=0)
        with col3:
            to_u = st.selectbox("To", units, index=1 if len(units) > 1 else 0)

        result = value * table[from_u] / table[to_u]
        st.success(f"**{value:g} {from_u} = {result:,.6g} {to_u}**")

        xs = np.linspace(0, max(value * 2, 1), 200)
        ys = xs * table[from_u] / table[to_u]
        fig, ax = plt.subplots(figsize=(6, 3.2))
        ax.plot(xs, ys, color="#1f77b4")
        ax.scatter([value], [result], color="red", zorder=5, label="Your value")
        ax.set_xlabel(from_u)
        ax.set_ylabel(to_u)
        ax.set_title("Conversion is linear: output scales directly with input")
        ax.grid(alpha=0.3)
        ax.legend()
        st.pyplot(fig)

    with st.expander("📘 How this works"):
        st.markdown(
            r"""
Every unit within a quantity type is converted through a common **base (SI) unit**:

$$
\text{result} = \text{value} \times \frac{f_{\text{from}}}{f_{\text{to}}}
$$

where $$f_{\text{from}}$$ and $$f_{\text{to}}$$ are the factors that turn each unit into the base
SI unit (e.g. meters for length, pascals for pressure). Temperature is the one exception because
its scales have different **zero points**, not just different step sizes, so it is converted to
Kelvin first and then to the target scale using:

$$
K = C + 273.15 \qquad K = (F-32)\cdot\frac{5}{9} + 273.15 \qquad K = R \cdot \frac{5}{9}
$$
"""
        )


# ----------------------------------------------------------------------------
# =====================  STRESS & STRAIN CALCULATOR  ==========================
# ----------------------------------------------------------------------------
MATERIAL_PRESETS = {
    "Steel (structural)": 200.0,
    "Aluminum": 69.0,
    "Copper": 110.0,
    "Titanium": 116.0,
    "Concrete": 30.0,
    "Wood (pine, along grain)": 11.0,
    "Custom": None,
}


def stress_strain_tab():
    st.header("📏 Stress & Strain Calculator")
    st.write("Axial loading of a prismatic member (Hooke's Law region).")

    c1, c2 = st.columns(2)
    with c1:
        P_kN = st.number_input("Axial force, P (kN)", value=50.0, step=1.0)
        A_mm2 = st.number_input("Cross-sectional area, A (mm²)", value=500.0, min_value=0.0, step=1.0)
        L0_mm = st.number_input("Original length, L₀ (mm)", value=1000.0, min_value=0.0, step=1.0)
    with c2:
        material = st.selectbox("Material (auto-fills modulus)", list(MATERIAL_PRESETS.keys()))
        default_E = MATERIAL_PRESETS[material] if MATERIAL_PRESETS[material] else 200.0
        E_GPa = st.number_input("Young's modulus, E (GPa)", value=float(default_E), min_value=0.0, step=1.0)
        yield_MPa = st.number_input("Yield strength (MPa, optional — 0 to skip)", value=250.0, min_value=0.0, step=1.0)

    errors = []
    if A_mm2 <= 0:
        errors.append("Cross-sectional area must be greater than zero.")
    if L0_mm <= 0:
        errors.append("Original length must be greater than zero.")
    if E_GPa <= 0:
        errors.append("Young's modulus must be greater than zero.")

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
    else:
        # Convert to SI
        P_N = P_kN * 1e3
        A_m2 = A_mm2 * 1e-6
        L0_m = L0_mm * 1e-3
        E_Pa = E_GPa * 1e9

        stress_Pa = P_N / A_m2
        stress_MPa = stress_Pa / 1e6
        strain = stress_Pa / E_Pa
        elongation_mm = strain * L0_mm

        r1, r2, r3 = st.columns(3)
        r1.metric("Stress, σ", f"{stress_MPa:,.4g} MPa")
        r2.metric("Strain, ε", f"{strain:,.4e}")
        r3.metric("Elongation, ΔL", f"{elongation_mm:,.4g} mm")

        if yield_MPa > 0:
            if abs(stress_MPa) >= yield_MPa:
                st.error(f"⚠️ Stress ({stress_MPa:,.1f} MPa) meets or exceeds the yield strength "
                          f"({yield_MPa:,.1f} MPa) — the material is expected to yield permanently.")
            else:
                fos = yield_MPa / abs(stress_MPa) if stress_MPa != 0 else float("inf")
                st.info(f"Factor of safety against yielding: **{fos:,.2f}**")

        # Graph: stress-strain line up to yield (or 1.5x current strain if no yield given)
        max_strain = (yield_MPa / E_GPa / 1000) if yield_MPa > 0 else abs(strain) * 1.5
        max_strain = max(max_strain, abs(strain) * 1.2, 1e-6)
        eps = np.linspace(0, max_strain, 200)
        sig = eps * E_GPa * 1000  # MPa
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(eps, sig, color="#1f77b4", label=f"Elastic line (E = {E_GPa:g} GPa)")
        ax.scatter([abs(strain)], [abs(stress_MPa)], color="red", zorder=5, label="Operating point")
        if yield_MPa > 0:
            ax.axhline(yield_MPa, color="orange", linestyle="--", label=f"Yield strength ({yield_MPa:g} MPa)")
        ax.set_xlabel("Strain, ε")
        ax.set_ylabel("Stress, σ (MPa)")
        ax.set_title("How strain relates to stress (Hooke's Law)")
        ax.grid(alpha=0.3)
        ax.legend()
        st.pyplot(fig)

    with st.expander("📘 Equations used"):
        st.markdown(
            r"""
**Normal stress** — average force per unit area on the cross-section:

$$
\sigma = \frac{P}{A}
$$

**Hooke's Law** (valid in the linear-elastic region only) relates stress to strain through the
material's Young's modulus $$E$$:

$$
\sigma = E\,\varepsilon \quad\Longrightarrow\quad \varepsilon = \frac{\sigma}{E}
$$

**Elongation** follows directly from the definition of strain, $$\varepsilon = \Delta L / L_0$$:

$$
\Delta L = \varepsilon\, L_0 = \frac{P L_0}{A E}
$$

**Factor of safety** compares the material's yield strength to the actual working stress:

$$
\text{FOS} = \frac{\sigma_{\text{yield}}}{\sigma}
$$

A factor of safety below 1 means the part is predicted to yield.
"""
        )


# ----------------------------------------------------------------------------
# ======================  BEAM DEFLECTION CALCULATOR  =========================
# ----------------------------------------------------------------------------
BEAM_CASES = [
    "Simply supported — center point load",
    "Simply supported — uniformly distributed load",
    "Cantilever — point load at free end",
    "Cantilever — uniformly distributed load",
]


def deflection_curve(case, x, L, P, w, E, I):
    """Returns deflection y(x) in meters (downward positive). x is a numpy array."""
    if case == BEAM_CASES[0]:  # simply supported, center point load P
        y = np.where(
            x <= L / 2,
            P * x * (3 * L ** 2 - 4 * x ** 2) / (48 * E * I),
            P * (L - x) * (3 * L ** 2 - 4 * (L - x) ** 2) / (48 * E * I),
        )
    elif case == BEAM_CASES[1]:  # simply supported, UDL w
        y = w * x * (L ** 3 - 2 * L * x ** 2 + x ** 3) / (24 * E * I)
    elif case == BEAM_CASES[2]:  # cantilever, end point load P (fixed at x=0)
        y = P * x ** 2 * (3 * L - x) / (6 * E * I)
    else:  # cantilever, UDL w
        y = w * x ** 2 * (6 * L ** 2 - 4 * L * x + x ** 2) / (24 * E * I)
    return y


def beam_deflection_tab():
    st.header("🏗️ Beam Deflection Calculator")
    st.write("Elastic deflection of a beam with a constant cross-section (small-deflection theory).")

    case = st.selectbox("Beam & loading case", BEAM_CASES)
    is_point_load = "point load" in case

    c1, c2 = st.columns(2)
    with c1:
        L_m = st.number_input("Beam length, L (m)", value=3.0, min_value=0.0, step=0.1)
        E_GPa = st.number_input("Elastic modulus, E (GPa)", value=200.0, min_value=0.0, step=1.0)
        if is_point_load:
            P_kN = st.number_input("Point load, P (kN)", value=10.0, step=1.0)
            w_kNm = 0.0
        else:
            w_kNm = st.number_input("Distributed load, w (kN/m)", value=5.0, step=1.0)
            P_kN = 0.0
    with c2:
        use_rect = st.checkbox("Compute I from a rectangular cross-section instead", value=False)
        if use_rect:
            b_mm = st.number_input("Width, b (mm)", value=100.0, min_value=0.0, step=1.0)
            h_mm = st.number_input("Height, h (mm)", value=200.0, min_value=0.0, step=1.0)
            I_mm4 = (b_mm * h_mm ** 3) / 12.0 if (b_mm > 0 and h_mm > 0) else 0.0
            st.caption(f"Computed I = b·h³/12 = {I_mm4:,.4g} mm⁴")
        else:
            I_mm4 = st.number_input("Moment of inertia, I (mm⁴)", value=8.333e6, min_value=0.0, format="%.6g")

    errors = []
    if L_m <= 0:
        errors.append("Beam length must be greater than zero.")
    if E_GPa <= 0:
        errors.append("Elastic modulus must be greater than zero.")
    if I_mm4 <= 0:
        errors.append("Moment of inertia must be greater than zero.")

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
    else:
        E_Pa = E_GPa * 1e9
        I_m4 = I_mm4 * 1e-12
        P_N = P_kN * 1e3
        w_Nm = w_kNm * 1e3

        x = np.linspace(0, L_m, 300)
        y_m = deflection_curve(case, x, L_m, P_N, w_Nm, E_Pa, I_m4)
        y_mm = y_m * 1e3
        max_defl_mm = np.max(np.abs(y_mm))

        st.metric("Maximum deflection", f"{max_defl_mm:,.4g} mm")

        span_ratio = L_m * 1000 / max_defl_mm if max_defl_mm > 0 else float("inf")
        if span_ratio < 250:
            st.warning(f"⚠️ Deflection is large relative to span (L/{span_ratio:,.0f}). "
                       f"Many design codes require at least L/250–L/360 for serviceability — check your load/section.")

        fig, ax = plt.subplots(figsize=(7, 3.5))
        ax.plot(x, -y_mm, color="#1f77b4", linewidth=2)
        ax.axhline(0, color="gray", linewidth=1)
        ax.fill_between(x, -y_mm, 0, alpha=0.15, color="#1f77b4")
        ax.set_xlabel("Position along beam, x (m)")
        ax.set_ylabel("Deflection (mm, downward = negative)")
        ax.set_title(f"Deflection shape — {case}")
        ax.grid(alpha=0.3)
        st.pyplot(fig)

    with st.expander("📘 Equations used"):
        st.markdown(
            r"""
All cases assume linear-elastic material behavior and small deflections (Euler–Bernoulli beam
theory), with $$E$$ = modulus of elasticity and $$I$$ = second moment of area of the cross-section.

**Simply supported, center point load P:**

$$
y(x) = \frac{Px(3L^2-4x^2)}{48EI}\ \ (0 \le x \le L/2), \qquad
\delta_{max} = \frac{PL^3}{48EI}\ \text{at } x = L/2
$$

**Simply supported, uniformly distributed load w (force/length):**

$$
y(x) = \frac{wx(L^3 - 2Lx^2 + x^3)}{24EI}, \qquad
\delta_{max} = \frac{5wL^4}{384EI}\ \text{at } x = L/2
$$

**Cantilever, point load P at the free end:**

$$
y(x) = \frac{Px^2(3L-x)}{6EI}, \qquad \delta_{max} = \frac{PL^3}{3EI}\ \text{at } x = L
$$

**Cantilever, uniformly distributed load w:**

$$
y(x) = \frac{wx^2(6L^2-4Lx+x^2)}{24EI}, \qquad \delta_{max} = \frac{wL^4}{8EI}\ \text{at } x = L
$$

**Rectangular section moment of inertia:**

$$
I = \frac{bh^3}{12}
$$
"""
        )


# ----------------------------------------------------------------------------
# =======================  IDEAL GAS LAW CALCULATOR  ===========================
# ----------------------------------------------------------------------------
def ideal_gas_tab():
    st.header("💨 Ideal Gas Law Calculator")
    st.write("Solve $$PV = nRT$$ for any one variable given the other three.")

    solve_for = st.radio("Solve for:", ["Pressure (P)", "Volume (V)", "Temperature (T)", "Moles (n)"], horizontal=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        P_kPa = st.number_input("Pressure, P (kPa)", value=101.325, min_value=0.0,
                                 disabled=(solve_for == "Pressure (P)"))
    with c2:
        V_L = st.number_input("Volume, V (L)", value=10.0, min_value=0.0,
                               disabled=(solve_for == "Volume (V)"))
    with c3:
        T_unit = st.selectbox("Temp. unit", ["Kelvin (K)", "Celsius (°C)"])
        T_input = st.number_input(f"Temperature ({T_unit})", value=25.0 if T_unit == "Celsius (°C)" else 298.15,
                                   disabled=(solve_for == "Temperature (T)"))
    with c4:
        n_mol = st.number_input("Moles, n (mol)", value=1.0, min_value=0.0,
                                 disabled=(solve_for == "Moles (n)"))

    T_K = T_input + 273.15 if T_unit == "Celsius (°C)" else T_input

    errors = []
    if solve_for != "Temperature (T)" and T_K <= 0:
        errors.append("Temperature must be above absolute zero (0 K).")
    if solve_for != "Pressure (P)" and P_kPa < 0:
        errors.append("Pressure cannot be negative.")
    if solve_for != "Volume (V)" and V_L < 0:
        errors.append("Volume cannot be negative.")
    if solve_for != "Moles (n)" and n_mol < 0:
        errors.append("Moles cannot be negative.")

    if errors:
        for e in errors:
            st.error(f"⚠️ {e}")
    else:
        # R in kPa*L/(mol*K) equals 8.314 (since 1 kPa*L = 1 J)
        R = R_GAS
        if solve_for == "Pressure (P)":
            if n_mol == 0 or V_L == 0:
                st.error("⚠️ Moles and volume must be greater than zero to solve for pressure.")
                return
            P_kPa = n_mol * R * T_K / V_L
            st.success(f"**P = n·R·T / V = {P_kPa:,.4g} kPa**")
        elif solve_for == "Volume (V)":
            if n_mol == 0 or P_kPa == 0:
                st.error("⚠️ Moles and pressure must be greater than zero to solve for volume.")
                return
            V_L = n_mol * R * T_K / P_kPa
            st.success(f"**V = n·R·T / P = {V_L:,.4g} L**")
        elif solve_for == "Temperature (T)":
            if n_mol == 0:
                st.error("⚠️ Moles must be greater than zero to solve for temperature.")
                return
            T_K = P_kPa * V_L / (n_mol * R)
            st.success(f"**T = P·V / (n·R) = {T_K:,.4g} K  ({T_K - 273.15:,.4g} °C)**")
        else:
            if T_K == 0:
                st.error("⚠️ Temperature must be greater than zero to solve for moles.")
                return
            n_mol = P_kPa * V_L / (R * T_K)
            st.success(f"**n = P·V / (R·T) = {n_mol:,.4g} mol**")

        # Isotherm graph: P vs V at this T, n (Boyle's Law)
        V_range = np.linspace(max(V_L * 0.2, 0.01), V_L * 3 if V_L > 0 else 20, 200)
        P_range = n_mol * R * T_K / V_range
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.plot(V_range, P_range, color="#1f77b4", label=f"Isotherm at T = {T_K:,.1f} K")
        ax.scatter([V_L], [P_kPa], color="red", zorder=5, label="Current state")
        ax.set_xlabel("Volume, V (L)")
        ax.set_ylabel("Pressure, P (kPa)")
        ax.set_title("Boyle's Law: how volume trades off against pressure")
        ax.grid(alpha=0.3)
        ax.legend()
        st.pyplot(fig)

    with st.expander("📘 Equation used"):
        st.markdown(
            r"""
The **ideal gas law** relates pressure, volume, moles, and absolute temperature:

$$
PV = nRT
$$

where $$R = 8.314\ \text{J}/(\text{mol}\cdot\text{K})$$ is the universal gas constant (numerically
identical to $$8.314\ \text{kPa}\cdot\text{L}/(\text{mol}\cdot\text{K})$$, which is why this
calculator works directly in kPa and L). The model assumes point-like molecules with no
intermolecular forces — a good approximation for real gases at low pressure and moderate-to-high
temperature, but it breaks down near a gas's condensation point.
"""
        )


# ----------------------------------------------------------------------------
# =====================  THERMODYNAMIC PHASE IDENTIFIER  ======================
# ----------------------------------------------------------------------------
SUBSTANCES = {
    "Water (H2O)": {"Tt": 273.16, "Pt": 0.6117, "Tc": 647.10, "Pc": 22064.0, "Lv": 40650.0, "Ls": 51070.0},
    "Carbon Dioxide (CO2)": {"Tt": 216.58, "Pt": 517.0, "Tc": 304.13, "Pc": 7377.3, "Lv": 16850.0, "Ls": 25230.0},
    "Nitrogen (N2)": {"Tt": 63.15, "Pt": 12.5, "Tc": 126.19, "Pc": 3395.8, "Lv": 5570.0, "Ls": 6540.0},
    "Ammonia (NH3)": {"Tt": 195.40, "Pt": 6.09, "Tc": 405.40, "Pc": 11333.0, "Lv": 23350.0, "Ls": 30800.0},
}


def sat_pressure(T, Tt, Pt, L):
    """Clausius-Clapeyron estimate of saturation pressure (kPa) at temperature T (K)."""
    return Pt * np.exp(-(L / R_GAS) * (1.0 / T - 1.0 / Tt))


def identify_phase(T, P, props):
    Tt, Pt, Tc, Pc, Lv, Ls = props["Tt"], props["Pt"], props["Tc"], props["Pc"], props["Lv"], props["Ls"]
    if T > Tc and P > Pc:
        return "Supercritical fluid"
    if T > Tc:
        return "Gas (above critical temperature)"
    if T < Tt:
        p_sub = sat_pressure(T, Tt, Pt, Ls)
        return "Solid" if P > p_sub else "Vapor (gas)"
    p_sat = sat_pressure(T, Tt, Pt, Lv)
    return "Liquid" if P > p_sat else "Vapor (gas)"


def phase_identifier_tab():
    st.header("🌡️ Thermodynamic Phase Identifier")
    st.write("Estimates whether a substance is solid, liquid, vapor, or supercritical at a given "
             "temperature and pressure, using the Clausius–Clapeyron relation anchored at the triple point.")

    substance_name = st.selectbox("Substance", list(SUBSTANCES.keys()))
    props = SUBSTANCES[substance_name]

    c1, c2 = st.columns(2)
    with c1:
        T_unit = st.selectbox("Temperature unit", ["Kelvin (K)", "Celsius (°C)"], key="phase_T_unit")
        default_T = 298.15 if T_unit == "Kelvin (K)" else 25.0
        T_in = st.number_input(f"Temperature ({T_unit})", value=default_T)
    with c2:
        P_kPa = st.number_input("Pressure (kPa)", value=101.325, min_value=0.0)

    T_K = T_in + 273.15 if T_unit == "Celsius (°C)" else T_in

    if T_K <= 0:
        st.error("⚠️ Temperature must be above absolute zero (0 K).")
        return
    if P_kPa < 0:
        st.error("⚠️ Pressure cannot be negative.")
        return

    phase = identify_phase(T_K, P_kPa, props)
    st.success(f"**Predicted phase: {phase}**")

    st.caption(
        f"{substance_name} — triple point: {props['Tt']:.2f} K / {props['Pt']:.3g} kPa · "
        f"critical point: {props['Tc']:.2f} K / {props['Pc']:.0f} kPa"
    )

    # --- Phase diagram graph ---
    Tt, Pt, Tc, Pc, Lv, Ls = props["Tt"], props["Pt"], props["Tc"], props["Pc"], props["Lv"], props["Ls"]
    T_sub = np.linspace(max(Tt * 0.5, 1.0), Tt, 150)
    P_sub = sat_pressure(T_sub, Tt, Pt, Ls)
    T_vap = np.linspace(Tt, Tc, 150)
    P_vap = sat_pressure(T_vap, Tt, Pt, Lv)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(T_sub, P_sub, color="#2ca02c", label="Sublimation curve (solid ↔ vapor)")
    ax.plot(T_vap, P_vap, color="#1f77b4", label="Vaporization curve (liquid ↔ vapor)")
    ax.plot([Tt, Tt], [Pt, Pc * 1.15], color="#d62728", linestyle="--", label="Fusion line (solid ↔ liquid, approx.)")
    ax.scatter([Tt], [Pt], color="black", zorder=5, marker="o")
    ax.annotate("Triple point", (Tt, Pt), textcoords="offset points", xytext=(8, -12), fontsize=8)
    ax.scatter([Tc], [Pc], color="black", zorder=5, marker="s")
    ax.annotate("Critical point", (Tc, Pc), textcoords="offset points", xytext=(-70, 5), fontsize=8)
    ax.scatter([T_K], [P_kPa], color="orange", zorder=6, s=90, edgecolor="black", label="Your state")
    ax.set_yscale("log")
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Pressure (kPa, log scale)")
    ax.set_title(f"P–T Phase Diagram — {substance_name}")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="lower right")
    st.pyplot(fig)

    with st.expander("📘 Method & equations"):
        st.markdown(
            r"""
The boundary between two phases follows the **Clausius–Clapeyron relation**, integrated
approximately (assuming the latent heat $$L$$ is constant and the vapor is ideal) starting from
the known triple point $$(T_t, P_t)$$:

$$
P_{sat}(T) = P_t \exp\!\left[-\frac{L}{R}\left(\frac{1}{T} - \frac{1}{T_t}\right)\right]
$$

- The **vaporization curve** (liquid ↔ vapor boundary, from the triple point up to the critical
  point) uses the molar latent heat of vaporization, $$L_v$$.
- The **sublimation curve** (solid ↔ vapor boundary, below the triple point) uses the molar
  latent heat of sublimation, $$L_s$$.
- The **fusion line** (solid ↔ liquid boundary) is approximated here as vertical at $$T = T_t$$ —
  a reasonable simplification for teaching purposes, since real fusion lines are nearly vertical
  and only weakly pressure-dependent for most substances.

Decision rule for a given $$(T, P)$$:

1. If $$T > T_c$$: **gas**, or **supercritical fluid** if also $$P > P_c$$.
2. If $$T < T_t$$: compare $$P$$ to $$P_{sub}(T)$$ → **solid** if above, **vapor** if below.
3. Otherwise ($$T_t \le T \le T_c$$): compare $$P$$ to $$P_{sat}(T)$$ → **liquid** if above,
   **vapor** if below.

This is a simplified educational model, not a substitute for a full equation of state (e.g. NIST
REFPROP) for engineering design work.
"""
        )


# ----------------------------------------------------------------------------
# ================================  MAIN  ======================================
# ----------------------------------------------------------------------------
def main():
    st.title("⚙️ Interactive Engineering Calculator")
    st.caption(
        "Unit conversion, mechanics of materials, beam deflection, ideal-gas behavior, and "
        "thermodynamic phase prediction — with live graphs and equation explanations."
    )

    with st.sidebar:
        st.header("About")
        st.markdown(
            """
This app bundles five engineering calculators into one interface:

1. **Unit Converter** — length, mass, force, pressure, energy, power, volume, area, velocity,
   angle, and temperature.
2. **Stress & Strain** — axial stress, strain, elongation, and factor of safety.
3. **Beam Deflection** — four standard simply-supported / cantilever load cases.
4. **Ideal Gas Law** — solve $$PV=nRT$$ for any variable.
5. **Phase Identifier** — solid/liquid/vapor/supercritical prediction from a P–T diagram.

Every tab validates its inputs and explains the equations behind its results.
"""
        )
        st.info("Tip: expand the **'Equations used'** section in each tab for the full derivation.")

    tabs = st.tabs([
        "🔄 Unit Converter", "📏 Stress & Strain", "🏗️ Beam Deflection",
        "💨 Ideal Gas Law", "🌡️ Phase Identifier",
    ])

    with tabs[0]:
        unit_converter_tab()
    with tabs[1]:
        stress_strain_tab()
    with tabs[2]:
        beam_deflection_tab()
    with tabs[3]:
        ideal_gas_tab()
    with tabs[4]:
        phase_identifier_tab()


if __name__ == "__main__":
    main()
