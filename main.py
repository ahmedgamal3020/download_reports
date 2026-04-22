import streamlit as st
import pandas as pd
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor 
import polars as pl
# %%
print(st.secrets["connection_string"])

def load_data():
    return pl.read_database_uri(
    query="SELECT source,item_code,qty FROM ksa.fact_sales_invoice",
    uri=st.secrets['connection_string'],
    schema_overrides={
        "source": pl.Utf8,
        "item_code": pl.Utf8,
    }
)

df = load_data()

st.markdown("<h1 style='color:#042771;'>Mobility Pro</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#042771;'>Download Reports :)</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
options = sorted(df["source"].unique().to_list())
customers = (df.select("item_code")
      .unique()
      .sort("item_code")
      .to_series()
      .to_list()
)
with col1:
    group = st.selectbox(
    "item_code",
    options=options,
    index=None,
    placeholder="Select item_code"
)

with col2:
    customer = st.selectbox(
    "source",
    options=customers,
    index=None,
    placeholder="Select source"
)

# Sample DataFra
# Function to convert to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_pandas().to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

excel_data = to_excel(df)

# Download button
st.download_button(
    label="Download Excel",
    data=excel_data,
    file_name="report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# %%


# %%



