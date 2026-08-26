from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# MAVA — MULTI-AGENT VALIDATION ARCHITECTURE
# THESIS DEMONSTRATION APPLICATION
# ============================================================
#
# This application is a presentation layer over frozen
# experimental results stored in the GitHub repository.
#
# IMPORTANT:
#   - No Gemini API calls
#   - No external API calls
#   - No Google Drive paths
#   - No Colab paths
#   - No modification of research results
#
# Repository structure expected:
#
# MAVA-Multi-Agent-Validation-Architecture/
# │
# ├── streamlit/
# │   ├── app.py
# │   └── requirements.txt
# │
# └── results/
#     ├── figures/
#     └── tables/
#
# ============================================================


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MAVA | Thesis Demonstrator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# REPOSITORY PATHS
# ============================================================

# app.py:
# repository_root/streamlit/app.py
#
# parents[0] = streamlit/
# parents[1] = repository root

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_ROOT / "results"
TABLES_DIR = RESULTS_DIR / "tables"
FIGURES_DIR = RESULTS_DIR / "figures"


# ============================================================
# RESEARCH CONSTANTS
# ============================================================

TOTAL_DATASETS = 3
TOTAL_CLAIMS = 126

BASELINE_MATCH = 22
BASELINE_MISMATCH = 90
BASELINE_UNVERIFIED = 14
BASELINE_VERIFIED = 112
BASELINE_HALLUCINATION_RATE = 80.36

MAVA_MATCH = 93
MAVA_MISMATCH = 19
MAVA_UNVERIFIED = 14
MAVA_VERIFIED = 112
MAVA_HALLUCINATION_RATE = 16.96

ABSOLUTE_REDUCTION = 63.39
RELATIVE_REDUCTION = 78.89

PROPOSED_CORRECTIONS = 84
VALID_CORRECTIONS = 71
INVALID_CORRECTIONS = 13

DATASET_CLAIMS = {
    "Customer_Churn": 21,
    "Financial": 54,
    "Walmart": 51,
}


# ============================================================
# CUSTOM CSS
# ============================================================
#
# Only CSS is used here.
# No HTML content is used for the actual application UI.
#
# This avoids the raw <p>, <div>, etc. problem that appeared
# in the previous Streamlit deployment.
# ============================================================

