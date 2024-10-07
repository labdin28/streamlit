import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
# Create a copy of the DataFrame with the index set to "Order_Date"
df_with_date_index = df.set_index('Order_Date')
sales_by_month = df_with_date_index.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

# (1) Dropdown for Category selection
if 'category' in df.columns:
    category_selected = st.selectbox("Select a Category", df['category'].unique())

# Filter dataframe based on selected category
filtered_df = df[df['category'] == category_selected]

# (2) Multi-select for Sub-Category within the selected Category
if not filtered_df.empty and 'sub-category' in filtered_df.columns:
    sub_category_options = filtered_df['sub-category'].unique()
    selected_sub_categories = st.multiselect(
        "Select one or more sub-categories:",
        sub_category_options,
        default=None,
        placeholder="Choose one or more sub-categories"
    )

# Further filter based on selected sub-categories
if selected_sub_categories:
    filtered_df = filtered_df[filtered_df['sub-category'].isin(selected_sub_categories)]

# Display the selected options without showing any filtered DataFrame
st.write("You selected the Category:", category_selected)
st.write("You selected the Sub-Categories:", selected_sub_categories)

# (3) Display Metrics for the filtered selection
if not filtered_df.empty and 'sales' in filtered_df.columns and 'profit' in filtered_df.columns:
    total_sales = filtered_df['sales'].sum()
    total_profit = filtered_df['profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

st.write("### Metrics for Selected Categories and Sub-Categories")
st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Profit Margin (%)", f"{profit_margin:.2f}%")

# (4) Aggregated sales by month for selected categories and sub-categories
filtered_df_with_date_index = filtered_df.set_index('order_date')
sales_by_month_filtered = filtered_df_with_date_index['sales'].groupby(pd.Grouper(freq='M')).sum()
st.write("### Sales by Month for Selected Categories and Sub-Categories")
st.line_chart(sales_by_month_filtered)

# (5) Delta for profit margin compared to overall profit margin
overall_sales = df['sales'].sum()
overall_profit = df['profit'].sum()
overall_profit_margin = (overall_profit / overall_sales) * 100 if overall_sales != 0 else 0
profit_margin_delta = profit_margin - overall_profit_margin

st.metric("Overall Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")
else:
st.write("No data available for the selected sub-categories.")
else:
st.write("Category column not found in the data.")
