"""
🎓 Student Performance Analytics Dashboard
A comprehensive web application for analyzing student academic performance.
Built with Streamlit, Pandas, Matplotlib, Seaborn, and Plotly.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
import warnings

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS STYLING
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global Styles ── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Main Background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
    }

    /* ── Sidebar Styling ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e3f 0%, #2d1b69 100%) !important;
        border-right: 1px solid rgba(139, 92, 246, 0.3);
    }

    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #e0d4f7 !important;
    }

    /* ── Metric Cards ── */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(59, 130, 246, 0.15));
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3);
    }

    [data-testid="stMetricLabel"] {
        color: #a78bfa !important;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="stMetricValue"] {
        color: #f0e6ff !important;
        font-weight: 700;
    }

    /* ── DataFrames ── */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(139, 92, 246, 0.25);
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(30, 30, 63, 0.6);
        border-radius: 12px;
        padding: 6px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        color: #a78bfa;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
        color: white !important;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.5) !important;
    }

    /* ── Download Button ── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.3) !important;
    }

    /* ── File Uploader ── */
    [data-testid="stFileUploader"] {
        background: rgba(139, 92, 246, 0.05);
        border: 2px dashed rgba(139, 92, 246, 0.4);
        border-radius: 16px;
        padding: 20px;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(139, 92, 246, 0.1);
        border-radius: 12px;
        font-weight: 600;
    }

    /* ── Section Headers ── */
    .section-header {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(59, 130, 246, 0.1));
        border-left: 4px solid #8b5cf6;
        border-radius: 0 12px 12px 0;
        padding: 16px 24px;
        margin: 20px 0;
    }

    .section-header h2 {
        margin: 0;
        color: #e0d4f7;
        font-size: 1.4rem;
    }

    /* ── Insight Cards ── */
    .insight-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(59, 130, 246, 0.1));
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }

    .insight-card-warning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(239, 68, 68, 0.1));
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
    }

    /* ── Hero Section ── */
    .hero-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(59, 130, 246, 0.1));
        border-radius: 20px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        margin-bottom: 30px;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 400;
    }

    /* ── Grade Badge ── */
    .grade-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }

    /* ── Divider ── */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #8b5cf6, transparent);
        margin: 30px 0;
        border: none;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #1a1a3e; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #8b5cf6, #6366f1);
        border-radius: 4px;
    }

    /* ── Select / Multiselect ── */
    .stSelectbox, .stMultiSelect {
        border-radius: 12px;
    }

    /* ── Slider ── */
    .stSlider [data-baseweb="slider"] [role="slider"] {
        background-color: #8b5cf6 !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────

def detect_columns(df):
    """Auto-detect relevant columns from the uploaded dataset."""
    col_mapping = {
        "id": None,
        "name": None,
        "attendance": None,
        "internal_marks": None,
        "assignment": None,
        "final_marks": None,
        "grade": None,
        "study_hours": None,
    }

    for col in df.columns:
        col_lower = col.lower().replace(" ", "_").replace("-", "_")
        if any(k in col_lower for k in ["student_id", "stu_id", "id", "roll"]):
            col_mapping["id"] = col
        elif any(k in col_lower for k in ["student_name", "name"]):
            col_mapping["name"] = col
        elif any(k in col_lower for k in ["attendance", "attend"]):
            col_mapping["attendance"] = col
        elif any(k in col_lower for k in ["internal", "mid_term", "midterm", "sessional"]):
            col_mapping["internal_marks"] = col
        elif any(k in col_lower for k in ["assignment", "homework", "project_score"]):
            col_mapping["assignment"] = col
        elif any(k in col_lower for k in ["final_exam", "final_mark", "exam_mark", "total_mark"]):
            col_mapping["final_marks"] = col
        elif any(k in col_lower for k in ["grade"]):
            col_mapping["grade"] = col
        elif any(k in col_lower for k in ["study_hour", "hours"]):
            col_mapping["study_hours"] = col

    return col_mapping


def generate_insights(df, col_map):
    """Generate automatic insights from the data."""
    insights = []
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Attendance vs Final Marks correlation
    if col_map["attendance"] and col_map["final_marks"]:
        corr = df[col_map["attendance"]].corr(df[col_map["final_marks"]])
        if corr > 0.5:
            insights.append({
                "icon": "📈",
                "title": "Attendance Drives Performance",
                "text": f"Strong positive correlation ({corr:.2f}) between attendance and final marks. Students with higher attendance tend to score significantly better.",
                "type": "positive"
            })
        elif corr > 0.3:
            insights.append({
                "icon": "📊",
                "title": "Moderate Attendance Impact",
                "text": f"Moderate positive correlation ({corr:.2f}) between attendance and final marks. Attending classes provides a measurable advantage.",
                "type": "positive"
            })
        else:
            insights.append({
                "icon": "⚠️",
                "title": "Weak Attendance Correlation",
                "text": f"Weak correlation ({corr:.2f}) between attendance and final marks. Other factors may be more influential.",
                "type": "warning"
            })

    # Assignment vs Final Marks
    if col_map["assignment"] and col_map["final_marks"]:
        corr = df[col_map["assignment"]].corr(df[col_map["final_marks"]])
        if corr > 0.5:
            insights.append({
                "icon": "📝",
                "title": "Assignments Strongly Influence Results",
                "text": f"Strong correlation ({corr:.2f}) between assignment scores and final exam marks. Consistent assignment completion is a key predictor of success.",
                "type": "positive"
            })
        elif corr > 0.3:
            insights.append({
                "icon": "📋",
                "title": "Assignments Moderately Linked to Outcomes",
                "text": f"Moderate correlation ({corr:.2f}) between assignments and final marks. Regular practice through assignments helps build exam readiness.",
                "type": "positive"
            })

    # Internal Marks vs Final Marks
    if col_map["internal_marks"] and col_map["final_marks"]:
        corr = df[col_map["internal_marks"]].corr(df[col_map["final_marks"]])
        if corr > 0.5:
            insights.append({
                "icon": "🎯",
                "title": "Internal Assessments Predict Final Performance",
                "text": f"Strong correlation ({corr:.2f}) between internal marks and final exam scores. Internal assessments are reliable predictors.",
                "type": "positive"
            })

    # Study Hours impact
    if col_map["study_hours"] and col_map["final_marks"]:
        corr = df[col_map["study_hours"]].corr(df[col_map["final_marks"]])
        if corr > 0.4:
            insights.append({
                "icon": "⏰",
                "title": "Study Hours Pay Off",
                "text": f"Positive correlation ({corr:.2f}) between weekly study hours and final marks. More dedicated study time translates to better outcomes.",
                "type": "positive"
            })

    # Low attendance students
    if col_map["attendance"] and col_map["final_marks"]:
        low_attend = df[df[col_map["attendance"]] < 60]
        if len(low_attend) > 0:
            avg_low = low_attend[col_map["final_marks"]].mean()
            avg_all = df[col_map["final_marks"]].mean()
            insights.append({
                "icon": "🚨",
                "title": f"{len(low_attend)} Students with Low Attendance (<60%)",
                "text": f"These students average {avg_low:.1f} marks vs class average of {avg_all:.1f}. Early intervention recommended.",
                "type": "warning"
            })

    # Top performers
    if col_map["final_marks"]:
        top_pct = df[col_map["final_marks"]].quantile(0.9)
        top_students = df[df[col_map["final_marks"]] >= top_pct]
        insights.append({
            "icon": "🏆",
            "title": f"Top 10% Score Above {top_pct:.0f} Marks",
            "text": f"{len(top_students)} students are in the top tier. Their average attendance is "
                    + (f"{top_students[col_map['attendance']].mean():.1f}%" if col_map["attendance"] else "N/A")
                    + ".",
            "type": "positive"
        })

    # Grade distribution insight
    if col_map["grade"]:
        grade_counts = df[col_map["grade"]].value_counts()
        most_common = grade_counts.index[0]
        insights.append({
            "icon": "📊",
            "title": f"Most Common Grade: {most_common}",
            "text": f"{grade_counts.iloc[0]} students ({grade_counts.iloc[0]/len(df)*100:.1f}%) received grade {most_common}. "
                    + f"Grade distribution spans from {grade_counts.index[-1]} to {grade_counts.index[0]}.",
            "type": "positive"
        })

    # Failing students
    if col_map["final_marks"]:
        fail_threshold = 40
        failing = df[df[col_map["final_marks"]] < fail_threshold]
        if len(failing) > 0:
            insights.append({
                "icon": "⚠️",
                "title": f"{len(failing)} Students At Risk of Failing",
                "text": f"{len(failing)} students scored below {fail_threshold} marks. These students need immediate academic support and mentoring.",
                "type": "warning"
            })

    return insights


def create_pdf_report(df, col_map, insights):
    """Generate a PDF report of the analytics."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 60, "", ln=True)
    pdf.cell(0, 15, "Student Performance", ln=True, align="C")
    pdf.cell(0, 15, "Analytics Report", ln=True, align="C")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 20, "", ln=True)
    pdf.cell(0, 10, f"Total Students: {len(df)}", ln=True, align="C")
    pdf.cell(0, 10, f"Generated by Student Analytics Dashboard", ln=True, align="C")

    # Statistics Page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, "Descriptive Statistics", ln=True)
    pdf.set_font("Helvetica", "", 10)

    numeric_df = df.select_dtypes(include=[np.number])
    stats = numeric_df.describe().round(2)

    # Table header
    pdf.set_font("Helvetica", "B", 9)
    col_width = (pdf.w - 30) / (len(stats.columns) + 1)
    pdf.cell(col_width, 8, "Statistic", border=1, align="C")
    for col in stats.columns:
        display_name = col[:12] if len(col) > 12 else col
        pdf.cell(col_width, 8, display_name, border=1, align="C")
    pdf.ln()

    # Table rows
    pdf.set_font("Helvetica", "", 8)
    for idx in stats.index:
        pdf.cell(col_width, 8, str(idx), border=1, align="C")
        for col in stats.columns:
            pdf.cell(col_width, 8, str(stats.loc[idx, col]), border=1, align="C")
        pdf.ln()

    # Insights Page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, "Key Insights", ln=True)
    pdf.ln(5)

    for insight in insights:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, f"{insight['icon']} {insight['title']}", ln=True)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, insight["text"])
        pdf.ln(5)

    return pdf.output()


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px 0 10px 0;">
        <span style="font-size: 3rem;">🎓</span>
        <h2 style="margin: 5px 0; background: linear-gradient(135deg, #8b5cf6, #06b6d4);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 800;">Student Analytics</h2>
        <p style="color: #94a3b8; font-size: 0.85rem;">Performance Dashboard v2.0</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Navigation
    page = st.radio(
        "📍 Navigation",
        ["🏠 Home", "📤 Upload Data", "📊 Statistics", "📈 Visualizations",
         "🔍 Correlation Analysis", "💡 Insights", "🎯 Predict & Filter"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Dataset info
    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df
        st.markdown("### 📁 Dataset Info")
        st.markdown(f"**Rows:** {len(df)}")
        st.markdown(f"**Columns:** {len(df.columns)}")
        st.markdown(f"**Numeric Cols:** {len(df.select_dtypes(include=[np.number]).columns)}")

        # Quick filter
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown("### ⚙️ Quick Settings")
        st.session_state.theme = st.selectbox(
            "Chart Theme",
            ["plotly_dark", "plotly", "ggplot2", "seaborn"],
            index=0
        )
    else:
        st.info("📤 Upload a CSV to get started!")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 10px; color: #64748b; font-size: 0.75rem;">
        Built with ❤️ using Streamlit<br>
        © 2026 Student Analytics
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# INITIALIZE SESSION STATE
# ─────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = None
if "col_map" not in st.session_state:
    st.session_state.col_map = None
if "theme" not in st.session_state:
    st.session_state.theme = "plotly_dark"


# ─────────────────────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">🎓 Student Performance Analytics</div>
        <div class="hero-subtitle">
            Upload your student data and unlock powerful insights with advanced analytics,
            beautiful visualizations, and predictive modeling.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="text-align:center; padding: 30px 15px;
            background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(139,92,246,0.05));
            border: 1px solid rgba(139,92,246,0.2); border-radius: 16px;">
            <div style="font-size: 2.5rem;">📤</div>
            <h4 style="color: #e0d4f7;">Upload</h4>
            <p style="color: #94a3b8; font-size: 0.85rem;">Import CSV datasets with student records</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align:center; padding: 30px 15px;
            background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(59,130,246,0.05));
            border: 1px solid rgba(59,130,246,0.2); border-radius: 16px;">
            <div style="font-size: 2.5rem;">📊</div>
            <h4 style="color: #e0d4f7;">Analyze</h4>
            <p style="color: #94a3b8; font-size: 0.85rem;">Statistical analysis & correlation matrices</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align:center; padding: 30px 15px;
            background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(16,185,129,0.05));
            border: 1px solid rgba(16,185,129,0.2); border-radius: 16px;">
            <div style="font-size: 2.5rem;">📈</div>
            <h4 style="color: #e0d4f7;">Visualize</h4>
            <p style="color: #94a3b8; font-size: 0.85rem;">Interactive charts & heatmaps</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="text-align:center; padding: 30px 15px;
            background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(245,158,11,0.05));
            border: 1px solid rgba(245,158,11,0.2); border-radius: 16px;">
            <div style="font-size: 2.5rem;">💡</div>
            <h4 style="color: #e0d4f7;">Insights</h4>
            <p style="color: #94a3b8; font-size: 0.85rem;">Auto-generated insights & predictions</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    ### 🚀 Getting Started
    1. **Navigate to Upload Data** from the sidebar
    2. Upload a CSV file or use the sample dataset
    3. Explore statistics, visualizations, and insights
    
    ### 📋 Expected Dataset Columns
    | Column | Description | Example |
    |--------|-------------|---------|
    | Student ID | Unique identifier | STU0001 |
    | Student Name | Full name | Aarav Sharma |
    | Attendance (%) | Class attendance percentage | 82.5 |
    | Internal Marks | Mid-term / sessional marks | 38 |
    | Assignment Score | Homework / project scores | 75 |
    | Final Exam Marks | End-term exam marks | 68 |
    | Grade | Letter grade (optional) | B+ |
    """)


# ─────────────────────────────────────────────────────────────
# PAGE: UPLOAD DATA
# ─────────────────────────────────────────────────────────────
elif page == "📤 Upload Data":
    st.markdown("""
    <div class="section-header">
        <h2>📤 Data Upload Center</h2>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📁 Upload CSV", "📦 Use Sample Data"])

    with tab1:
        uploaded_file = st.file_uploader(
            "Drag and drop your CSV file here",
            type=["csv"],
            help="Upload a CSV file containing student performance data"
        )

        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.session_state.col_map = detect_columns(df)
                st.success(f"✅ Successfully loaded **{len(df)}** records with **{len(df.columns)}** columns!")
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")

    with tab2:
        st.markdown("Don't have a dataset? Use our pre-generated sample data with 150 students.")
        if st.button("🎲 Load Sample Dataset", use_container_width=True):
            try:
                df = pd.read_csv("sample_student_data.csv")
                st.session_state.df = df
                st.session_state.col_map = detect_columns(df)
                st.success(f"✅ Sample dataset loaded! **{len(df)}** students ready for analysis.")
            except FileNotFoundError:
                st.error("❌ Sample dataset not found. Please run `python generate_sample_data.py` first.")

    # Show preview if data loaded
    if st.session_state.df is not None:
        df = st.session_state.df
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        st.markdown("### 👀 Dataset Preview (First 10 Rows)")
        st.dataframe(
            df.head(10),
            use_container_width=True,
            height=400
        )

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📐 Dataset Shape")
            st.metric("Total Rows", len(df))
            st.metric("Total Columns", len(df.columns))
        with col2:
            st.markdown("### 🔤 Column Types")
            dtype_df = pd.DataFrame({
                "Column": df.columns,
                "Type": df.dtypes.astype(str).values,
                "Non-Null Count": df.count().values,
                "Null Count": df.isnull().sum().values
            })
            st.dataframe(dtype_df, use_container_width=True, hide_index=True)

        # Column mapping review
        with st.expander("🔧 Auto-Detected Column Mapping"):
            col_map = st.session_state.col_map
            for key, val in col_map.items():
                st.markdown(f"**{key.replace('_', ' ').title()}:** {val if val else '❌ Not detected'}")


