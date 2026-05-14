import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Cloud Kitchen PNL Dashboard",
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

st.title("Cloud Kitchen PNL Dashboard")


# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    df = pd.read_csv("outputs/cleaned_pnl_data.csv")
    return df


df = load_data()


# ---------------- DATE FORMATTING ---------------- #

df['MONTH'] = pd.to_datetime(df['MONTH'])

df['MONTH_LABEL'] = df['MONTH'].dt.strftime('%b %Y')


# ---------------- CREATE GM_PERCENT IF MISSING ---------------- #

if 'GM_PERCENT' not in df.columns:
    df['GM_PERCENT'] = (
        df['GROSS_MARGIN'] / df['NET_REVENUE']
    ) * 100


# ---------------- FIX VARIANCE SCALE ---------------- #

if df['VARIANCE'].mean() > 100:
    df['VARIANCE'] = df['VARIANCE'] / 10000


# ---------------- SIDEBAR ---------------- #

st.sidebar.header("Dashboard Filters")

st.sidebar.info(
    "Use filters to explore kitchen performance, profitability, and operational trends."
)


# ---------------- CITY FILTER ---------------- #

city_filter = st.sidebar.multiselect(
    "Select City",
    options=sorted(df['CITY'].dropna().unique()),
    default=sorted(df['CITY'].dropna().unique())
)


# ---------------- MONTH FILTER ---------------- #

month_filter = st.sidebar.multiselect(
    "Select Month",
    options=sorted(df['MONTH_LABEL'].dropna().unique()),
    default=sorted(df['MONTH_LABEL'].dropna().unique())
)


# ---------------- FILTERING ---------------- #

filtered_df = df[
    (df['CITY'].isin(city_filter)) &
    (df['MONTH_LABEL'].isin(month_filter))
]


# ---------------- KPI SECTION ---------------- #

st.subheader("Executive KPI Summary")

col1, col2, col3, col4 = st.columns(4)


total_revenue = filtered_df['NET_REVENUE'].sum()

avg_ebitda = filtered_df['KITCHEN_EBITDA'].mean()

avg_gm = filtered_df['GM_PERCENT'].mean()

total_stores = filtered_df['STORE'].nunique()


col1.metric(
    "Total Revenue",
    format_number(total_revenue)
)

col2.metric(
    "Average EBITDA",
    format_number(avg_ebitda)
)

col3.metric(
    "Average GM %",
    f"{avg_gm:.2f}%"
)

col4.metric(
    "Total Stores",
    total_stores
)

st.divider()


# ---------------- TREND ANALYSIS ---------------- #

st.subheader("Trend Analysis")

col5, col6 = st.columns(2)


# ---------------- MONTHLY REVENUE TREND ---------------- #

monthly_revenue = (
    filtered_df.groupby('MONTH')['NET_REVENUE']
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_revenue,
    x='MONTH',
    y='NET_REVENUE',
    title='Monthly Revenue Trend',
    markers=True
)

col5.plotly_chart(
    fig1,
    use_container_width=True
)


# ---------------- MONTHLY EBITDA TREND ---------------- #

monthly_ebitda = (
    filtered_df.groupby('MONTH')['KITCHEN_EBITDA']
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly_ebitda,
    x='MONTH',
    y='KITCHEN_EBITDA',
    title='Monthly EBITDA Trend',
    markers=True
)

col6.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()


# ---------------- OPERATIONAL ANALYSIS ---------------- #

st.subheader("Operational Performance Analysis")

col7, col8 = st.columns(2)


# ---------------- TOP STORES ---------------- #

top_stores = (
    filtered_df.groupby('STORE')['NET_REVENUE']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_stores,
    x='STORE',
    y='NET_REVENUE',
    title='Top 10 Revenue Generating Stores',
    color='NET_REVENUE'
)

fig3.update_layout(
    xaxis_tickangle=-45
)

col7.plotly_chart(
    fig3,
    use_container_width=True
)


# ---------------- STACKED REVENUE VS EBITDA ---------------- #

top10_profit = (
    filtered_df.groupby('STORE')[['NET_REVENUE', 'KITCHEN_EBITDA']]
    .sum()
    .sort_values(by='NET_REVENUE', ascending=False)
    .head(10)
    .reset_index()
)

top10_profit['COST_COMPONENT'] = (
    top10_profit['NET_REVENUE']
    - top10_profit['KITCHEN_EBITDA']
)

fig4 = go.Figure()

fig4.add_trace(
    go.Bar(
        x=top10_profit['STORE'],
        y=top10_profit['KITCHEN_EBITDA'],
        name='EBITDA'
    )
)

fig4.add_trace(
    go.Bar(
        x=top10_profit['STORE'],
        y=top10_profit['COST_COMPONENT'],
        name='Operational Cost Portion'
    )
)

fig4.update_layout(
    barmode='stack',
    title='Revenue Composition of Top Stores',
    xaxis_tickangle=-45
)

col8.plotly_chart(
    fig4,
    use_container_width=True
)

st.divider()


# ---------------- CITY REVENUE ---------------- #

st.subheader("City Level Revenue Analysis")

city_revenue = (
    filtered_df.groupby('CITY')['NET_REVENUE']
    .sum()
    .reset_index()
)

fig5 = px.bar(
    city_revenue,
    x='CITY',
    y='NET_REVENUE',
    title='Revenue Contribution Across Cities',
    color='NET_REVENUE'
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.divider()


# ---------------- VARIANCE VS EBITDA ---------------- #

st.subheader("Variance Impact Analysis")

fig6 = px.scatter(
    filtered_df,
    x='VARIANCE',
    y='KITCHEN_EBITDA',
    color='CITY',
    hover_data=['STORE', 'NET_REVENUE'],
    title='Impact of Food Variance on Profitability'
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.divider()


# ---------------- DETAILED TABLE ---------------- #

st.subheader("Detailed Kitchen Data")

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
    file_name='filtered_dashboard_data.csv',
    mime='text/csv'
)


# ---------------- FOOTER ---------------- #

st.caption(
    "Cloud Kitchen Analytics Dashboard | Built using Streamlit & Plotly"
)