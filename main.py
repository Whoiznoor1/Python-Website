import streamlit as st
import pandas as pd

# App Title
st.title("📊 Simple Data Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Load CSV and clean columns
    df = pd.read_csv(uploaded_file)
    df.columns = df.columns.str.strip()

    # Try converting 'Date' column if present
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Preview data
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # Show basic summary
    st.subheader("📈 Data Summary")
    st.write(df.describe())

    # Filter section
    st.subheader("🔎 Filter Data")
    selected_column = st.selectbox("Choose a column to filter by", df.columns, key="filter_column")
    unique_values = df[selected_column].dropna().unique()
    selected_value = st.selectbox("Choose a value", unique_values, key="filter_value")

    filtered_df = df[df[selected_column] == selected_value]
    st.write("🎯 Filtered Data")
    st.dataframe(filtered_df)

    # Plotting section
    st.subheader("📉 Plot Data")
    if not filtered_df.empty:
        numeric_columns = filtered_df.select_dtypes(include=['number']).columns.tolist()
        object_columns = filtered_df.select_dtypes(include=['object', 'datetime']).columns.tolist()

        x_axis = st.selectbox("Select X-axis", object_columns + numeric_columns, key="x_axis")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="y_axis")

        if st.button("Generate Plot", key="plot_button"):
            try:
                # Drop NA values and set index
                plot_data = filtered_df[[x_axis, y_axis]].dropna()

                # Convert x-axis to datetime if it’s the 'Date' column
                if x_axis.lower() == 'date':
                    plot_data[x_axis] = pd.to_datetime(plot_data[x_axis], errors='coerce')
                    plot_data = plot_data.dropna(subset=[x_axis])

                plot_data = plot_data.set_index(x_axis)
                st.line_chart(plot_data)
            except Exception as e:
                st.error(f"Plotting failed: {e}")
    else:
        st.warning("⚠️ No data found for the selected filter.")
else:
    st.info("📂 Please upload a CSV file to begin.")
