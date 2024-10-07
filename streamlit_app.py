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
category_selected = st.selectbox("Select a Category", df['Category'].unique())

# Filter dataframe based on selected category
filtered_df = df[df['Category'] == category_selected]


# (2) Multi-select for Sub-Category within the selected Category
options = st.multiselect(
    "Select one or more categories:",
    df['Category'].unique(),  
    default=None,  
    placeholder="Choose one or more options"
)

# Display the selected options
st.write("You selected:", options)

if options:
    filtered_df = df[df['Category'].isin(options)]
    st.write("Filtered Data:")
    st.dataframe(filtered_df)
else:
    st.write("Please select one or more options to filter the data.")
        
# (3) Line chart of sales for the selected items
if not filtered_df.empty:
    filtered_df_with_date_index = filtered_df.set_index('Order_Date')
    sales_by_month_filtered = filtered_df_with_date_index.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()
    st.line_chart(sales_by_month_filtered, y="Sales")

# (4) Metrics for the selected items: total sales, total profit, and overall profit margin (%)
if not filtered_df.empty:
    total_sales = filtered_df['Sales'].sum()
    total_profit = filtered_df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales != 0 else 0

    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Profit", f"${total_profit:,.2f}")
    st.metric("Profit Margin (%)", f"{profit_margin:.2f}%")

# (5) Delta option for profit margin
if not filtered_df.empty:
    overall_sales = df['Sales'].sum()
    overall_profit = df['Profit'].sum()
    overall_profit_margin = (overall_profit / overall_sales) * 100 if overall_sales != 0 else 0
    profit_margin_delta = profit_margin - overall_profit_margin

    st.metric("Overall Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{profit_margin_delta:.2f}%")
