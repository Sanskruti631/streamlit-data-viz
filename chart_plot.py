import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page config
st.set_page_config(page_title="Data Visualization App", layout="wide")

# Title
st.title("📊 Data Visualization with Matplotlib")


# Load sample dataset
@st.cache_data  # Cache the data for better performance
def load_data():
    data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Sales': [120, 150, 180, 135, 210, 190, 220, 240, 230, 250, 270, 300],
        'Expenses': [80, 90, 95, 75, 110, 100, 120, 130, 125, 140, 150, 160],
        'Profit': [40, 60, 85, 60, 100, 90, 100, 110, 105, 110, 120, 140]
    })

    return data


df = load_data()

# Sidebar controls
st.sidebar.header("Customize the Plots")
chart_type = st.sidebar.selectbox(
    "Select Chart Type",
    options=["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart", "Histogram"]
)

show_expenses = st.sidebar.checkbox("Show Expenses", True)
show_profit = st.sidebar.checkbox("Show Profit", True)

# Create plots based on user selection
fig, ax = plt.subplots(figsize=(10, 5))

if chart_type == "Bar Chart":
    width = 0.35
    x = np.arange(len(df['Month']))

    if show_expenses:
        ax.bar(x - width / 2, df['Expenses'], width, label='Expenses', color='#FF7F0E')
    if show_profit:
        ax.bar(x + width / 2, df['Profit'], width, label='Profit', color='#1F77B4')

    ax.set_xticks(x)
    ax.set_xticklabels(df['Month'])
    ax.set_title("Monthly Performance Comparison")
    ax.legend()

elif chart_type == "Line Chart":
    if show_expenses:
        ax.plot(df['Month'], df['Expenses'], marker='o', label='Expenses', color='#FF7F0E')
    if show_profit:
        ax.plot(df['Month'], df['Profit'], marker='s', label='Profit', color='#1F77B4')

    ax.set_title("Monthly Trends")
    ax.legend()

elif chart_type == "Scatter Plot":
    ax.scatter(df['Expenses'], df['Sales'], c=df.index, cmap='viridis')
    ax.set_xlabel("Expenses")
    ax.set_ylabel("Sales")
    ax.set_title("Expenses vs Sales")

elif chart_type == "Pie Chart":
    data = df['Sales']
    wedges, texts, _ = ax.pie(
        data,
        labels=df['Month'],
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Paired.colors,
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.5}
    )
    ax.set_title("Monthly Sales Distribution")

elif chart_type == "Histogram":
    ax.hist(df['Sales'], bins=10, color='skyblue', edgecolor='black')
    ax.set_title("Sales Distribution")
    ax.set_xlabel("Sales")
    ax.set_ylabel("Frequency")

# Add grid and styling
ax.grid(True, alpha=0.3)
plt.tight_layout()

# Display the plot
st.pyplot(fig)

# Show raw data
st.subheader("📝 Raw Data")
st.dataframe(df)

# Data download option
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='business_metrics.csv',
    mime='text/csv'
)
