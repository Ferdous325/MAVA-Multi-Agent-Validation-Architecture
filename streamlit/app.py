
from pathlib import Path
import json
import pandas as pd
import streamlit as st
import plotly.express as px

# ============================================================
# MAVA RESEARCH DEMONSTRATOR
# Frozen research-result presentation layer.
# No Gemini/API calls are made by this application.
# ============================================================

st.set_page_config(
    page_title="MAVA Research Demonstrator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Styling
# ------------------------------------------------------------
st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}
.hero {
    padding: 1.6rem 1.8rem;
    border-radius: 18px;
    border: 1px solid rgba(128,128,128,.25);
    margin-bottom: 1.2rem;
}
.hero h1 {margin-bottom: .3rem;}
.hero p {margin-bottom: 0; font-size: 1.05rem;}
.section-note {color: #666; font-size: .92rem;}
.metric-label {font-size: .85rem; color:#666;}
.pipeline {
    padding: 1rem;
    border: 1px solid rgba(128,128,128,.25);
    border-radius: 14px;
    text-align:center;
    min-height: 95px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Paths
# Works in Colab/Drive and can also work locally if the
# MAVA_RESEARCH_ROOT environment variable is supplied.
# ------------------------------------------------------------
DEFAULT_ROOTS = [
    Path("/content/drive/MyDrive/MAVA_Research"),
    Path.cwd(),
]

def locate_project():
    for root in DEFAULT_ROOTS:
        if (root / "outputs").exists() and (root / "results").exists():
            return root
    return DEFAULT_ROOTS[0]

PROJECT_ROOT = locate_project()
OUTPUTS = PROJECT_ROOT / "outputs"
RESULTS = PROJECT_ROOT / "results"
TABLES = RESULTS / "tables"
FIGURES = RESULTS / "figures"
DATA = PROJECT_ROOT / "data"

# ------------------------------------------------------------
# Loaders
# ------------------------------------------------------------
@st.cache_data
def csv_file(path_str):
    path = Path(path_str)
    return pd.read_csv(path) if path.exists() else None

@st.cache_data
def text_file(path_str):
    path = Path(path_str)
    return path.read_text(encoding="utf-8") if path.exists() else None

def first_existing(*paths):
    for p in paths:
        if p.exists():
            return p
    return None

def table(name):
    p = TABLES / name
    return csv_file(str(p))

def output_table(*relative_paths):
    p = first_existing(*(OUTPUTS / x for x in relative_paths))
    return csv_file(str(p)) if p else None

def narrative(dataset):
    p = OUTPUTS / "narratives" / dataset / "raw_response.txt"
    return text_file(str(p))

def image_path(name):
    p = FIGURES / name
    return p if p.exists() else None

final_validation = output_table(
    "validation/mava_revalidation/FINAL_MAVA_REVALIDATION.csv",
    "final_thesis_analysis/FINAL_THESIS_CLAIM_LEVEL_ANALYSIS.csv",
)

dataset_results = table("FINAL_DATASET_RESULTS.csv")
claim_type_results = table("FINAL_CLAIM_TYPE_RESULTS.csv")
transitions = table("FINAL_VALIDATION_TRANSITIONS.csv")
overall_results = table("FINAL_OVERALL_RESULTS.csv")
corrections = table("CORRECTION_VERIFICATION.csv")
claims = output_table("claims/ALL_DATASETS_ATOMIC_CLAIMS.csv")

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
st.sidebar.title("🛡️ MAVA")
st.sidebar.caption("Multi-Agent Validation Architecture")
st.sidebar.divider()

pages = [
    "🏠 Overview",
    "🏗️ Architecture",
    "📂 Datasets",
    "🤖 LLM Narratives",
    "🔍 Claim Validation",
    "📊 Results",
    "🛡️ Correction Agent",
    "🔎 Research Audit",
]
page = st.sidebar.radio("Navigate", pages)

st.sidebar.divider()
st.sidebar.caption("Frozen experimental artifacts")
st.sidebar.caption("No Gemini API call is made by this app.")

if not OUTPUTS.exists():
    st.error(f"Could not find MAVA outputs at:\n{OUTPUTS}")
    st.stop()

# ============================================================
# OVERVIEW
# ============================================================
if page == "🏠 Overview":
    st.markdown("""
    <div class="hero">
        <h1>Multi-Agent Validation Architecture (MAVA)</h1>
        <p>
        A research framework for reducing hallucination in
        Generative AI-based Business Analytics through claim-level
        validation and verified correction.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Datasets", "3")
    c2.metric("Atomic Claims", "126")
    c3.metric("Baseline", "80.36%")
    c4.metric("MAVA", "16.96%")

    st.divider()

    left, right = st.columns([1.25, 1])

    with left:
        st.subheader("Research contribution")
        st.write(
            "MAVA separates narrative generation from evidence-based validation. "
            "LLM-generated business narratives are decomposed into atomic claims, "
            "validated against deterministic ground truth, and corrected only "
            "when proposed corrections pass independent verification."
        )

        st.success(
            "Hallucination rate reduction: 63.39 percentage points "
            "(78.89% relative reduction)."
        )

    with right:
        st.subheader("Experimental scope")
        st.write("Three business analytics datasets:")
        st.markdown("""
        - **Customer Churn** — 21 claims
        - **Financial** — 54 claims
        - **Walmart** — 51 claims
        """)
        st.write("Total: **126 claims**")

    st.divider()

    st.subheader("Baseline → MAVA")
    overview_df = pd.DataFrame({
        "System": ["Baseline", "MAVA"],
        "Hallucination Rate (%)": [80.36, 16.96],
    })
    fig = px.bar(
        overview_df,
        x="System",
        y="Hallucination Rate (%)",
        text_auto=".2f",
        title="Overall Hallucination Rate",
    )
    fig.update_layout(showlegend=False, yaxis_range=[0, 90])
    st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ARCHITECTURE
# ============================================================
elif page == "🏗️ Architecture":
    st.title("MAVA Architecture")
    st.caption(
        "The architecture below represents the experimental workflow "
        "implemented and evaluated in the thesis."
    )

    stages = [
        ("01", "Dataset", "Business analytics input"),
        ("02", "Ground Truth", "Deterministic evidence"),
        ("03", "Narrative Agent", "LLM-generated narrative"),
        ("04", "Claim Extraction", "Atomic claim inventory"),
        ("05", "Validator Agent", "MATCH / MISMATCH / UNVERIFIED"),
        ("06", "Correction Agent", "Deterministic correction"),
        ("07", "Correction Verification", "Independent verification"),
        ("08", "Final MAVA Validation", "Final evaluation"),
    ]

    for row_start in range(0, len(stages), 4):
        cols = st.columns(4)
        for col, (num, title, desc) in zip(cols, stages[row_start:row_start+4]):
            with col:
                st.markdown(
                    f'<div class="pipeline"><b>{num}. {title}</b><br>'
                    f'<span class="section-note">{desc}</span></div>',
                    unsafe_allow_html=True
                )
        if row_start + 4 < len(stages):
            st.markdown("<br>", unsafe_allow_html=True)

    st.divider()

    st.subheader("What is different about MAVA?")
    st.markdown("""
    **Traditional LLM business analysis**

    `Dataset → LLM → Narrative`

    **MAVA**

    `Dataset → Ground Truth → LLM Narrative → Atomic Claims → Validation → Correction → Verification → Final Result`
    """)

    st.info(
        "The key contribution is not simply using an LLM. "
        "It is the validation-oriented architecture that creates an "
        "auditable path from generated narrative to evidence-backed claims."
    )

# ============================================================
# DATASETS
# ============================================================
elif page == "📂 Datasets":
    st.title("Dataset Explorer")

    names = {
        "Customer_Churn": "customer_churn.csv",
        "Financial": "Financial.csv",
        "Walmart": "Walmart.csv",
    }
    selected = st.selectbox("Select dataset", list(names))

    path = DATA / names[selected]
    if not path.exists():
        st.warning(f"Dataset file not found: {path}")
    else:
        df = csv_file(str(path))

        a, b, c = st.columns(3)
        a.metric("Rows", f"{len(df):,}")
        b.metric("Columns", f"{len(df.columns):,}")
        c.metric("Claims", {"Customer_Churn": 21, "Financial": 54, "Walmart": 51}[selected])

        st.subheader("Preview")
        st.dataframe(df.head(20), use_container_width=True, hide_index=True)

        st.subheader("Schema")
        schema = pd.DataFrame({
            "Column": df.columns,
            "Data Type": [str(x) for x in df.dtypes],
            "Missing Values": [int(df[c].isna().sum()) for c in df.columns],
        })
        st.dataframe(schema, use_container_width=True, hide_index=True)

# ============================================================
# NARRATIVES
# ============================================================
elif page == "🤖 LLM Narratives":
    st.title("Preserved Gemini Narratives")
    st.caption(
        "These are the original saved responses used as evidence in the experiment."
    )

    selected = st.selectbox(
        "Select dataset",
        ["Customer_Churn", "Financial", "Walmart"]
    )
    raw = narrative(selected)

    if raw:
        st.text_area("Original Gemini response", raw, height=520)
    else:
        st.warning("Narrative evidence not found.")

    st.info(
        "This page displays preserved evidence only. "
        "It does not call Gemini again."
    )

# ============================================================
# CLAIM VALIDATION
# ============================================================
elif page == "🔍 Claim Validation":
    st.title("Claim-Level Validation")

    if final_validation is None:
        st.error("Final validation artifact not found.")
        st.stop()

    df = final_validation.copy()

    id_col = next(
        (c for c in ["Canonical_Claim_ID", "Global_Claim_ID", "Claim_ID"]
         if c in df.columns),
        None
    )
    status_col = "MAVA_Status" if "MAVA_Status" in df.columns else "Validation_Status"

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Claims", len(df))
    c2.metric("MATCH", int((df[status_col] == "MATCH").sum()))
    c3.metric("MISMATCH", int((df[status_col] == "MISMATCH").sum()))

    st.divider()

    if "Dataset" in df.columns:
        selected_ds = st.selectbox(
            "Dataset",
            ["All"] + sorted(df["Dataset"].dropna().unique().tolist())
        )
        if selected_ds != "All":
            df = df[df["Dataset"] == selected_ds]

    selected_status = st.multiselect(
        "MAVA status",
        ["MATCH", "MISMATCH", "UNVERIFIED"],
        default=["MATCH", "MISMATCH", "UNVERIFIED"],
    )
    df = df[df[status_col].isin(selected_status)]

    if "Claim_Type" in df.columns:
        selected_types = st.multiselect(
            "Claim type",
            sorted(df["Claim_Type"].dropna().unique().tolist()),
            default=sorted(df["Claim_Type"].dropna().unique().tolist()),
        )
        df = df[df["Claim_Type"].isin(selected_types)]

    st.write(f"Showing **{len(df)}** claims.")

    display_cols = [
        c for c in [
            id_col, "Dataset", "Claim_Type",
            "Original_Claim_Text", "Claim_Text",
            "Validation_Status", "MAVA_Status",
            "Validation_Reason"
        ] if c and c in df.columns
    ]

    st.dataframe(
        df[display_cols] if display_cols else df,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# RESULTS
# ============================================================
elif page == "📊 Results":
    st.title("Experimental Results")

    st.subheader("1. Overall result")

    overall = pd.DataFrame({
        "System": ["Baseline", "MAVA"],
        "Hallucination Rate (%)": [80.36, 16.96],
    })

    fig = px.bar(
        overall,
        x="System",
        y="Hallucination Rate (%)",
        text_auto=".2f",
        title="Baseline vs MAVA Hallucination Rate",
    )
    fig.update_layout(yaxis_range=[0, 90], showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.success(
        "**63.39 percentage-point reduction** in hallucination rate "
        "and **78.89% relative reduction**."
    )

    st.subheader("2. Dataset-wise comparison")

    if dataset_results is not None:
        d = dataset_results[
            [
                "Dataset",
                "Baseline_Hallucination_Rate_Percent",
                "MAVA_Hallucination_Rate_Percent",
            ]
        ].copy()

        d = d.melt(
            id_vars="Dataset",
            var_name="System",
            value_name="Hallucination Rate (%)",
        )
        d["System"] = d["System"].map({
            "Baseline_Hallucination_Rate_Percent": "Baseline",
            "MAVA_Hallucination_Rate_Percent": "MAVA",
        })

        fig = px.bar(
            d,
            x="Dataset",
            y="Hallucination Rate (%)",
            color="System",
            barmode="group",
            text_auto=".2f",
            title="Dataset-wise Hallucination Rate",
        )
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(dataset_results, use_container_width=True, hide_index=True)

    st.subheader("3. Claim-type comparison")

    if claim_type_results is not None:
        ct = claim_type_results[
            [
                "Claim_Type",
                "Baseline_Hallucination_Rate_Percent",
                "MAVA_Hallucination_Rate_Percent",
            ]
        ].fillna(0)

        ct = ct.melt(
            id_vars="Claim_Type",
            var_name="System",
            value_name="Hallucination Rate (%)",
        )
        ct["System"] = ct["System"].str.replace(
            "_Hallucination_Rate_Percent", "", regex=False
        )

        fig = px.bar(
            ct,
            x="Claim_Type",
            y="Hallucination Rate (%)",
            color="System",
            barmode="group",
            text_auto=".2f",
            title="Hallucination Rate by Claim Type",
        )
        fig.update_layout(yaxis_range=[0, 110])
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("4. Validation transitions")

    if transitions is not None:
        st.dataframe(transitions, use_container_width=True, hide_index=True)

    # Display existing static thesis figures where available.
    st.subheader("Research figures")

    figure_names = [
        "fig01_mava_architecture.png",
        "fig02_overall_hallucination_rate.png",
        "fig03_dataset_hallucination_comparison.png",
        "fig04_claim_status_before_after.png",
        "fig05_claim_validation_transitions.png",
        "fig06_claim_type_hallucination_comparison.png",
    ]

    for name in figure_names:
        p = image_path(name)
        if p:
            st.image(str(p), caption=name, use_container_width=True)

# ============================================================
# CORRECTION
# ============================================================
elif page == "🛡️ Correction Agent":
    st.title("Correction Agent & Verification")

    a, b, c = st.columns(3)
    a.metric("Proposed corrections", "84")
    b.metric("Valid corrections", "71")
    c.metric("Rejected corrections", "13")

    st.write(
        "Corrections were not accepted automatically. "
        "Each proposed correction was independently verified against "
        "the frozen ground truth."
    )

    if corrections is not None:
        st.dataframe(
            corrections,
            use_container_width=True,
            hide_index=True,
        )

        if "Verification_Status" in corrections.columns:
            counts = (
                corrections["Verification_Status"]
                .value_counts()
                .rename_axis("Status")
                .reset_index(name="Count")
            )

            fig = px.pie(
                counts,
                names="Status",
                values="Count",
                title="Correction Verification",
            )
            st.plotly_chart(fig, use_container_width=True)

    st.success(
        "71 independently verified corrections were applied in the final MAVA result."
    )

# ============================================================
# AUDIT
# ============================================================
elif page == "🔎 Research Audit":
    st.title("Research Audit & Reproducibility")

    audit = pd.DataFrame([
        ["Datasets evaluated", "3"],
        ["Atomic claims", "126"],
        ["Baseline validation records", "126"],
        ["Verified corrections", "71"],
        ["Rejected corrections", "13"],
        ["Remaining mismatches", "19"],
        ["Remaining unverified", "14"],
        ["Original narratives preserved", "Yes"],
        ["Frozen ground truth preserved", "Yes"],
        ["Gemini calls during validation/correction", "0"],
        ["Previous experimental outputs overwritten", "No"],
    ], columns=["Audit Item", "Value"])

    st.dataframe(audit, use_container_width=True, hide_index=True)

    st.subheader("Key research artifacts")

    artifact_paths = [
        "claims/ALL_DATASETS_ATOMIC_CLAIMS.csv",
        "validation/mava_revalidation/FINAL_MAVA_REVALIDATION.csv",
        "final_thesis_analysis/FINAL_THESIS_OVERALL_RESULTS.csv",
        "final_thesis_analysis/FINAL_THESIS_DATASET_RESULTS.csv",
        "final_thesis_analysis/FINAL_THESIS_CLAIM_TYPE_RESULTS.csv",
        "correction_verification/CORRECTION_VERIFICATION.csv",
        "final_thesis_analysis/FINAL_THESIS_EXPERIMENT_SUMMARY.json",
    ]

    rows = []
    for rel in artifact_paths:
        p = OUTPUTS / rel
        rows.append({
            "Artifact": rel,
            "Status": "FOUND" if p.exists() else "MISSING",
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.info(
        "The Streamlit application is a presentation layer over frozen "
        "research artifacts. It does not modify the experiment."
    )

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.divider()
st.caption(
    "MAVA Research Demonstrator • Frozen experimental evidence • "
    "No live Gemini calls"
)