st.markdown(
    """
    <style>

    /* Main application width */
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.20);
    }

    /* Small muted text */
    .muted {
        color: #777777;
        font-size: 0.9rem;
    }

    /* Section spacing */
    .section-space {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }

    /* Hide Streamlit deploy menu where possible */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FILE LOADERS
# ============================================================

@st.cache_data(show_spinner=False)
def load_csv(filename):
    """
    Load a CSV from results/tables.
    Returns None when the file does not exist.
    """
    path = TABLES_DIR / filename

    if not path.exists():
        return None

    try:
        return pd.read_csv(path)
    except Exception:
        return None


def figure_exists(filename):
    """
    Return figure path when available.
    """
    path = FIGURES_DIR / filename

    if path.exists():
        return str(path)

    return None


# ============================================================
# LOAD RESULT TABLES
# ============================================================

overall_results = load_csv(
    "FINAL_OVERALL_RESULTS.csv"
)

dataset_results = load_csv(
    "FINAL_DATASET_RESULTS.csv"
)

claim_type_results = load_csv(
    "FINAL_CLAIM_TYPE_RESULTS.csv"
)

transitions = load_csv(
    "FINAL_VALIDATION_TRANSITIONS.csv"
)

correction_verification = load_csv(
    "CORRECTION_VERIFICATION.csv"
)

verified_corrections = load_csv(
    "VERIFIED_CORRECTIONS_71.csv"
)

remaining_mismatches = load_csv(
    "REMAINING_MISMATCHES_19.csv"
)

remaining_unverified = load_csv(
    "REMAINING_UNVERIFIED_14.csv"
)

claim_level_analysis = load_csv(
    "FINAL_THESIS_CLAIM_LEVEL_ANALYSIS.csv"
)


# ============================================================
# REPOSITORY HEALTH CHECK
# ============================================================

def repository_ready():
    """
    Basic check that the Streamlit application has access
    to the expected repository directories.
    """
    return (
        PROJECT_ROOT.exists()
        and RESULTS_DIR.exists()
        and TABLES_DIR.exists()
        and FIGURES_DIR.exists()
    )


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛡️ MAVA")

st.sidebar.caption(
    "Multi-Agent Validation Architecture"
)

st.sidebar.caption(
    "Thesis Research Demonstrator"
)

st.sidebar.divider()

PAGES = [
    "🏠 Overview",
    "🏗️ MAVA Architecture",
    "📂 Experimental Scope",
    "🔍 Claim-Level Validation",
    "📊 Results & Visualizations",
    "🛡️ Correction & Verification",
    "🔎 Research Audit",
]

selected_page = st.sidebar.radio(
    "Navigation",
    PAGES,
)

st.sidebar.divider()

st.sidebar.markdown(
    "**Research status**"
)

st.sidebar.success(
    "Frozen experimental results"
)

st.sidebar.caption(
    "No live Gemini/API calls are made."
)

st.sidebar.caption(
    "Results are presentation-only."
)


# ============================================================
# SAFETY CHECK
# ============================================================

if not repository_ready():

    st.error(
        "The expected MAVA repository structure could not be found."
    )

    st.code(
        """
results/
├── figures/
└── tables/
        """,
        language="text",
    )

    st.stop()


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if selected_page == "🏠 Overview":

    st.title(
        "Multi-Agent Validation Architecture"
    )

    st.subheader(
        "Reducing Hallucination in Generative AI-Based Business Analytics"
    )

    st.write(
        """
        MAVA is a validation-oriented research framework designed to
        evaluate and reduce hallucination in Generative AI-based
        business analytics. Instead of treating an LLM-generated
        narrative as a single trusted output, MAVA decomposes the
        narrative into atomic claims and evaluates those claims
        against deterministic evidence.
        """
    )

    st.info(
        "The application presents frozen thesis experimental evidence. "
        "It does not regenerate narratives or call Gemini."
    )

    st.divider()

    # --------------------------------------------------------
    # KEY METRICS
    # --------------------------------------------------------

    st.subheader("Key Research Results")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Datasets",
        f"{TOTAL_DATASETS}",
    )

    c2.metric(
        "Atomic Claims",
        f"{TOTAL_CLAIMS}",
    )

    c3.metric(
        "Baseline Hallucination",
        f"{BASELINE_HALLUCINATION_RATE:.2f}%",
    )

    c4.metric(
        "MAVA Hallucination",
        f"{MAVA_HALLUCINATION_RATE:.2f}%",
    )

    st.divider()

    # --------------------------------------------------------
    # CONTRIBUTION
    # --------------------------------------------------------

    st.subheader("Research Contribution")

    left, right = st.columns(2)

    with left:

        st.markdown("### Conventional approach")

        st.code(
            "Dataset → LLM → Narrative",
            language="text",
        )

        st.write(
            """
            A conventional workflow may treat the generated narrative
            as the final analytical output, making it difficult to
            identify exactly which statements are unsupported or
            incorrect.
            """
        )

    with right:

        st.markdown("### MAVA approach")

        st.code(
            "Dataset → Ground Truth → LLM Narrative → "
            "Atomic Claims → Validation → Correction → Verification",
            language="text",
        )

        st.write(
            """
            MAVA introduces claim-level validation and independent
            verification so that the generated analytical narrative
            can be evaluated against deterministic evidence.
            """
        )

    st.divider()

    # --------------------------------------------------------
    # MAIN RESULT
    # --------------------------------------------------------

    st.subheader(
        "Overall Experimental Result"
    )

    overall_chart = pd.DataFrame(
        {
            "System": [
                "Baseline",
                "MAVA",
            ],
            "Hallucination Rate (%)": [
                BASELINE_HALLUCINATION_RATE,
                MAVA_HALLUCINATION_RATE,
            ],
        }
    )

    fig = px.bar(
        overall_chart,
        x="System",
        y="Hallucination Rate (%)",
        text_auto=".2f",
        title="Baseline vs MAVA Hallucination Rate",
    )

    fig.update_layout(
        yaxis_range=[0, 90],
        showlegend=False,
        height=450,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Absolute reduction",
            f"{ABSOLUTE_REDUCTION:.2f} percentage points",
        )

    with c2:

        st.metric(
            "Relative reduction",
            f"{RELATIVE_REDUCTION:.2f}%",
        )

    st.success(
        "The final MAVA experiment reduced the measured hallucination "
        "rate from 80.36% to 16.96%."
    )

    st.divider()

    # --------------------------------------------------------
    # DATASET SCOPE
    # --------------------------------------------------------

    st.subheader(
        "Experimental Scope"
    )

    scope = pd.DataFrame(
        {
            "Dataset": [
                "Customer Churn",
                "Financial",
                "Walmart",
            ],
            "Claims": [
                21,
                54,
                51,
            ],
            "Domain": [
                "Customer analytics",
                "Financial analytics",
                "Retail sales analytics",
            ],
        }
    )

    st.dataframe(
        scope,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PAGE 2 — ARCHITECTURE
# ============================================================

elif selected_page == "🏗️ MAVA Architecture":

    st.title(
        "MAVA Architecture"
    )

    st.write(
        """
        The proposed Multi-Agent Validation Architecture separates
        narrative generation from evidence-based validation and
        correction. This creates an auditable path from an LLM-generated
        business narrative to an evidence-backed final result.
        """
    )

    st.divider()

    # --------------------------------------------------------
    # ARCHITECTURE FIGURE
    # --------------------------------------------------------

    architecture_image = figure_exists(
        "fig01_mava_architecture.png"
    )

    if architecture_image:

        st.image(
            architecture_image,
            caption="MAVA Multi-Agent Validation Architecture",
            use_container_width=True,
        )

    st.divider()

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.subheader(
        "MAVA Processing Pipeline"
    )

    stages = [
        (
            "01",
            "Dataset",
            "Business analytics input",
        ),
        (
            "02",
            "Ground Truth",
            "Deterministic evidence",
        ),
        (
            "03",
            "Narrative Agent",
            "LLM-generated narrative",
        ),
        (
            "04",
            "Claim Extraction",
            "Atomic claim inventory",
        ),
        (
            "05",
            "Validator Agent",
            "MATCH / MISMATCH / UNVERIFIED",
        ),
        (
            "06",
            "Correction Agent",
            "Evidence-based correction",
        ),
        (
            "07",
            "Verification Agent",
            "Independent verification",
        ),
        (
            "08",
            "Final MAVA Result",
            "Final validated output",
        ),
    ]

    for start in range(
        0,
        len(stages),
        4,
    ):

        columns = st.columns(4)

        current = stages[
            start:start + 4
        ]

        for column, stage in zip(
            columns,
            current,
        ):

            number, title, description = stage

            with column:

                st.markdown(
                    f"### {number}. {title}"
                )

                st.caption(
                    description
                )

        if start + 4 < len(stages):

            st.divider()

    st.divider()

    # --------------------------------------------------------
    # AGENT ROLES
    # --------------------------------------------------------

    st.subheader(
        "Functional Agent Roles"
    )

    agent_table = pd.DataFrame(
        {
            "Component": [
                "Narrative Agent",
                "Claim Extraction",
                "Validator Agent",
                "Correction Agent",
                "Verification Agent",
            ],
            "Primary Function": [
                "Generate business analytical narrative",
                "Decompose narrative into atomic claims",
                "Compare claims with deterministic evidence",
                "Generate evidence-supported corrections",
                "Independently verify proposed corrections",
            ],
        }
    )

    st.dataframe(
        agent_table,
        use_container_width=True,
        hide_index=True,
    )

    st.info(
        "The central contribution of MAVA is the validation architecture "
        "surrounding Generative AI output rather than simply generating "
        "another analytical narrative."
    )


# ============================================================
# PAGE 3 — EXPERIMENTAL SCOPE
# ============================================================

elif selected_page == "📂 Experimental Scope":

    st.title(
        "Experimental Scope"
    )

    st.write(
        """
        The experiment evaluates MAVA across three business analytics
        datasets and 126 atomic claims.
        """
    )

    dataset_info = pd.DataFrame(
        {
            "Dataset": [
                "Customer Churn",
                "Financial",
                "Walmart",
            ],
            "Claims": [
                21,
                54,
                51,
            ],
            "Domain": [
                "Customer analytics",
                "Financial analytics",
                "Retail sales analytics",
            ],
        }
    )

    st.dataframe(
        dataset_info,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader(
        "Claim Distribution"
    )

    fig = px.bar(
        dataset_info,
        x="Dataset",
        y="Claims",
        text="Claims",
        title="Atomic Claims by Dataset",
    )

    fig.update_layout(
        height=450,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    st.info(
        "Raw datasets are intentionally not included in the public "
        "Streamlit presentation layer. The application focuses on "
        "the reproducible research results and frozen evidence."
    )


# ============================================================
# PAGE 4 — CLAIM-LEVEL VALIDATION
# ============================================================

elif selected_page == "🔍 Claim-Level Validation":

    st.title(
        "Claim-Level Validation"
    )

    st.write(
        """
        MAVA evaluates individual analytical statements rather than
        treating an entire generated narrative as one indivisible output.
        Each claim is assigned a validation status based on available
        deterministic evidence.
        """
    )

    # --------------------------------------------------------
    # CLAIM METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Claims",
        TOTAL_CLAIMS,
    )

    c2.metric(
        "MATCH",
        MAVA_MATCH,
    )

    c3.metric(
        "MISMATCH",
        MAVA_MISMATCH,
    )

    c4.metric(
        "UNVERIFIED",
        MAVA_UNVERIFIED,
    )

    st.divider()

    # --------------------------------------------------------
    # CLAIM LEVEL DATASET
    # --------------------------------------------------------

    if claim_level_analysis is not None:

        st.subheader(
            "Claim Inventory"
        )

        df = claim_level_analysis.copy()

        # Dataset filter
        if "Dataset" in df.columns:

            datasets = sorted(
                df["Dataset"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_dataset = st.selectbox(
                "Dataset",
                ["All"] + datasets,
            )

            if selected_dataset != "All":

                df = df[
                    df["Dataset"].astype(str)
                    == selected_dataset
                ]

        # Status filter
        status_column = None

        for candidate in [
            "MAVA_Status",
            "Validation_Status",
            "Final_Status",
        ]:

            if candidate in df.columns:

                status_column = candidate
                break

        if status_column:

            selected_status = st.multiselect(
                "MAVA Validation Status",
                [
                    "MATCH",
                    "MISMATCH",
                    "UNVERIFIED",
                ],
                default=[
                    "MATCH",
                    "MISMATCH",
                    "UNVERIFIED",
                ],
            )

            df = df[
                df[status_column].astype(str)
                .isin(selected_status)
            ]

        # Claim search
        search_text = st.text_input(
            "Search claim text",
            placeholder="Type a keyword or phrase...",
        )

        if search_text:

            text_columns = [
                c
                for c in [
                    "Original_Claim_Text",
                    "MAVA_Claim_Text",
                    "Claim_Text",
                    "Claim",
                ]
                if c in df.columns
            ]

            if text_columns:

                mask = pd.Series(
                    False,
                    index=df.index,
                )

                for column in text_columns:

                    mask = (
                        mask
                        |
                        df[column]
                        .fillna("")
                        .astype(str)
                        .str.contains(
                            search_text,
                            case=False,
                            regex=False,
                        )
                    )

                df = df[mask]

        st.write(
            f"Showing **{len(df)}** claim records."
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.warning(
            "FINAL_THESIS_CLAIM_LEVEL_ANALYSIS.csv "
            "was not found in results/tables."
        )

        st.info(
            "Upload FINAL_THESIS_CLAIM_LEVEL_ANALYSIS.csv "
            "to results/tables to enable the full claim explorer."
        )

    st.divider()

    # --------------------------------------------------------
    # CLAIM TYPE RESULTS
    # --------------------------------------------------------

    st.subheader(
        "Claim-Type Validation"
    )

    if claim_type_results is not None:

        st.dataframe(
            claim_type_results,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # TRANSITIONS
    # --------------------------------------------------------

    st.subheader(
        "Validation Transitions"
    )

    if transitions is not None:

        st.dataframe(
            transitions,
            use_container_width=True,
            hide_index=True,
        )

    transition_image = figure_exists(
        "fig05_claim_validation_transitions.png"
    )

    if transition_image:

        st.image(
            transition_image,
            caption="Claim Validation Transitions",
            use_container_width=True,
        )


# ============================================================
# PAGE 5 — RESULTS & VISUALIZATIONS
# ============================================================

elif selected_page == "📊 Results & Visualizations":

    st.title(
        "Experimental Results & Visualizations"
    )

    st.write(
        """
        The following results compare the baseline LLM validation
        performance with the final MAVA result using the same
        126-claim experimental inventory.
        """
    )

    # --------------------------------------------------------
    # OVERALL RESULT
    # --------------------------------------------------------

    st.subheader(
        "1. Overall Hallucination Rate"
    )

    overall_chart = pd.DataFrame(
        {
            "System": [
                "Baseline",
                "MAVA",
            ],
            "Hallucination Rate (%)": [
                BASELINE_HALLUCINATION_RATE,
                MAVA_HALLUCINATION_RATE,
            ],
        }
    )

    fig = px.bar(
        overall_chart,
        x="System",
        y="Hallucination Rate (%)",
        text_auto=".2f",
        title="Baseline vs MAVA Hallucination Rate",
    )

    fig.update_layout(
        yaxis_range=[0, 90],
        showlegend=False,
        height=450,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Absolute Reduction",
            f"{ABSOLUTE_REDUCTION:.2f} pp",
        )

    with c2:

        st.metric(
            "Relative Reduction",
            f"{RELATIVE_REDUCTION:.2f}%",
        )

    st.divider()

    # --------------------------------------------------------
    # DATASET LEVEL
    # --------------------------------------------------------

    st.subheader(
        "2. Dataset-Wise Comparison"
    )

    if dataset_results is not None:

        required = [
            "Dataset",
            "Baseline_Hallucination_Rate_Percent",
            "MAVA_Hallucination_Rate_Percent",
        ]

        if all(
            column in dataset_results.columns
            for column in required
        ):

            chart_data = dataset_results[
                required
            ].copy()

            chart_data = chart_data.rename(
                columns={
                    "Baseline_Hallucination_Rate_Percent":
                        "Baseline",
                    "MAVA_Hallucination_Rate_Percent":
                        "MAVA",
                }
            )

            chart_data = chart_data.melt(
                id_vars="Dataset",
                var_name="System",
                value_name="Hallucination Rate (%)",
            )

            fig = px.bar(
                chart_data,
                x="Dataset",
                y="Hallucination Rate (%)",
                color="System",
                barmode="group",
                text_auto=".2f",
                title="Hallucination Rate by Dataset",
            )

            fig.update_layout(
                yaxis_range=[0, 100],
                height=500,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        st.dataframe(
            dataset_results,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # CLAIM TYPE
    # --------------------------------------------------------

    st.subheader(
        "3. Claim-Type Comparison"
    )

    if claim_type_results is not None:

        required = [
            "Claim_Type",
            "Baseline_Hallucination_Rate_Percent",
            "MAVA_Hallucination_Rate_Percent",
        ]

        if all(
            column in claim_type_results.columns
            for column in required
        ):

            chart_data = claim_type_results[
                required
            ].copy()

            chart_data = chart_data.fillna(0)

            chart_data = chart_data.rename(
                columns={
                    "Baseline_Hallucination_Rate_Percent":
                        "Baseline",
                    "MAVA_Hallucination_Rate_Percent":
                        "MAVA",
                }
            )

            chart_data = chart_data.melt(
                id_vars="Claim_Type",
                var_name="System",
                value_name="Hallucination Rate (%)",
            )

            fig = px.bar(
                chart_data,
                x="Claim_Type",
                y="Hallucination Rate (%)",
                color="System",
                barmode="group",
                text_auto=".2f",
                title="Hallucination Rate by Claim Type",
            )

            fig.update_layout(
                yaxis_range=[0, 110],
                height=500,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        st.dataframe(
            claim_type_results,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # TRANSITIONS
    # --------------------------------------------------------

    st.subheader(
        "4. Validation Transitions"
    )

    if transitions is not None:

        st.dataframe(
            transitions,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # STATIC THESIS FIGURES
    # --------------------------------------------------------

    st.subheader(
        "5. Thesis Figures"
    )

    figure_list = [
        (
            "fig02_overall_hallucination_rate.png",
            "Overall Hallucination Rate",
        ),
        (
            "fig03_dataset_hallucination_comparison.png",
            "Dataset-Wise Hallucination Comparison",
        ),
        (
            "fig04_claim_status_before_after.png",
            "Claim Status Before and After MAVA",
        ),
        (
            "fig05_claim_validation_transitions.png",
            "Claim Validation Transitions",
        ),
        (
            "fig06_claim_type_hallucination_comparison.png",
            "Claim-Type Hallucination Comparison",
        ),
    ]

    for filename, caption in figure_list:

        image = figure_exists(filename)

        if image:

            st.image(
                image,
                caption=caption,
                use_container_width=True,
            )


# ============================================================
# PAGE 6 — CORRECTION & VERIFICATION
# ============================================================

elif selected_page == "🛡️ Correction & Verification":

    st.title(
        "Correction Agent & Independent Verification"
    )

    st.write(
        """
        MAVA does not automatically accept a proposed correction.
        Corrections are independently checked against frozen
        deterministic ground truth before they are incorporated into
        the final experimental result.
        """
    )

    # --------------------------------------------------------
    # CORRECTION METRICS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Proposed Corrections",
        PROPOSED_CORRECTIONS,
    )

    c2.metric(
        "Valid Corrections",
        VALID_CORRECTIONS,
    )

    c3.metric(
        "Rejected Corrections",
        INVALID_CORRECTIONS,
    )

    st.divider()

    # --------------------------------------------------------
    # VERIFICATION CHART
    # --------------------------------------------------------

    verification_chart = pd.DataFrame(
        {
            "Status": [
                "Valid Corrections",
                "Rejected Corrections",
            ],
            "Count": [
                VALID_CORRECTIONS,
                INVALID_CORRECTIONS,
            ],
        }
    )

    fig = px.pie(
        verification_chart,
        names="Status",
        values="Count",
        title="Correction Verification",
        hole=0.45,
    )

    fig.update_layout(
        height=450,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    # --------------------------------------------------------
    # VERIFICATION TABLE
    # --------------------------------------------------------

    st.subheader(
        "Correction Verification Records"
    )

    if correction_verification is not None:

        st.dataframe(
            correction_verification,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # VERIFIED CORRECTIONS
    # --------------------------------------------------------

    st.subheader(
        "Independently Verified Corrections"
    )

    if verified_corrections is not None:

        st.dataframe(
            verified_corrections,
            use_container_width=True,
            hide_index=True,
        )

    st.success(
        "71 corrections passed independent verification and were "
        "applied to the final MAVA result."
    )

    st.info(
        "13 proposed corrections were rejected and therefore excluded "
        "from the verified MAVA result."
    )


# ============================================================
# PAGE 7 — RESEARCH AUDIT
# ============================================================

elif selected_page == "🔎 Research Audit":

    st.title(
        "Research Audit & Reproducibility"
    )

    st.write(
        """
        This section summarizes the integrity controls used when
        producing the final thesis result.
        """
    )

    # --------------------------------------------------------
    # AUDIT TABLE
    # --------------------------------------------------------

    audit = pd.DataFrame(
        {
            "Research Item": [
                "Datasets evaluated",
                "Atomic claims",
                "Baseline MATCH",
                "Baseline MISMATCH",
                "Baseline UNVERIFIED",
                "MAVA MATCH",
                "MAVA MISMATCH",
                "MAVA UNVERIFIED",
                "Baseline verified claims",
                "MAVA verified claims",
                "Proposed corrections",
                "Verified corrections",
                "Rejected corrections",
                "Remaining mismatches",
                "Remaining unverified",
                "Original claims modified",
                "Original validation modified",
                "Frozen ground truth modified",
                "Gemini calls during correction",
            ],
            "Value": [
                "3",
                "126",
                "22",
                "90",
                "14",
                "93",
                "19",
                "14",
                "112",
                "112",
                "84",
                "71",
                "13",
                "19",
                "14",
                "No",
                "No",
                "No",
                "0",
            ],
        }
    )

    st.dataframe(
        audit,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # --------------------------------------------------------
    # RESEARCH INTEGRITY
    # --------------------------------------------------------

    st.subheader(
        "Research Integrity Controls"
    )

    integrity_items = [
        "Original claims preserved",
        "Original Gemini narratives preserved",
        "Frozen ground truth preserved",
        "Original baseline validation preserved",
        "Corrections independently verified",
        "Invalid corrections excluded",
        "Same 126-claim inventory used",
        "No additional Gemini calls during correction",
        "Previous experimental outputs preserved",
    ]

    for item in integrity_items:

        st.success(
            f"✓ {item}"
        )

    st.divider()

    # --------------------------------------------------------
    # REMAINING MISMATCHES
    # --------------------------------------------------------

    st.subheader(
        "Remaining Mismatches"
    )

    st.caption(
        "19 claims remain MISMATCH after the verified correction stage."
    )

    if remaining_mismatches is not None:

        st.dataframe(
            remaining_mismatches,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "The detailed remaining mismatch file is not available "
            "in the public repository."
        )

    # --------------------------------------------------------
    # REMAINING UNVERIFIED
    # --------------------------------------------------------

    st.subheader(
        "Remaining Unverified Claims"
    )

    st.caption(
        "14 claims remain UNVERIFIED because sufficient evidence "
        "was not available for deterministic validation."
    )

    if remaining_unverified is not None:

        st.dataframe(
            remaining_unverified,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "The detailed remaining unverified file is not available "
            "in the public repository."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "MAVA Research Demonstrator • "
    "Multi-Agent Validation Architecture • "
   
)
