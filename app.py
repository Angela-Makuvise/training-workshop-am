import streamlit as st
import pandas as pd

st.set_page_config(page_title="🧠 AI Data Explorer", layout="wide")
st.title("🧠 AI Data Explorer")

uploaded = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx","xls"])

if uploaded:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        xl = pd.ExcelFile(uploaded)
        sheet = st.selectbox("Select sheet", xl.sheet_names)
        df = pd.read_excel(uploaded, sheet_name=sheet)

    st.success("Dataset loaded.")
    st.subheader("Preview")
    st.dataframe(df.head())

    st.subheader("Overview")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing", int(df.isna().sum().sum()))
    c4.metric("Duplicates", int(df.duplicated().sum()))

    st.subheader("Column summary")
    summary = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "missing": df.isna().sum(),
        "missing_%": (df.isna().mean()*100).round(2),
        "unique": df.nunique()
    })
    st.dataframe(summary)

    num = df.select_dtypes("number")
    if not num.empty:
        st.subheader("Statistical summary")
        st.dataframe(num.describe().T)
        st.bar_chart(num.isna().sum())
else:
    st.info("Upload a dataset to begin.")

