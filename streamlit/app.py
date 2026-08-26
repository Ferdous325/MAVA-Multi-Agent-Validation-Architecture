from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# MAVA RESEARCH DEMONSTRATOR
# Public thesis presentation layer
#
# IMPORTANT:
# - No Gemini/API calls
# - No Google Drive paths
# - No Colab paths
# - Uses only repository-contained frozen results
# ============================================================


st.set_page_config(
    page_title="MAVA | Multi-Agent Validation Architecture",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# REPOSITORY PATHS
# ============================================================

# app.py is located at:
# repository_root/streamlit/app.py
#
# Therefore parents[1] = repository root.

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS = PROJECT_ROOT / "results"
FIGURES = RESULTS / "figures"
TABLES = RESULTS / "tables"


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero {
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(128,128,128,.25);
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        margin-bottom: .4rem;
    }

    .hero p {
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    .pipeline {
        padding: 1.1rem;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,.25);
        text-align: center;
        min-height: 105px;
        margin-bottom: 10px;
    }

    .pipeline-number {
        font-size: .75rem;
        font-weight: 700;
        opacity: .65;
    }

    .pipeline-title {
        font-size: 1rem;
        font-weight: 700;
    }

    .pipeline-description {
        font-size: .82rem;
        opacity: .7;
    }

    .result-box {
        padding: 1.2rem;
        border-radius: 15px;
        border: 1px solid rgba(128,128,128,.25);
        text-align: center;
    }

    .result-number {
        font-size: 2rem;
        font-weight: 700;
    }

    .result-label {
        font-size: .85rem;
        opacity: .7;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOADERS
# ============================================================

@st.cache_data
def load_csv(filename):
    path = TABLES / filename

    if not path.exists():
        return None

    return pd.read_csv(path)


def load_figure(filename):
    path = FIGURES / filename

    if path.exists():
        return str(path)

    return None


# ============================================================
# LOAD THESIS TABLES
# ============================================================

overall_results = load_csv("FINAL_OVERALL_RESULTS.csv")
dataset_results = load_csv("FINAL_DATASET_RESULTS.csv")
claim_type_results = load_csv("FINAL_CLAIM_TYPE_RESULTS.csv")
transitions = load_csv("FINAL_VALIDATION_TRANSITIONS.csv")
corrections = load_csv("CORRECTION_VERIFICATION.csv")
verified_corrections = load_csv("VERIFIED_CORRECTIONS_71.csv")
remaining_mismatches = load_csv("REMAINING_MISMATCHES_19.csv")
remaining_unverified = load_csv("REMAINING_UNVERIFIED_14.csv")

# Optional supporting tables
table01 = load_csv("table01_dataset_results.csv")
table02 = load_csv("table02_overall_results.csv")
table03 = load_csv("table03_claim_type_results.csv")
table04 = load_csv("table04_correction_verification.csv")
table05 = load_csv("table05_validation_transitions.csv")


# ============================================================
# CONSTANT RESEARCH RESULTS
# ============================================================

TOTAL_CLAIMS = 126

BASELINE_MATCH = 22
BASELINE_MISMATCH = 90
BASELINE_UNVERIFIED = 14
BASELINE_VERIFIED = 112
BASELINE_RATE = 80.36

MAVA_MATCH = 93
MAVA_MISMATCH = 19
MAVA_UNVERIFIED = 14
MAVA_VERIFIED = 112
MAVA_RATE = 16.96

ABSOLUTE_REDUCTION = 63.39
RELATIVE_REDUCTION = 78.89

PROPOSED_CORRECTIONS = 84
VALID_CORRECTIONS = 71
INVALID_CORRECTIONS = 13


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🛡️ MAVA")

st.sidebar.caption(
    "Multi-Agent Validation Architecture"
)

st.sidebar.divider()

pages = [
    "🏠 Overview",
    "🏗️ MAVA Architecture",
    "📂 Experimental Datasets",
    "🔍 Claim Validation",
    "📊 Experimental Results",
    "🛡️ Correction & Verification",
    "🔎 Research Audit",
]

page = st.sidebar.radio(
    "Navigate",
    pages,
)

st.sidebar.divider()

st.sidebar.caption(
    "Frozen thesis experimental results"
)

st.sidebar.caption(
    "No live Gemini/API calls"
)


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        """
        <div class="hero">
            <h1>Multi-Agent Validation Architecture</h1>

            <p>
            Reducing Hallucination in Generative AI-Based Business Analytics
            through claim-level validation and independently verified correction.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # Key metrics
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Datasets",
        "3",
    )

    c2.metric(
        "Atomic Claims",
        "126",
    )

    c3.metric(
        "Baseline",
        "80.36%",
    )

    c4.metric(
        "MAVA",
        "16.96%",
    )

    st.divider()

    # --------------------------------------------------------
    # Main contribution
    # --------------------------------------------------------

    st.subheader("Research Contribution")

    st.write(
        """
        MAVA introduces a validation-oriented architecture for
        Generative AI-based business analytics. Instead of treating an
        LLM-generated narrative as a single output, the framework decomposes
        the narrative into atomic claims and evaluates those claims against
        deterministic ground truth.
        """
    )

    st.write(
        """
        Claims identified as inconsistent are passed through a deterministic
        correction process. Proposed corrections are independently verified
        before being accepted into the final MAVA result.
        """
    )

    st.success(
        f"MAVA reduced the measured hallucination rate from "
        f"{BASELINE_RATE:.2f}% to {MAVA_RATE:.2f}%, "
        f"a reduction of {ABSOLUTE_REDUCTION:.2f} percentage points."
    )

    # --------------------------------------------------------
    # Overall graph
    # --------------------------------------------------------

    st.subheader("Baseline vs MAVA")

    overall = pd.DataFrame(
        {
            "System": ["Baseline", "MAVA"],
            "Hallucination Rate (%)": [
                BASELINE_RATE,
                MAVA_RATE,
            ],
        }
    )

    fig = px.bar(
        overall,
        x="System",
        y="Hallucination Rate (%)",
        text_auto=".2f",
        title="Overall Hallucination Rate",
    )

    fig.update_layout(
        showlegend=False,
        yaxis_range=[0, 90],
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # Research scope
    # --------------------------------------------------------

    st.subheader("Experimental Scope")

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
        }
    )

    st.dataframe(
        scope,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# ARCHITECTURE
# ============================================================

elif page == "🏗️ MAVA Architecture":

    st.title("MAVA Architecture")

    st.write(
        """
        MAVA separates Generative AI narrative generation from
        deterministic evidence validation. The architecture creates an
        auditable path from a generated business narrative to a verified
        final result.
        """
    )

    # --------------------------------------------------------
    # Architecture image
    # --------------------------------------------------------

    architecture = load_figure(
        "fig01_mava_architecture.png"
    )

    if architecture:

        st.image(
            architecture,
            caption="MAVA Multi-Agent Validation Architecture",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Pipeline
    # --------------------------------------------------------

    st.subheader("Experimental Pipeline")

    stages = [
        (
            "01",
            "Dataset",
            "Business analytics data",
        ),
        (
            "02",
            "Ground Truth",
            "Deterministic evidence",
        ),
        (
            "03",
            "Narrative Agent",
            "LLM-generated analysis",
        ),
        (
            "04",
            "Claim Extraction",
            "Atomic claims",
        ),
        (
            "05",
            "Validator Agent",
            "Evidence comparison",
        ),
        (
            "06",
            "Correction Agent",
            "Deterministic correction",
        ),
        (
            "07",
            "Verification",
            "Independent checking",
        ),
        (
            "08",
            "Final MAVA Result",
            "Final evaluation",
        ),
    ]

    for start in range(0, len(stages), 4):

        cols = st.columns(4)

        for col, stage in zip(
            cols,
            stages[start:start + 4],
        ):

            number, title, description = stage

            with col:

                st.markdown(
                    f"""
                    <div class="pipeline">

                    <div class="pipeline-number">
                    {number}
                    </div>

                    <div class="pipeline-title">
                    {title}
                    </div>

                    <div class="pipeline-description">
                    {description}
                    </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.divider()

    st.subheader("Why MAVA is different")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Conventional LLM Analysis")

        st.code(
            "Dataset → LLM → Narrative",
            language="text",
        )

        st.write(
            "The generated narrative is typically treated as the final output."
        )

    with col2:

        st.markdown("### MAVA")

        st.code(
            "Dataset → Ground Truth → LLM → Claims → Validation → Correction → Verification",
            language="text",
        )

        st.write(
            "MAVA introduces claim-level evidence checking and verified correction."
        )


# ============================================================
# DATASETS
# ============================================================

elif page == "📂 Experimental Datasets":

    st.title("Experimental Datasets")

    st.write(
        """
        MAVA was evaluated across three datasets representing different
        business analytics scenarios.
        """
    )

    dataset_info = pd.DataFrame(
        {
            "Dataset": [
                "Customer Churn",
                "Financial",
                "Walmart",
            ],
            "Rows": [
                "7,043",
                "700",
                "6,435",
            ],
            "Columns": [
                "21",
                "16",
                "8",
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

    st.info(
        "Raw datasets are intentionally not included in the public "
        "demonstration repository. The public application presents the "
        "frozen experimental results and research evidence."
    )

    st.subheader("Dataset-wise claim distribution")

    fig = px.bar(
        dataset_info,
        x="Dataset",
        y="Claims",
        text="Claims",
        title="Atomic Claims by Dataset",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# CLAIM VALIDATION
# ============================================================

elif page == "🔍 Claim Validation":

    st.title("Claim-Level Validation")

    st.write(
        """
        Each generated business narrative was decomposed into atomic
        claims. Claims were classified as MATCH, MISMATCH, or UNVERIFIED
        according to their agreement with deterministic evidence.
        """
    )

    # --------------------------------------------------------
    # Status metrics
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
    # Claim type results
    # --------------------------------------------------------

    if claim_type_results is not None:

        st.subheader(
            "Claim-Type Validation"
        )

        st.dataframe(
            claim_type_results,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # Validation transition
    # --------------------------------------------------------

    if transitions is not None:

        st.subheader(
            "Validation Transitions"
        )

        st.dataframe(
            transitions,
            use_container_width=True,
            hide_index=True,
        )

    # --------------------------------------------------------
    # Existing figure
    # --------------------------------------------------------

    figure = load_figure(
        "fig04_claim_status_before_after.png"
    )

    if figure:

        st.image(
            figure,
            caption="Claim Status Before and After MAVA",
            use_container_width=True,
        )

    figure = load_figure(
        "fig05_claim_validation_transitions.png"
    )

    if figure:

        st.image(
            figure,
            caption="Claim Validation Transitions",
            use_container_width=True,
        )

    st.info(
        "The detailed 126-claim inventory remains part of the research "
        "artifacts. This public dashboard presents its aggregated "
        "validation evidence."
    )


# ============================================================
# EXPERIMENTAL RESULTS
# ============================================================

elif page == "📊 Experimental Results":

    st.title("Experimental Results")

    # --------------------------------------------------------
    # Main result
    # --------------------------------------------------------

    st.subheader(
        "Overall Hallucination Rate"
    )

    overall = pd.DataFrame(
        {
            "System": [
                "Baseline",
                "MAVA",
            ],
            "Hallucination Rate (%)": [
                BASELINE_RATE,
                MAVA_RATE,
            ],
        }
    )

    fig = px.bar(
        overall,
        x="System",
        y="Hallucination Rate (%)",
        text_auto=".2f",
        title="Baseline vs MAVA",
    )

    fig.update_layout(
        yaxis_range=[0, 90],
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    c1, c2 = st.columns(2)

    with c1:

        st.markdown(
            f"""
            <div class="result-box">

            <div class="result-number">
            {ABSOLUTE_REDUCTION:.2f}
            </div>

            <div class="result-label">
            Percentage-point reduction
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:

        st.markdown(
            f"""
            <div class="result-box">

            <div class="result-number">
            {RELATIVE_REDUCTION:.2f}%
            </div>

            <div class="result-label">
            Relative reduction
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # Dataset results
    # --------------------------------------------------------

    st.subheader(
        "Dataset-wise Results"
    )

    if dataset_results is not None:

        st.dataframe(
            dataset_results,
            use_container_width=True,
            hide_index=True,
        )

        required = [
            "Dataset",
            "Baseline_Hallucination_Rate_Percent",
            "MAVA_Hallucination_Rate_Percent",
        ]

        if all(
            c in dataset_results.columns
            for c in required
        ):

            d = dataset_results[
                required
            ].copy()

            d = d.rename(
                columns={
                    "Baseline_Hallucination_Rate_Percent":
                        "Baseline",
                    "MAVA_Hallucination_Rate_Percent":
                        "MAVA",
                }
            )

            d = d.melt(
                id_vars="Dataset",
                var_name="System",
                value_name="Hallucination Rate (%)",
            )

            fig = px.bar(
                d,
                x="Dataset",
                y="Hallucination Rate (%)",
                color="System",
                barmode="group",
                text_auto=".2f",
                title="Dataset-wise Hallucination Comparison",
            )

            fig.update_layout(
                yaxis_range=[0, 100]
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

    # --------------------------------------------------------
    # Claim type
    # --------------------------------------------------------

    st.subheader(
        "Claim-Type Results"
    )

    if claim_type_results is not None:

        st.dataframe(
            claim_type_results,
            use_container_width=True,
            hide_index=True,
        )

    figure = load_figure(
        "fig06_claim_type_hallucination_comparison.png"
    )

    if figure:

        st.image(
            figure,
            caption="Claim-Type Hallucination Comparison",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # Static thesis figures
    # --------------------------------------------------------

    st.subheader(
        "Thesis Visualizations"
    )

    figure_names = [
        "fig02_overall_hallucination_rate.png",
        "fig03_dataset_hallucination_comparison.png",
        "fig04_claim_status_before_after.png",
        "fig05_claim_validation_transitions.png",
    ]

    for name in figure_names:

        figure = load_figure(name)

        if figure:

            st.image(
                figure,
                caption=name,
                use_container_width=True,
            )


# ============================================================
# CORRECTION & VERIFICATION
# ============================================================

elif page == "🛡️ Correction & Verification":

    st.title(
        "Correction Agent & Independent Verification"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Proposed Corrections",
        PROPOSED_CORRECTIONS,
    )

    c2.metric(
        "Verified Corrections",
        VALID_CORRECTIONS,
    )

    c3.metric(
        "Rejected Corrections",
        INVALID_CORRECTIONS,
    )

    st.divider()

    st.write(
        """
        MAVA does not automatically accept corrections. Proposed corrections
        are independently checked against the frozen ground truth.
        Only corrections that pass verification are applied to the final
        MAVA result.
        """
    )

    verification = pd.DataFrame(
        {
            "Verification Status": [
                "VALID_CORRECTION",
                "INVALID_CORRECTION",
            ],
            "Count": [
                VALID_CORRECTIONS,
                INVALID_CORRECTIONS,
            ],
        }
    )

    fig = px.pie(
        verification,
        names="Verification Status",
        values="Count",
        title="Correction Verification",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.subheader(
        "Verification Evidence"
    )

    if corrections is not None:

        st.dataframe(
            corrections,
            use_container_width=True,
            hide_index=True,
        )

    st.subheader(
        "Verified Corrections"
    )

    if verified_corrections is not None:

        st.dataframe(
            verified_corrections,
            use_container_width=True,
            hide_index=True,
        )

    st.success(
        "71 independently verified corrections were applied "
        "to the final MAVA result."
    )


# ============================================================
# RESEARCH AUDIT
# ============================================================

elif page == "🔎 Research Audit":

    st.title(
        "Research Audit & Reproducibility"
    )

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
                "Proposed corrections",
                "Verified corrections",
                "Rejected corrections",
                "Remaining mismatches",
                "Remaining unverified",
                "Original evidence modified",
                "Gemini calls during validation/correction",
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
                "84",
                "71",
                "13",
                "19",
                "14",
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

    st.subheader(
        "Research Integrity"
    )

    st.markdown(
        """
        ✓ Original claims preserved

        ✓ Frozen ground truth preserved

        ✓ Original validation preserved

        ✓ Independently verified corrections

        ✓ Invalid corrections excluded

        ✓ No additional Gemini API calls

        ✓ Previous experimental outputs preserved

        ✓ Final result generated from the same 126 claims
        """
    )

    st.subheader(
        "Remaining Mismatches"
    )

    if remaining_mismatches is not None:

        st.dataframe(
            remaining_mismatches,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.write(
            "19 remaining mismatches are recorded in the thesis result tables."
        )

    st.subheader(
        "Remaining Unverified Claims"
    )

    if remaining_unverified is not None:

        st.dataframe(
            remaining_unverified,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.write(
            "14 claims remain UNVERIFIED and are preserved "
            "as part of the final evaluation."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "MAVA Research Demonstrator | "
    "Frozen thesis experimental evidence | "
    "No live Gemini/API calls"
)
