import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("./data/gapminder_data_graphs.csv")

with st.sidebar:
    selected_continent = st.selectbox("Select continent", df['continent'].unique().tolist())
    selected_country = st.selectbox("Select country",
                                    df[df['continent']==selected_continent]['country'].unique().tolist())
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col not in ['year', 'country', 'continent']]
    selected_columns = st.multiselect("Select columns to display and plot", options= numeric_cols,
                                      default= ['gdp'])

filtered_df = df[(df['continent'] == selected_continent) & (df['country'] == selected_country)]
st.subheader(selected_country)
if selected_columns:
    num_cols_per_row = 2
    rows = (len(selected_columns) + num_cols_per_row - 1) // num_cols_per_row

    for i in range(rows):
        cols = st.columns(num_cols_per_row)
        for j in range(num_cols_per_row):
            idx = i * num_cols_per_row + j
            if idx < len(selected_columns):
                colname = selected_columns[idx]
                fig = px.line(
                    filtered_df,
                    x='year',
                    y=colname,
                    markers=True,
                    title=f"{colname} Over Time",
                    template="plotly_white"
                )
                cols[j].plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 Please select at least one column to plot.")
st.subheader("Raw Data")
st.write(filtered_df[selected_columns])
