import streamlit as st
import pandas as pd

# App Title
st.title("📊 Simple Data Dashboard")

# File Upload
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV and parse dates (optional, only if 'Date' column exists)
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names

    # Try parsing 'Date' column to datetime (if exists)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Data Preview
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    # Data Summary
    st.header("📈 Data Summary")
    st.write(df.describe())

    # Data Filter Section
    st.subheader("🔎 Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)

    unique_values = df[selected_column].dropna().unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write("🎯 Filtered Data", filtered_df)

    # Plot Section
    st.subheader("📉 Plot Data")
    if not filtered_df.empty:
        plot_columns = filtered_df.select_dtypes(include=["number", "datetime", "object"]).columns.tolist()
        x_column = st.selectbox("Select x-axis column", plot_columns)
        y_column = st.selectbox("Select y-axis column", plot_columns)

        if st.button("Generate Plot"):
            if x_column in filtered_df.columns and y_column in filtered_df.columns:
                try:
                    # Drop missing values in selected columns
                    plot_data = filtered_df[[x_column, y_column]].dropna()

                    # Convert x_column to datetime if it's a date-like string
                    if x_column.lower() == 'date':
                        plot_data[x_column] = pd.to_datetime(plot_data[x_column], errors='coerce')
                        plot_data = plot_data.dropna(subset=[x_column])

                    plot_data = plot_data.set_index(x_column)
                    st.line_chart(plot_data)
                except Exception as e:
                    st.error(f"Plotting failed: {e}")
            else:
                st.error("Selected columns not found in the filtered data.")
    else:
        st.warning("⚠️ Filtered data is empty. Please adjust your filter.")

else:
    st.info("📂 Please upload a CSV file to begin.")