# ─────────────────────────────────────────────────────────────
# PAGE: STATISTICS
# ─────────────────────────────────────────────────────────────
elif page == "📊 Statistics":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()

    df = st.session_state.df
    col_map = st.session_state.col_map

    st.markdown("""
    <div class="section-header">
        <h2>📊 Descriptive Statistics</h2>
    </div>
    """, unsafe_allow_html=True)

    # Quick metric cards
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if col_map["final_marks"]:
        col1, col2, col3, col4, col5 = st.columns(5)
        fm = df[col_map["final_marks"]]
        with col1:
            st.metric("📊 Mean", f"{fm.mean():.1f}")
        with col2:
            st.metric("📍 Median", f"{fm.median():.1f}")
        with col3:
            st.metric("📏 Std Dev", f"{fm.std():.1f}")
        with col4:
            st.metric("🔺 Max", f"{fm.max():.0f}")
        with col5:
            st.metric("🔻 Min", f"{fm.min():.0f}")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Full statistics table
    st.markdown("### 📋 Complete Statistical Summary")

    stats_df = df[numeric_cols].describe().T
    stats_df["variance"] = df[numeric_cols].var()
    stats_df["skewness"] = df[numeric_cols].skew()
    stats_df["kurtosis"] = df[numeric_cols].kurtosis()

    stats_df = stats_df.round(2)
    stats_df.columns = ["Count", "Mean", "Std Dev", "Min", "25th %ile",
                         "Median", "75th %ile", "Max", "Variance", "Skewness", "Kurtosis"]

    st.dataframe(
        stats_df.style.background_gradient(cmap="RdYlGn", subset=["Mean", "Median"]),
        use_container_width=True,
        height=300
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Per-column deep dive
    st.markdown("### 🔬 Column Deep Dive")
    selected_col = st.selectbox("Select a numeric column:", numeric_cols)

    if selected_col:
        col1, col2 = st.columns(2)

        with col1:
            # Distribution plot
            fig = px.histogram(
                df, x=selected_col, nbins=25,
                title=f"Distribution of {selected_col}",
                template=st.session_state.theme,
                color_discrete_sequence=["#8b5cf6"],
                marginal="box"
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e0d4f7"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Violin plot
            fig = px.violin(
                df, y=selected_col,
                title=f"Violin Plot of {selected_col}",
                template=st.session_state.theme,
                color_discrete_sequence=["#06b6d4"],
                box=True, points="all"
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e0d4f7"
            )
            st.plotly_chart(fig, use_container_width=True)

    # Grade distribution
    if col_map["grade"]:
        st.markdown("### 🎯 Grade Distribution")
        grade_counts = df[col_map["grade"]].value_counts().reset_index()
        grade_counts.columns = ["Grade", "Count"]

        grade_order = ["A+", "A", "B+", "B", "C", "D", "F"]
        grade_counts["Grade"] = pd.Categorical(grade_counts["Grade"], categories=grade_order, ordered=True)
        grade_counts = grade_counts.sort_values("Grade")

        colors = ["#10b981", "#34d399", "#60a5fa", "#818cf8", "#f59e0b", "#f97316", "#ef4444"]

        fig = px.bar(
            grade_counts, x="Grade", y="Count",
            title="Grade Distribution",
            template=st.session_state.theme,
            color="Grade",
            color_discrete_sequence=colors
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e0d4f7",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: VISUALIZATIONS
# ─────────────────────────────────────────────────────────────
elif page == "📈 Visualizations":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()

    df = st.session_state.df
    col_map = st.session_state.col_map
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.markdown("""
    <div class="section-header">
        <h2>📈 Interactive Visualizations</h2>
    </div>
    """, unsafe_allow_html=True)

    viz_tab1, viz_tab2, viz_tab3, viz_tab4 = st.tabs([
        "🔵 Scatter Plots", "📦 Box Plots", "📊 Histograms", "🌡️ Heatmap"
    ])

    # ── Scatter Plots ──
    with viz_tab1:
        st.markdown("### 🔵 Scatter Plot Analysis")
        col1, col2 = st.columns(2)

        with col1:
            x_col = st.selectbox("X-Axis:", numeric_cols, index=0, key="scatter_x")
        with col2:
            default_y = numeric_cols.index(col_map["final_marks"]) if col_map["final_marks"] in numeric_cols else min(1, len(numeric_cols)-1)
            y_col = st.selectbox("Y-Axis:", numeric_cols, index=default_y, key="scatter_y")

        color_col = None
        if col_map["grade"]:
            color_col = col_map["grade"]

        fig = px.scatter(
            df, x=x_col, y=y_col,
            color=color_col,
            hover_data=[col_map["name"]] if col_map["name"] else None,
            title=f"{x_col} vs {y_col}",
            template=st.session_state.theme,
            trendline="ols",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig.update_traces(marker=dict(size=10, opacity=0.7, line=dict(width=1, color="#1a1a3e")))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e0d4f7",
            height=550
        )
        st.plotly_chart(fig, use_container_width=True)

        # Correlation stat
        corr_val = df[x_col].corr(df[y_col])
        corr_color = "#10b981" if abs(corr_val) > 0.5 else "#f59e0b" if abs(corr_val) > 0.3 else "#ef4444"
        st.markdown(f"""
        <div style="text-align:center; padding: 15px;
            background: rgba(139,92,246,0.1); border-radius: 12px;
            border: 1px solid rgba(139,92,246,0.2);">
            <span style="color: #94a3b8;">Pearson Correlation:</span>
            <span style="color: {corr_color}; font-size: 1.5rem; font-weight: 700;"> {corr_val:.3f}</span>
            <span style="color: #94a3b8;"> — {'Strong' if abs(corr_val) > 0.5 else 'Moderate' if abs(corr_val) > 0.3 else 'Weak'} relationship</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Box Plots ──
    with viz_tab2:
        st.markdown("### 📦 Box Plot - Marks Distribution")

        selected_box_cols = st.multiselect(
            "Select columns for box plot:",
            numeric_cols,
            default=numeric_cols[:4]
        )

        if selected_box_cols:
            fig = go.Figure()
            colors = ["#8b5cf6", "#06b6d4", "#10b981", "#f59e0b", "#ef4444", "#ec4899"]

            for i, col in enumerate(selected_box_cols):
                fig.add_trace(go.Box(
                    y=df[col], name=col,
                    marker_color=colors[i % len(colors)],
                    boxmean='sd'
                ))

            fig.update_layout(
                title="Score Distribution Comparison",
                template=st.session_state.theme,
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e0d4f7",
                height=550
            )
            st.plotly_chart(fig, use_container_width=True)

        # Box plot by grade
        if col_map["grade"] and col_map["final_marks"]:
            st.markdown("### 📦 Final Marks by Grade")
            fig = px.box(
                df, x=col_map["grade"], y=col_map["final_marks"],
                color=col_map["grade"],
                title="Final Marks Distribution by Grade",
                template=st.session_state.theme,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e0d4f7",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── Histograms ──
    with viz_tab3:
        st.markdown("### 📊 Score Frequency Histograms")

        hist_col = st.selectbox("Select column:", numeric_cols, key="hist_col")
        n_bins = st.slider("Number of bins:", 10, 50, 25)

        fig = px.histogram(
            df, x=hist_col, nbins=n_bins,
            title=f"Frequency Distribution of {hist_col}",
            template=st.session_state.theme,
            color_discrete_sequence=["#8b5cf6"],
            marginal="rug"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e0d4f7",
            height=500,
            bargap=0.05
        )
        st.plotly_chart(fig, use_container_width=True)

        # Overlaid histograms
        if len(numeric_cols) >= 2:
            st.markdown("### 📊 Overlaid Distributions")
            multi_cols = st.multiselect(
                "Compare distributions:",
                numeric_cols,
                default=numeric_cols[:3],
                key="multi_hist"
            )
            if multi_cols:
                fig = go.Figure()
                colors = ["#8b5cf6", "#06b6d4", "#10b981", "#f59e0b", "#ef4444"]
                for i, col in enumerate(multi_cols):
                    fig.add_trace(go.Histogram(
                        x=df[col], name=col, opacity=0.6,
                        marker_color=colors[i % len(colors)]
                    ))
                fig.update_layout(
                    barmode="overlay",
                    title="Overlaid Score Distributions",
                    template=st.session_state.theme,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#e0d4f7",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)

    # ── Heatmap ──
    with viz_tab4:
        st.markdown("### 🌡️ Correlation Heatmap")

        corr_matrix = df[numeric_cols].corr().round(3)

        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix Heatmap",
            template=st.session_state.theme,
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e0d4f7",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

        # Seaborn static heatmap
        with st.expander("🎨 Static Heatmap (Seaborn)"):
            fig_sns, ax = plt.subplots(figsize=(10, 8))
            fig_sns.patch.set_facecolor("#1a1a3e")
            ax.set_facecolor("#1a1a3e")

            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            sns.heatmap(
                corr_matrix, mask=mask, annot=True, fmt=".2f",
                cmap="coolwarm", center=0, square=True,
                linewidths=2, linecolor="#2d1b69",
                cbar_kws={"shrink": 0.8},
                annot_kws={"color": "white", "fontsize": 10}
            )
            ax.tick_params(colors="#e0d4f7")
            plt.title("Correlation Matrix (Lower Triangle)", color="#e0d4f7", fontsize=14, pad=15)
            st.pyplot(fig_sns)
            plt.close()


# ─────────────────────────────────────────────────────────────
# PAGE: CORRELATION ANALYSIS
# ─────────────────────────────────────────────────────────────
elif page == "🔍 Correlation Analysis":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()

    df = st.session_state.df
    col_map = st.session_state.col_map
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.markdown("""
    <div class="section-header">
        <h2>🔍 Correlation Analysis</h2>
    </div>
    """, unsafe_allow_html=True)

    # Correlation Matrix Table
    st.markdown("### 📊 Correlation Matrix")
    corr_matrix = df[numeric_cols].corr().round(3)
    st.dataframe(
        corr_matrix.style.background_gradient(cmap="RdBu_r", vmin=-1, vmax=1),
        use_container_width=True
    )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Key Relationship Highlights
    st.markdown("### 🔗 Key Relationships")

    relationships = []

    if col_map["attendance"] and col_map["final_marks"]:
        relationships.append(("Attendance", col_map["attendance"], "Final Marks", col_map["final_marks"]))
    if col_map["assignment"] and col_map["final_marks"]:
        relationships.append(("Assignments", col_map["assignment"], "Final Marks", col_map["final_marks"]))
    if col_map["internal_marks"] and col_map["final_marks"]:
        relationships.append(("Internal Marks", col_map["internal_marks"], "Final Marks", col_map["final_marks"]))
    if col_map["study_hours"] and col_map["final_marks"]:
        relationships.append(("Study Hours", col_map["study_hours"], "Final Marks", col_map["final_marks"]))

    if relationships:
        cols = st.columns(len(relationships))
        for i, (label1, c1, label2, c2) in enumerate(relationships):
            corr_val = df[c1].corr(df[c2])
            strength = "Strong ✅" if abs(corr_val) > 0.5 else "Moderate 🟡" if abs(corr_val) > 0.3 else "Weak 🔴"
            with cols[i]:
                st.markdown(f"""
                <div style="text-align:center; padding: 20px;
                    background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(59,130,246,0.1));
                    border: 1px solid rgba(139,92,246,0.2); border-radius: 16px;">
                    <div style="font-size: 2rem; margin-bottom: 5px;">
                        {"📈" if corr_val > 0 else "📉"}
                    </div>
                    <div style="color: #a78bfa; font-size: 0.85rem; font-weight: 600;">
                        {label1} vs {label2}
                    </div>
                    <div style="color: #f0e6ff; font-size: 1.8rem; font-weight: 800; margin: 5px 0;">
                        {corr_val:.3f}
                    </div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">{strength}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

        # Detailed scatter plots for key relationships
        st.markdown("### 📈 Relationship Scatter Plots")
        for label1, c1, label2, c2 in relationships:
            col_l, col_r = st.columns([3, 1])
            with col_l:
                fig = px.scatter(
                    df, x=c1, y=c2,
                    title=f"{label1} vs {label2}",
                    template=st.session_state.theme,
                    trendline="ols",
                    color_discrete_sequence=["#8b5cf6"]
                )
                fig.update_traces(marker=dict(size=8, opacity=0.6))
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#e0d4f7",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            with col_r:
                corr_val = df[c1].corr(df[c2])
                st.markdown(f"""
                <div style="padding: 30px 15px; text-align:center; margin-top: 50px;">
                    <div style="color: #a78bfa; font-weight: 600;">Correlation</div>
                    <div style="font-size: 2.5rem; font-weight: 800;
                        color: {'#10b981' if corr_val > 0.5 else '#f59e0b' if corr_val > 0.3 else '#ef4444'};">
                        {corr_val:.3f}
                    </div>
                    <div style="color: #94a3b8; margin-top: 10px; font-size: 0.85rem;">
                        {"This indicates a strong positive relationship. Improving {0} is likely to boost {1}."
                         .format(label1.lower(), label2.lower()) if corr_val > 0.5
                         else "Moderate relationship detected. There are other influencing factors."
                         if corr_val > 0.3
                         else "Weak relationship. Other factors dominate."}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Unable to identify key relationships. Please ensure your dataset has the expected columns.")

    # Pair plot
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 🔢 Pairwise Relationships")
    pair_cols = st.multiselect(
        "Select columns for pair plot:",
        numeric_cols,
        default=numeric_cols[:4],
        key="pair_plot_cols"
    )
    if pair_cols and len(pair_cols) >= 2:
        fig = px.scatter_matrix(
            df, dimensions=pair_cols,
            color=col_map["grade"] if col_map["grade"] else None,
            title="Scatter Matrix",
            template=st.session_state.theme,
            opacity=0.6
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#e0d4f7",
            height=700
        )
        st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# PAGE: INSIGHTS
# ─────────────────────────────────────────────────────────────
elif page == "💡 Insights":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()

    df = st.session_state.df
    col_map = st.session_state.col_map

    st.markdown("""
    <div class="section-header">
        <h2>💡 Automated Insights & Recommendations</h2>
    </div>
    """, unsafe_allow_html=True)

    insights = generate_insights(df, col_map)

    # Positive insights
    positive_insights = [i for i in insights if i["type"] == "positive"]
    warning_insights = [i for i in insights if i["type"] == "warning"]

    if positive_insights:
        st.markdown("### ✅ Positive Findings")
        for insight in positive_insights:
            st.markdown(f"""
            <div class="insight-card">
                <h4 style="color: #10b981; margin: 0 0 8px 0;">
                    {insight["icon"]} {insight["title"]}
                </h4>
                <p style="color: #cbd5e1; margin: 0; line-height: 1.6;">
                    {insight["text"]}
                </p>
            </div>
            """, unsafe_allow_html=True)

    if warning_insights:
        st.markdown("### ⚠️ Areas of Concern")
        for insight in warning_insights:
            st.markdown(f"""
            <div class="insight-card-warning">
                <h4 style="color: #f59e0b; margin: 0 0 8px 0;">
                    {insight["icon"]} {insight["title"]}
                </h4>
                <p style="color: #cbd5e1; margin: 0; line-height: 1.6;">
                    {insight["text"]}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Recommendations
    st.markdown("### 🎯 Recommendations")

    recommendations = [
        ("🏫", "Attendance Monitoring", "Implement attendance tracking alerts for students falling below 70%. Early intervention can improve outcomes significantly."),
        ("📝", "Assignment Strategy", "Encourage consistent assignment completion. Create study groups for students struggling with assignments."),
        ("📖", "Study Hours", "Recommend minimum study hours based on performance data. Students averaging above median marks typically study 15+ hours/week."),
        ("🤝", "Peer Mentoring", "Pair high-performing students with at-risk students. Peer learning has shown strong positive effects on academic outcomes."),
        ("📊", "Regular Assessment", "Increase frequency of low-stakes assessments to identify knowledge gaps early in the semester."),
    ]

    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(recommendations):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="padding: 20px; margin: 8px 0;
                background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.05));
                border: 1px solid rgba(99,102,241,0.2); border-radius: 14px;">
                <div style="font-size: 1.5rem; margin-bottom: 5px;">{icon}</div>
                <h4 style="color: #a78bfa; margin: 0 0 5px 0;">{title}</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Download Report
    st.markdown("### 📥 Export Report")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📄 Generate PDF Report", use_container_width=True):
            try:
                pdf_bytes = create_pdf_report(df, col_map, insights)
                st.session_state.pdf_report = pdf_bytes
                st.success("✅ Report generated successfully!")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

        if "pdf_report" in st.session_state:
            st.download_button(
                "⬇️ Download PDF Report",
                data=st.session_state.pdf_report,
                file_name="student_performance_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    with col2:
        # CSV export
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Data as CSV",
            data=csv,
            file_name="student_data_export.csv",
            mime="text/csv",
            use_container_width=True
        )


# ─────────────────────────────────────────────────────────────
# PAGE: PREDICT & FILTER
# ─────────────────────────────────────────────────────────────
elif page == "🎯 Predict & Filter":
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()

    df = st.session_state.df
    col_map = st.session_state.col_map
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    st.markdown("""
    <div class="section-header">
        <h2>🎯 Predict & Filter Students</h2>
    </div>
    """, unsafe_allow_html=True)

    pred_tab, filter_tab = st.tabs(["🔮 Grade Prediction", "🔎 Filter Students"])

    # ── Grade Prediction ──
    with pred_tab:
        st.markdown("### 🔮 Predict Final Marks Using Linear Regression")

        if col_map["final_marks"]:
            from sklearn.linear_model import LinearRegression
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import r2_score, mean_absolute_error

            # Select features
            feature_cols = [c for c in numeric_cols if c != col_map["final_marks"]]
            selected_features = st.multiselect(
                "Select predictor features:",
                feature_cols,
                default=feature_cols[:3]
            )

            if selected_features and len(selected_features) >= 1:
                # Train model
                X = df[selected_features].dropna()
                y = df.loc[X.index, col_map["final_marks"]]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                model = LinearRegression()
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)
                r2 = r2_score(y_test, y_pred)
                mae = mean_absolute_error(y_test, y_pred)

                # Model metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("R² Score", f"{r2:.3f}")
                with col2:
                    st.metric("Mean Abs Error", f"{mae:.2f}")
                with col3:
                    st.metric("Features Used", len(selected_features))

                # Feature importance
                st.markdown("#### 📊 Feature Coefficients")
                coef_df = pd.DataFrame({
                    "Feature": selected_features,
                    "Coefficient": model.coef_.round(3),
                    "Abs Impact": np.abs(model.coef_).round(3)
                }).sort_values("Abs Impact", ascending=False)

                fig = px.bar(
                    coef_df, x="Feature", y="Coefficient",
                    title="Feature Importance (Regression Coefficients)",
                    template=st.session_state.theme,
                    color="Coefficient",
                    color_continuous_scale="RdBu_r"
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#e0d4f7",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

                # Prediction vs Actual
                fig = px.scatter(
                    x=y_test, y=y_pred,
                    labels={"x": "Actual Marks", "y": "Predicted Marks"},
                    title="Predicted vs Actual Final Marks",
                    template=st.session_state.theme,
                    color_discrete_sequence=["#8b5cf6"]
                )
                fig.add_trace(go.Scatter(
                    x=[y_test.min(), y_test.max()],
                    y=[y_test.min(), y_test.max()],
                    mode="lines",
                    name="Perfect Prediction",
                    line=dict(color="#10b981", dash="dash", width=2)
                ))
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#e0d4f7",
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)

                # Manual prediction
                st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
                st.markdown("### 🎮 Try Manual Prediction")
                st.markdown("Enter values to predict a student's final marks:")

                input_cols = st.columns(len(selected_features))
                input_vals = {}
                for i, feat in enumerate(selected_features):
                    with input_cols[i]:
                        input_vals[feat] = st.number_input(
                            feat, value=float(df[feat].mean()),
                            min_value=float(df[feat].min()),
                            max_value=float(df[feat].max()),
                            step=1.0
                        )

                if st.button("🔮 Predict Final Marks", use_container_width=True):
                    input_df = pd.DataFrame([input_vals])
                    prediction = model.predict(input_df)[0]
                    prediction = np.clip(prediction, 0, 100)

                    # Assign grade
                    if prediction >= 90:
                        grade, grade_color = "A+", "#10b981"
                    elif prediction >= 80:
                        grade, grade_color = "A", "#34d399"
                    elif prediction >= 70:
                        grade, grade_color = "B+", "#60a5fa"
                    elif prediction >= 60:
                        grade, grade_color = "B", "#818cf8"
                    elif prediction >= 50:
                        grade, grade_color = "C", "#f59e0b"
                    elif prediction >= 40:
                        grade, grade_color = "D", "#f97316"
                    else:
                        grade, grade_color = "F", "#ef4444"

                    st.markdown(f"""
                    <div style="text-align:center; padding: 30px;
                        background: linear-gradient(135deg, rgba(139,92,246,0.15), rgba(59,130,246,0.1));
                        border: 1px solid rgba(139,92,246,0.3); border-radius: 20px; margin: 20px 0;">
                        <div style="color: #94a3b8; font-size: 1rem;">Predicted Final Marks</div>
                        <div style="font-size: 3.5rem; font-weight: 800; color: #f0e6ff;">
                            {prediction:.1f}
                        </div>
                        <div style="display:inline-block; padding: 6px 20px; border-radius: 20px;
                            background: {grade_color}; color: white; font-weight: 700; font-size: 1.2rem;">
                            Grade: {grade}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Final marks column not detected. Please ensure your dataset includes a final exam marks column.")

    # ── Filter Students ──
    with filter_tab:
        st.markdown("### 🔎 Filter & Search Students")

        col1, col2 = st.columns(2)

        with col1:
            if col_map["final_marks"]:
                marks_range = st.slider(
                    "Final Marks Range:",
                    min_value=int(df[col_map["final_marks"]].min()),
                    max_value=int(df[col_map["final_marks"]].max()),
                    value=(int(df[col_map["final_marks"]].min()), int(df[col_map["final_marks"]].max()))
                )

        with col2:
            if col_map["attendance"]:
                attend_range = st.slider(
                    "Attendance Range (%):",
                    min_value=int(df[col_map["attendance"]].min()),
                    max_value=int(df[col_map["attendance"]].max()),
                    value=(int(df[col_map["attendance"]].min()), int(df[col_map["attendance"]].max()))
                )

        # Grade filter
        if col_map["grade"]:
            selected_grades = st.multiselect(
                "Filter by Grade:",
                options=sorted(df[col_map["grade"]].unique()),
                default=sorted(df[col_map["grade"]].unique())
            )

        # Apply filters
        filtered_df = df.copy()

        if col_map["final_marks"]:
            filtered_df = filtered_df[
                (filtered_df[col_map["final_marks"]] >= marks_range[0]) &
                (filtered_df[col_map["final_marks"]] <= marks_range[1])
            ]

        if col_map["attendance"]:
            filtered_df = filtered_df[
                (filtered_df[col_map["attendance"]] >= attend_range[0]) &
                (filtered_df[col_map["attendance"]] <= attend_range[1])
            ]

        if col_map["grade"] and selected_grades:
            filtered_df = filtered_df[filtered_df[col_map["grade"]].isin(selected_grades)]

        # Search by name
        if col_map["name"]:
            search_name = st.text_input("🔍 Search by student name:")
            if search_name:
                filtered_df = filtered_df[
                    filtered_df[col_map["name"]].str.contains(search_name, case=False, na=False)
                ]

        # Results
        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} students**")
        st.dataframe(filtered_df, use_container_width=True, height=500)

        # Export filtered data
        if len(filtered_df) > 0:
            csv = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download Filtered Data",
                data=csv,
                file_name="filtered_students.csv",
                mime="text/csv",
                use_container_width=True
            )
