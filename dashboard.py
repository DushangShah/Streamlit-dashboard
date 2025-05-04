import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("/Users/dushangshah/Downloads/ALL Subject Assignment/ALY 6040/Week 4/starbucks_sales_2024.csv")
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.title("Filter Data")
selected_country = st.sidebar.multiselect("Select Country", options=df['country'].unique(), default=df['country'].unique())
selected_store_type = st.sidebar.multiselect("Select Store Type", options=df['store_type'].unique(), default=df['store_type'].unique())
date_range = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])

# Filtered data
filtered_df = df[(df['country'].isin(selected_country)) &
                 (df['store_type'].isin(selected_store_type)) &
                 (df['date'] >= pd.to_datetime(date_range[0])) &
                 (df['date'] <= pd.to_datetime(date_range[1]))]

# Title
st.title("Starbucks Business Performance Dashboard")
st.markdown("Use the filters on the left to explore different aspects of Starbucks' global performance in 2024.")

# KPIs
total_sales = filtered_df['total_sales'].sum()
avg_order_value = filtered_df['avg_order_value'].mean()
loyalty_members = filtered_df['loyalty_member_count'].sum()
total_stores = filtered_df['store_id'].nunique()

# Styling the boxes for KPIs using markdown and custom HTML
kpi_style = """
    <style>
        .kpi-box {
            border: 2px solid #E2E2E2;
            padding: 20px;
            border-radius: 10px;
            background-color: #f5f5f5;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            margin: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .kpi-title {
            color: #4CAF50;
        }
        .kpi-value {
            color: #333;
            font-size: 30px;
        }
    </style>
"""

# Display the styles on the page
st.markdown(kpi_style, unsafe_allow_html=True)

# KPIs in a horizontal layout with custom boxes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Total Sales ($)</div>
            <div class="kpi-value">{total_sales:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Avg Order Value ($)</div>
            <div class="kpi-value">{avg_order_value:.2f}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Total Loyalty Members</div>
            <div class="kpi-value">{loyalty_members:,}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="kpi-box">
            <div class="kpi-title">Total Stores</div>
            <div class="kpi-value">{total_stores}</div>
        </div>
    """, unsafe_allow_html=True)

# Visual 1: Sales Trend
sales_trend = filtered_df.groupby('date')['total_sales'].sum().reset_index()
fig1 = px.line(sales_trend, x='date', y='total_sales', title='Monthly Sales Trend')
st.plotly_chart(fig1, use_container_width=True)

# Visual 2: Sales by Product Category
category_sales = filtered_df.groupby('product_category')['total_sales'].sum().reset_index()
fig2 = px.bar(category_sales, x='product_category', y='total_sales', title='Sales by Product Category', color='product_category')
st.plotly_chart(fig2, use_container_width=True)

# Visual 3: Store Count by Country
store_counts = filtered_df.groupby('country')['store_id'].nunique().reset_index().rename(columns={'store_id': 'store_count'})
fig3 = px.choropleth(store_counts, locations='country', locationmode='country names', color='store_count',
                     title='Store Count by Country', color_continuous_scale='Viridis')
st.plotly_chart(fig3, use_container_width=True)

# Storytelling
st.markdown("### Insights")
st.markdown("- **Sales Trends** show seasonal performance. Consider marketing campaigns in months with declining sales.")
st.markdown("- **Product Category Analysis** reveals top-selling items. Focus on promoting high-performing categories.")
st.markdown("- **Geographic Distribution** highlights key markets. Explore expansion opportunities in underrepresented regions.")
