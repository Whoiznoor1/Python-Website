import streamlit as st
import pandas as pd

st.title("Simple Data Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.header("Data Summary")
    st.write(df.describe())

    st.subheader("Data Filter")
    columns = df.columns.to_list()
    selected_column = st.selectbox("Select column to filter by", columns)
    
    unique_values = df[selected_column].unique()
    selected_value = st.selectbox("Select value", unique_values)

    filtered_df = df[df[selected_column] == selected_value]
    st.write(filtered_df)

    st.subheader("Plot Data")
    if not filtered_df.empty:
        x_column = st.selectbox("Select x-axis column", columns)
        y_column = st.selectbox("Select y-axis column", columns)

        if st.button("Generate Plot"):
            st.line_chart(filtered_df.set_index(x_column)[y_column])
    else:
        st.write("Filtered data is empty. Please adjust your filter.")
else:
    st.write("Waiting on a file upload.....")


        
