import streamlit as st
import pandas as pd


st.title("📊 Simple Data Dashboard")


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    
    
    df.columns = df.columns.str.strip()

    
    st.subheader("🔍 Data Preview")
    st.write(df.head())

    
    st.header("📈 Data Summary")
    st.write(df.describe())

    
    st.subheader("🔎 Filter Data")
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select column to filter by", columns)

    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write("🎯 Filtered Data", filtered_df)

    # Plot Section
    st.subheader("📉 Plot Data")
    if not filtered_df.empty:
        plot_columns = filtered_df.columns.tolist()

        x_column = st.selectbox("Select x-axis column", plot_columns)
        y_column = st.selectbox("Select y-axis column", plot_columns)

        if st.button("Generate Plot"):
            if x_column in filtered_df.columns and y_column in filtered_df.columns:
                try:
                    st.line_chart(filtered_df.set_index(x_column)[y_column])
                except Exception as e:
                    st.error(f"Plotting failed: {e}")
            else:
                st.error("Selected columns not found in the filtered data.")
    else:
        st.warning("Filtered data is empty. Please adjust your filter.")

else:
    st.info("📂 Please upload a CSV file to begin.")
