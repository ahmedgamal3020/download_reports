import streamlit as st
import pandas as pd
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor 


# %%
@st.cache_data
def load_data():
    return pd.read_excel('mobility_ksa_fact_stock_ledger_entry.xlsx')
df=load_data()

st.markdown("<h1 style='color:#042771;'>Mobility Pro</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color:#042771;'>Download Reports :)</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
options = sorted(df["voucher_type"].dropna().unique())
customers= sorted(df["item_code"].unique())

with col1:
    group = st.selectbox(
    "voucher_type",
    options=options,
    index=None,
    placeholder="Select voucher_type"
)

with col2:
    customer = st.selectbox(
    "item_code",
    options=customers,
    index=None,
    placeholder="Select item_code"
)

# Sample DataFra
# Function to convert to Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
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



