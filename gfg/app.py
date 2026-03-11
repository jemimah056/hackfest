import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="AI BI Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# CUSTOM CSS
# -------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* PROFESSIONAL BLUE BACKGROUND */

[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#0b1e4d,#1e3a8a);
}

/* TITLE STYLE */

.main-title {
    font-size:48px;
    font-weight:700;
    text-align:center;
    margin-bottom:10px;
    background: linear-gradient(90deg,#ffffff,#e2e8f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* KPI CARDS */

.card {
    background:white;
    padding:25px;
    border-radius:14px;
    box-shadow:0px 6px 20px rgba(0,0,0,0.2);
    text-align:center;
}

.metric {
    font-size:32px;
    font-weight:700;
    color:#1e3a8a;
}

.small-text {
    font-size:15px;
    color:#6b7280;
}

/* DATAFRAME STYLE */

div[data-testid="stDataFrame"] {
    background:white;
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# CSV UPLOAD
# -------------------------

st.sidebar.subheader("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Browse CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("CSV uploaded successfully")
else:
    df = pd.read_csv("sales_data.csv")

# -------------------------
# AUTO DETECT COLUMN TYPES
# -------------------------

numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# -------------------------
# SIDEBAR FILTER
# -------------------------

st.sidebar.title("Dashboard Filters")

if categorical_cols:
    filter_column = st.sidebar.selectbox(
        "Select Filter Column",
        categorical_cols
    )

    filter_values = st.sidebar.multiselect(
        "Filter Values",
        options=df[filter_column].unique(),
        default=df[filter_column].unique()
    )

    filtered_df = df[df[filter_column].isin(filter_values)]

else:
    filtered_df = df

# -------------------------
# TITLE
# -------------------------

st.markdown(
'<div class="main-title">Conversational AI Business Intelligence Dashboard</div>',
unsafe_allow_html=True
)

st.write("Ask business questions and generate dashboards instantly.")

st.divider()

# -------------------------
# KPI METRICS (GENERIC)
# -------------------------

col1, col2, col3 = st.columns(3)

total_rows = filtered_df.shape[0]
total_columns = filtered_df.shape[1]

numeric_sum = 0
if numeric_cols:
    numeric_sum = filtered_df[numeric_cols[0]].sum()

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="metric">📊 {total_rows}</div>
        <div class="small-text">Total Records</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="metric">📁 {total_columns}</div>
        <div class="small-text">Total Columns</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="metric">🔢 {numeric_sum}</div>
        <div class="small-text">Sum of {numeric_cols[0] if numeric_cols else 'Values'}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# -------------------------
# QUERY INPUT
# -------------------------

query = st.text_input("💬 Ask a business question")

st.caption("Example: category analysis, trend analysis, distribution")


# -------------------------
# QUERY ANALYSIS
# -------------------------

def analyze_query(query):

    query = query.lower()

    if numeric_cols and categorical_cols:

        num_col = numeric_cols[0]
        cat_col = categorical_cols[0]

        result = filtered_df.groupby(cat_col)[num_col].sum().reset_index()

        if "trend" in query or "line" in query:

            chart = "line"
            title = f"{num_col} Trend by {cat_col}"

        elif "pie" in query or "distribution" in query:

            chart = "pie"
            title = f"{num_col} Distribution by {cat_col}"

        else:

            chart = "bar"
            title = f"{num_col} by {cat_col}"

    else:

        result = filtered_df
        chart = "table"
        title = "Dataset Preview"

    return result, chart, title

# -------------------------
# DASHBOARD OUTPUT
# -------------------------

if query:

    with st.spinner("AI is generating insights..."):

        result, chart, title = analyze_query(query)

    st.subheader(title)

    if chart == "bar":

        fig = px.bar(
            result,
            x=result.columns[0],
            y=result.columns[1],
            color=result.columns[0],
            text=result.columns[1]
        )

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "line":

        fig = px.line(
            result,
            x=result.columns[0],
            y=result.columns[1],
            markers=True
        )

        st.plotly_chart(fig, use_container_width=True)

    elif chart == "pie":

        fig = px.pie(
            result,
            names=result.columns[0],
            values=result.columns[1]
        )

        st.plotly_chart(fig, use_container_width=True)

    else:

        st.dataframe(result)

st.divider()

# -------------------------
# DATA PREVIEW
# -------------------------

st.subheader("📁 Dataset Preview")

st.dataframe(filtered_df)