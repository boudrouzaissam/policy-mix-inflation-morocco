import streamlit as st
import pandas as pd
from pathlib import Path
from PIL import Image

# =========================
# Page configuration
# =========================
st.set_page_config(
    page_title="Policy Mix and Inflation in Morocco",
    page_icon="📊",
    layout="wide"
)

# =========================
# Paths
# =========================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = BASE_DIR / "figures"

# =========================
# Header
# =========================
st.title("Policy Mix and Inflation Dynamics in Morocco")
st.caption("Empirical analysis using Local Projections | Morocco, 1967–2000")

st.markdown("""
This dashboard presents the empirical results of a research project on the dynamic relationship
between monetary-fiscal policy mix and inflation in Morocco.

The analysis focuses on whether the interaction between monetary and fiscal policy becomes
inflationary during historically active policy-mix episodes. The empirical strategy relies on
Local Projections estimated over the period 1967–2000.
""")

# =========================
# Sidebar
# =========================
st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Choose a section",
    [
        "Overview",
        "Data",
        "Baseline Results",
        "Robustness",
        "Figures",
        "Quarterly Extension"
    ]
)

# =========================
# Helper functions
# =========================
def load_excel(path):
    try:
        return pd.read_excel(path)
    except Exception as e:
        st.warning(f"Could not load file: {path.name}")
        st.error(e)
        return None

def show_image(filename, caption=None):
    path = FIGURES_DIR / filename
    if path.exists():
        image = Image.open(path)
        st.image(image, caption=caption, use_container_width=True)
    else:
        st.warning(f"Figure not found: {filename}")

# =========================
# Overview
# =========================
if section == "Overview":
    st.header("1. Research overview")

    st.markdown("""
    ### Research question

    This project investigates whether monetary-fiscal policy interactions contribute to inflation dynamics
    in Morocco, particularly during historically active policy-mix episodes.

    ### Empirical focus

    The main empirical objective is to estimate the dynamic response of inflation to the interaction between
    monetary and fiscal policy variables, while allowing this effect to differ during active policy-mix periods.

    ### Methodological approach

    The empirical strategy is based on **Local Projections**, which allow the response of inflation to be estimated
    separately at different horizons.

    The general idea is to estimate whether the interaction term becomes more inflationary during selected historical
    periods such as 1974–1982.
    """)

    st.info(
        "Main finding: the inflationary effect of the monetary-fiscal interaction appears to be delayed, "
        "with stronger effects around one to two periods after the shock."
    )

# =========================
# Data
# =========================
elif section == "Data":
    st.header("2. Dataset")

    data_file = DATA_DIR / "df_base_1967_2000_model_used.xlsx"

    if data_file.exists():
        df = load_excel(data_file)
        if df is not None:
            st.subheader("Annual dataset used in the empirical model")
            st.dataframe(df, use_container_width=True)

            st.subheader("Dataset structure")
            col1, col2, col3 = st.columns(3)
            col1.metric("Number of observations", df.shape[0])
            col2.metric("Number of variables", df.shape[1])

            if "year" in df.columns:
                col3.metric("Period", f"{int(df['year'].min())}–{int(df['year'].max())}")
            else:
                col3.metric("Period", "1967–2000")

            st.subheader("Variables")
            st.write(list(df.columns))
    else:
        st.warning("The dataset file was not found in the data folder.")

# =========================
# Baseline Results
# =========================
elif section == "Baseline Results":
    st.header("3. Baseline Local Projection results")

    st.markdown("""
    The benchmark specification defines the active policy-mix period as **1974–1982**.

    This specification is used as the central empirical case because it captures a historically important period
    marked by macroeconomic tensions, external shocks, and active policy interactions.
    """)

    show_image(
        "01_lp_coefficients_policy_mix_1974_1982.png",
        "Baseline coefficients: active policy-mix period 1974–1982"
    )

    st.subheader("Baseline result table")

    result_file = RESULTS_DIR / "lp_results_1967_2000_active_1974_1982_simple.xlsx"

    if result_file.exists():
        df_res = load_excel(result_file)
        if df_res is not None:
            st.dataframe(df_res, use_container_width=True)
    else:
        st.warning("Baseline result file not found.")

    st.markdown("""
    ### Interpretation

    The estimated interaction effect is positive and statistically significant mainly at intermediate horizons.
    In the benchmark specification, the strongest effect appears around horizon 2, suggesting that the inflationary
    consequences of monetary-fiscal interactions are not immediate but delayed.
    """)

# =========================
# Robustness
# =========================
elif section == "Robustness":
    st.header("4. Robustness across alternative active periods")

    st.markdown("""
    To assess whether the results depend on a specific historical dating of the active policy-mix period,
    several alternative definitions are considered:

    - 1974–1979
    - 1974–1982
    - 1974–1985
    - 1976–1982
    """)

    show_image(
        "02_robustesse_interaction_active_periods.png",
        "Robustness of the interaction effect across alternative active periods"
    )

    st.subheader("Result files")

    files = {
        "Active period 1974–1979": "lp_results_1967_2000_active_1974_1979_simple.xlsx",
        "Active period 1974–1982": "lp_results_1967_2000_active_1974_1982_simple.xlsx",
        "Active period 1974–1985": "lp_results_1967_2000_active_1974_1985_simple.xlsx",
        "Active period 1976–1982": "lp_results_1967_2000_active_1976_1982_simple.xlsx",
    }

    selected_label = st.selectbox("Choose a robustness specification", list(files.keys()))
    selected_file = RESULTS_DIR / files[selected_label]

    if selected_file.exists():
        df_selected = load_excel(selected_file)
        if df_selected is not None:
            st.dataframe(df_selected, use_container_width=True)
    else:
        st.warning(f"Result file not found: {files[selected_label]}")

    st.markdown("""
    ### Robustness interpretation

    The results suggest that the positive inflationary effect of the policy-mix interaction is not driven by a single
    historical dating. However, the timing of the response varies depending on the definition of the active period,
    which should be interpreted carefully in the research paper.
    """)

# =========================
# Figures
# =========================
elif section == "Figures":
    st.header("5. Local Projection figures")

    figure_choice = st.selectbox(
        "Choose a figure",
        [
            "03_lp_graph_active_1974_1979.png",
            "03_lp_graph_active_1974_1982.png",
            "03_lp_graph_active_1974_1985.png",
            "03_lp_graph_active_1976_1982.png",
        ]
    )

    show_image(figure_choice, figure_choice)

# =========================
# Quarterly Extension
# =========================
elif section == "Quarterly Extension":
    st.header("6. Quarterly extension")

    st.markdown("""
    The next step of the project is to complement the annual analysis with a quarterly interpolated dataset.

    The trimestrialisation procedure is based on Mansouri's temporal disaggregation formula, which converts annual
    series into quarterly series using information from the previous, current, and following annual observations.

    This extension is useful because the annual sample contains a limited number of observations, which may affect
    the stability of dynamic econometric estimates.

    ### Important note

    The quarterly series are interpolated and should therefore be interpreted as constructed quarterly data,
    not as directly observed quarterly data.
    """)

    st.info("This section will be updated after the quarterly dataset and estimates are generated.")
