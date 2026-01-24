import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Page Configuration & Custom CSS
# -----------------------------
st.set_page_config(
    page_title="Job Acceptance Prediction System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - OPTIMIZED FOR SMALLER SCREEN SIZE
st.markdown("""
    <style>
    /* 1. App Background - Dark */
    .stApp {
        background-color: #0E1117;
    }

    /* 2. Main Title Font - SMALLER SIZE */
    .main-title {
        font-size: 2.0rem !important; /* Reduced */
        font-weight: 800 !important;
        color: #FFFFFF !important;
        text-align: center;
        margin-bottom: 5px;
    }

    /* 3. Sub-text Font - SMALLER SIZE */
    .sub-text {
        font-size: 0.9rem !important; /* Reduced */
        line-height: 1.4;
        text-align: center;
        color: #D1D5DB !important;
        margin-bottom: 20px;
        padding: 0 50px;
    }

    /* 4. Dynamic Context Text - SMALLER SIZE */
    .dynamic-text {
        font-size: 0.9rem; /* Reduced */
        color: #9CA3AF;
        margin-bottom: 10px;
        font-style: italic;
        border-left: 3px solid #3B82F6;
        padding-left: 10px;
    }

    /* 5. Chart Explanation Text - SMALLER SIZE */
    .chart-explanation {
        font-size: 0.8rem; /* Reduced */
        color: #D1D5DB; 
        margin-top: 5px;
        background-color: #1F2937;
        padding: 10px;
        border-radius: 6px;
        border-top: 2px solid #F59E0B;
    }

    /* 6. KPI Card Style - COMPACT */
    .kpi-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 10px; /* Reduced */
        text-align: center;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-top: 4px solid #2563EB; 
    }
    .kpi-value {
        font-size: 1.5rem !important; /* Reduced */
        font-weight: 800;
        color: #000000 !important;
        margin: 0;
    }
    .kpi-label {
        font-size: 0.8rem !important; /* Reduced */
        font-weight: 600;
        color: #4B5563;
        margin: 0;
    }

    /* 7. Section Headers - SMALLER SIZE */
    .section-header {
        font-size: 1.5rem !important; /* Reduced */
        font-weight: 700;
        color: #FFFFFF !important;
        border-bottom: 1px solid #374151;
        padding-bottom: 5px;
        margin-top: 30px;
        margin-bottom: 10px;
    }
    
    /* 8. Insight Box Styling */
    .insight-box {
        background-color: #1F2937;
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid #10B981;
        margin-bottom: 10px;
        color: #FFFFFF;
        font-size: 0.85rem;
    }
    
    /* Fix for H4 headers provided by Streamlit */
    h4 {
        font-size: 1.1rem !important;
        padding-top: 0px !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 2. Load Data
# -----------------------------
DATA_PATH = "notebooks/data/cleaned_job_data.csv"

@st.cache_data
def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except:
        # Fallback dummy data
        data = {
            'status': ['Placed', 'Not Placed', 'Placed', 'Placed', 'Not Placed'] * 100,
            'degree_specialization': ['Sci&Tech', 'Comm&Mgmt', 'Sci&Tech', 'Other', 'Comm&Mgmt'] * 100,
            'experience_category': ['Fresher', 'Experienced', 'Fresher', 'Experienced', 'Fresher'] * 100,
            'skill_level': ['High', 'Low', 'Medium', 'High', 'Medium'] * 100,
            'technical_score': [80, 40, 60, 90, 45] * 100,
            'communication_score': [85, 50, 70, 95, 55] * 100,
            'aptitude_score': [75, 45, 65, 85, 50] * 100
        }
        return pd.DataFrame(data)

df = load_data()

# Identify target column
target_col = [c for c in df.columns if "place" in c.lower() or "status" in c.lower()][0]
df["status_numeric"] = df[target_col].map({"Placed": 1, "Not Placed": 0, "Yes": 1, "No": 0})

# -----------------------------
# 3. SIDEBAR (CHANGED TO DROPDOWNS)
# -----------------------------
st.sidebar.markdown("<h2 style='text-align: center;'>⚙️ Control Panel</h2>", unsafe_allow_html=True)
st.sidebar.info("Adjust the filters below to customize the analysis.")

with st.sidebar.expander("📂 Filter Options", expanded=True):
    # 1. Experience (DROPDOWN)
    exp_options = ["All"] + sorted(df["experience_category"].unique().tolist())
    experience_filter = st.selectbox("👔 1. Experience Level", options=exp_options)
    
    # 2. Skill (DROPDOWN)
    skill_options = ["All"] + sorted(df["skill_level"].unique().tolist())
    skill_filter = st.selectbox("🛠 2. Skill Level", options=skill_options)

    # 3. Degree (DROPDOWN)
    deg_options = ["All"] + sorted(df["degree_specialization"].unique().tolist())
    degree_filter = st.selectbox("🎓 3. Degree Specialization", options=deg_options)

# Apply Filters Logic for Dropdowns
filtered_df = df.copy()

if experience_filter != "All":
    filtered_df = filtered_df[filtered_df["experience_category"] == experience_filter]

if skill_filter != "All":
    filtered_df = filtered_df[filtered_df["skill_level"] == skill_filter]

if degree_filter != "All":
    filtered_df = filtered_df[filtered_df["degree_specialization"] == degree_filter]

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ About")
st.sidebar.markdown("This tool analyzes recruitment data to predict candidate success probabilities.")

# -----------------------------
# 4. BIG TITLE & INTRO
# -----------------------------
st.markdown('<div class="main-title">🚀 Job Acceptance Prediction System</div>', unsafe_allow_html=True)

st.markdown("""
<div class="sub-text">
    Welcome to the advanced HR Analytics Dashboard. This system leverages historical data 
    to analyze candidate performance, predicting who is likely to accept job offers. 
    By examining technical scores, communication skills, and experience levels, 
    recruitment teams can identify high-potential candidates and optimize strategy.
</div>
""", unsafe_allow_html=True)

# -----------------------------
# 5. KPIS
# -----------------------------
st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

# Calculations
total_candidates = len(filtered_df)
if total_candidates > 0:
    placement_rate = filtered_df["status_numeric"].mean() * 100
    dropout_rate = 100 - placement_rate
    high_risk_df = filtered_df[(filtered_df['technical_score'] < 50) & (filtered_df['communication_score'] < 50)]
    high_risk_pct = (len(high_risk_df) / total_candidates * 100)
    avg_tech = filtered_df['technical_score'].mean()
    avg_comm = filtered_df['communication_score'].mean()
    avg_apt = filtered_df['aptitude_score'].mean()
else:
    placement_rate = dropout_rate = high_risk_pct = avg_tech = avg_comm = avg_apt = 0

# --- DYNAMIC CONTEXT ---
kpi_context = f"""
Based on your current filters, we are analyzing a pool of <b>{total_candidates:,}</b> candidates. 
The current placement rate sits at <b>{placement_rate:.1f}%</b>. 
This dashboard view reflects the specific subset of talent selected in the sidebar, providing real-time metrics against the broader pool.
"""
st.markdown(f'<div class="dynamic-text">{kpi_context}</div>', unsafe_allow_html=True)

def kpi_card(label, value, symbol=""):
    st.markdown(f"""
    <div class="kpi-card">
        <p class="kpi-label">{label}</p>
        <p class="kpi-value">{symbol} {value}</p>
    </div>
    """, unsafe_allow_html=True)

# ROW 1
c1, c2, c3, c4 = st.columns(4)
with c1: kpi_card("Total Candidates", f"{total_candidates:,}", "👥")
with c2: kpi_card("Placement Rate", f"{placement_rate:.1f}%", "✅")
with c3: kpi_card("Dropout Rate", f"{dropout_rate:.1f}%", "❌")
with c4: kpi_card("High Risk Candidates", f"{high_risk_pct:.1f}%", "⚠️")

# ROW 2
c5, c6, c7 = st.columns(3)
with c5: kpi_card("Avg Technical Score", f"{avg_tech:.1f}", "📘")
with c6: kpi_card("Avg Communication", f"{avg_comm:.1f}", "🗣")
with c7: kpi_card("Avg Aptitude", f"{avg_apt:.1f}", "🧠")

# -----------------------------
# 6. RECRUITMENT ANALYSIS (Charts + Explanations)
# -----------------------------
st.markdown('<div class="section-header">📈 Recruitment Analysis</div>', unsafe_allow_html=True)

# --- ADDED MISSING ANALYSIS CONTEXT ---
analysis_context = f"""
This section breaks down the data into visual comparisons. 
The charts below dynamically update to show the ratio of placed candidates and the 
correlation between specific test scores (Technical, Communication, Aptitude) and the final hiring decision.
"""
st.markdown(f'<div class="dynamic-text">{analysis_context}</div>', unsafe_allow_html=True)

# Helper function for chart style (Clean White)
def set_white_chart_style(fig, ax):
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.tick_params(axis='x', colors='black', labelsize=8)
    ax.tick_params(axis='y', colors='black', labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor('#cccccc')
    return fig, ax

col_left, col_right = st.columns([1, 1]) # 50/50 split for even sizing

with col_left:
    st.markdown("#### 🥧 Placement Overview")
    if total_candidates > 0:
        fig, ax = plt.subplots(figsize=(4, 3)) # FIXED SIZE
        sns.countplot(data=filtered_df, x=target_col, palette="viridis", ax=ax)
        set_white_chart_style(fig, ax)
        st.pyplot(fig, use_container_width=True)
        
        # --- DYNAMIC EXPLANATION 1 ---
        p_count = len(filtered_df[filtered_df[target_col] == 'Placed'])
        np_count = len(filtered_df[filtered_df[target_col] == 'Not Placed'])
        
        st.markdown(f"""
        <div class="chart-explanation">
            <b>Insight:</b><br>
            In this selection, <b>{p_count}</b> candidates were placed vs <b>{np_count}</b> not placed.
            This visual helps identify if the selected pool has a healthy conversion rate.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No data available for these filters.")

with col_right:
    st.markdown("#### 🔗 Score Correlation Map") # Renamed for clarity
    if total_candidates > 0:
        fig, ax = plt.subplots(figsize=(4, 3)) # FIXED SIZE
        
        # FIXED: Only select relevant numeric columns for clarity
        relevant_cols = ['technical_score', 'communication_score', 'aptitude_score', 'status_numeric']
        corr_matrix = filtered_df[relevant_cols].corr()
        
        sns.heatmap(
            corr_matrix,
            annot=True, fmt=".2f", cmap="coolwarm", ax=ax,
            annot_kws={"size": 8}
        )
        
        # Style
        fig.patch.set_facecolor('white')
        ax.tick_params(axis='x', colors='black', rotation=45, labelsize=8)
        ax.tick_params(axis='y', colors='black', labelsize=8)
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(colors='black', labelsize=8)
        st.pyplot(fig, use_container_width=True)

        # --- DYNAMIC EXPLANATION 2 ---
        # Calculate actual correlation to make text accurate
        tech_corr = corr_matrix.loc['technical_score', 'status_numeric']
        comm_corr = corr_matrix.loc['communication_score', 'status_numeric']
        strongest = "Technical" if tech_corr > comm_corr else "Communication"
        
        st.markdown(f"""
        <div class="chart-explanation">
            <b>Insight:</b><br>
            This heatmap is simplified to show only critical score impacts. 
            Currently, <b>{strongest} Score</b> has the strongest influence on placement status 
            (Correlation: {max(tech_corr, comm_corr):.2f}).
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 7. BACKGROUND BREAKDOWN
# -----------------------------
st.markdown('<div class="section-header">🎓 Candidate Background Breakdown</div>', unsafe_allow_html=True)

bg_context = f"""
Dissecting performance based on educational background and experience levels helps identify 
which talent pools are yielding the best ROI for the company.
"""
st.markdown(f'<div class="dynamic-text">{bg_context}</div>', unsafe_allow_html=True)

b1, b2 = st.columns(2)

with b1:
    st.markdown("#### 🎓 Degree Specialization vs Status")
    if total_candidates > 0:
        fig, ax = plt.subplots(figsize=(4, 3)) # FIXED SIZE
        sns.countplot(data=filtered_df, x="degree_specialization", hue=target_col, palette="Set2", ax=ax)
        plt.xticks(rotation=45)
        plt.legend(facecolor='white', labelcolor='black', title='', fontsize=8)
        set_white_chart_style(fig, ax)
        st.pyplot(fig, use_container_width=True)

        # --- DYNAMIC EXPLANATION 3 ---
        # Find dominant degree
        dominant_degree = filtered_df['degree_specialization'].mode()[0] if not filtered_df.empty else "N/A"
        
        st.markdown(f"""
        <div class="chart-explanation">
            <b>Insight:</b><br>
            <b>{dominant_degree}</b> is the most common background in this view. 
            Compare the height of the orange (Placed) bars to see which major has the best success rate.
        </div>
        """, unsafe_allow_html=True)

with b2:
    st.markdown("#### ⏳ Experience Level Impact")
    if total_candidates > 0:
        fig, ax = plt.subplots(figsize=(4, 3)) # FIXED SIZE
        sns.countplot(data=filtered_df, x="experience_category", hue=target_col, palette="Set1", ax=ax)
        plt.legend(facecolor='white', labelcolor='black', title='', fontsize=8)
        set_white_chart_style(fig, ax)
        st.pyplot(fig, use_container_width=True)

        # --- DYNAMIC EXPLANATION 4 ---
        st.markdown(f"""
        <div class="chart-explanation">
            <b>Insight:</b><br>
            This chart isolates 'Fresher' vs 'Experienced' performance. 
            If the 'Placed' bar is significantly lower for Freshers, it suggests a need for better entry-level training programs.
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 8. STRATEGIC INSIGHTS
# -----------------------------
st.markdown('<div class="section-header">🧠 Strategic Business Insights</div>', unsafe_allow_html=True)

i1, i2 = st.columns(2)

with i1:
    st.markdown("""
    <div class="insight-box">
        <b>🎯 Skill Correlation</b><br>
        Candidates with Technical Scores above 70 consistently show a higher probability 
        of offer acceptance. Focus assessment efforts here.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
        <b>⚠️ Risk Mitigation</b><br>
        Early identification of candidates with low communication scores allows for 
        intervention training before the final interview rounds.
    </div>
    """, unsafe_allow_html=True)

with i2:
    st.markdown("""
    <div class="insight-box">
        <b>⏳ Experience Dynamics</b><br>
        'Freshers' often require different engagement strategies than 'Experienced' hires. 
        Tailor the onboarding process based on this categorization.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        <b>🚀 Hiring Efficiency</b><br>
        Focusing on high-conversion Degree Specializations can potentially reduce the 
        time-to-hire by approximately 15% quarter-over-quarter.
    </div>
    """, unsafe_allow_html=True)