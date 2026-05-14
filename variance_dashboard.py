import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Variance Level PNL Dashboard",
    layout="wide"
)


# ---------------- HELPER FUNCTION ---------------- #

def format_number(num):
    if num >= 10000000:
        return f"{num/10000000:.2f} Cr"
    elif num >= 100000:
        return f"{num/100000:.2f} L"
    else:
        return f"{num:,.0f}"


# ---------------- TITLE ---------------- #

st.title("Variance Level PNL Dashboard")


# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    df = pd.read_csv("outputs/cleaned_pnl_data.csv")
    return df

df = load_data()
# ---------------- FIX VARIANCE SCALE ---------------- #

if df['VARIANCE'].mean() > 100:
    df['VARIANCE'] = df['VARIANCE'] / 10000
    
# ---------------- REBUILD VARIANCE CATEGORY ---------------- #

def variance_bucket(x):
    if x < 2:
        return 'Var <2%'
    elif x < 3:
        return 'Var 2%-3%'
    elif x < 5:
        return 'Var 3%-5%'
    else:
        return 'Var >5%'


df['VARIANCE_CATEGORY'] = df['VARIANCE'].apply(variance_bucket)

# ---------------- DATE FORMATTING ---------------- #

df['MONTH'] = pd.to_datetime(df['MONTH'])

df['MONTH_LABEL'] = df['MONTH'].dt.strftime('%b %Y')


# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Variance Filters")

st.sidebar.info(
    "Use filters to explore variance trends and operational efficiency."
)

variance_filter = st.sidebar.multiselect(
    "Select Variance Category",
    options=df['VARIANCE_CATEGORY'].unique(),
    default=df['VARIANCE_CATEGORY'].unique()
)

revenue_filter = st.sidebar.multiselect(
    "Select Revenue Bucket",
    options=df['REVENUE_BUCKET'].unique(),
    default=df['REVENUE_BUCKET'].unique()
)

month_filter = st.sidebar.multiselect(
    "Select Month",
    options=df['MONTH_LABEL'].unique(),
    default=df['MONTH_LABEL'].unique()
)


# ---------------- FILTERING ---------------- #

filtered_df = df[
    (df['VARIANCE_CATEGORY'].isin(variance_filter)) &
    (df['REVENUE_BUCKET'].isin(revenue_filter)) &
    (df['MONTH_LABEL'].isin(month_filter))
]


# ---------------- KPI SECTION ---------------- #

st.subheader("Executive KPI Summary")

col1, col2, col3 = st.columns(3)

avg_variance = filtered_df['VARIANCE'].mean()

total_stores = filtered_df['STORE'].nunique()

avg_ebitda = filtered_df['KITCHEN_EBITDA'].mean()

col1.metric("Average Variance %", f"{avg_variance:.2f}%")

col2.metric("Total Stores", total_stores)

col3.metric("Average EBITDA", format_number(avg_ebitda))

st.divider()


# ---------------- VARIANCE ANALYSIS ---------------- #

st.subheader("Variance Performance Analysis")

col4, col5 = st.columns(2)


# ---------------- AVG VARIANCE BY REVENUE ---------------- #

variance_summary = (
    filtered_df.groupby('REVENUE_BUCKET')['VARIANCE']
    .mean()
    .reset_index()
)

fig1 = px.bar(
    variance_summary,
    x='REVENUE_BUCKET',
    y='VARIANCE',
    color='REVENUE_BUCKET',
    title='Average Variance by Revenue Bucket'
)

col4.plotly_chart(fig1, use_container_width=True)


# ---------------- STORE COUNT SUMMARY ---------------- #

store_summary = pd.pivot_table(
    filtered_df,
    values='STORE',
    index='REVENUE_BUCKET',
    columns='MONTH_LABEL',
    aggfunc='count',
    fill_value=0
)

col5.subheader("Store Count Summary")

col5.dataframe(store_summary)

st.divider()


# ---------------- VARIANCE DISTRIBUTION ---------------- #

variance_distribution = (
    filtered_df['VARIANCE_CATEGORY']
    .value_counts()
    .reset_index()
)

variance_distribution.columns = [
    'VARIANCE_CATEGORY',
    'COUNT'
]

fig2 = px.pie(
    variance_distribution,
    names='VARIANCE_CATEGORY',
    values='COUNT',
    title='Variance Category Distribution'
)

st.plotly_chart(fig2, use_container_width=True)

st.divider()


# ---------------- DETAILED TABLE ---------------- #

st.subheader("Detailed Variance Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# ---------------- DOWNLOAD BUTTON ---------------- #

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name='variance_dashboard_data.csv',
    mime='text/csv'
)


# ---------------- FOOTER ---------------- #

st.caption(
    "Variance Analytics Dashboard | Built using Streamlit & Plotly"
)