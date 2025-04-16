import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="BI Dashboard", layout="wide")

st.title("📊 Business Intelligence Dashboard")
st.markdown("Upload the Excel file to explore insights and visualizations.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    if "Sample Data" in xls.sheet_names:
        df = xls.parse("Sample Data")

        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        st.subheader("📌 Summary Statistics")
        with st.expander("Show Summary"):
            st.write(df.describe(include="all"))

        # Filters
        st.sidebar.header("🔎 Filters")
        city = st.sidebar.multiselect("City", options=df["City"].dropna().unique())
        medium = st.sidebar.multiselect("Medium", options=df["Medium"].dropna().unique())
        contact_status = st.sidebar.multiselect("Contact Status", options=df["Contact Status"].dropna().unique())
        year = st.sidebar.multiselect("Year", options=df["Year"].dropna().unique())

        df_filtered = df.copy()
        if city:
            df_filtered = df_filtered[df_filtered["City"].isin(city)]
        if medium:
            df_filtered = df_filtered[df_filtered["Medium"].isin(medium)]
        if contact_status:
            df_filtered = df_filtered[df_filtered["Contact Status"].isin(contact_status)]
        if year:
            df_filtered = df_filtered[df_filtered["Year"].isin(year)]

        st.subheader("📈 Visualizations")

        # Revenue by City
        st.markdown("### Revenue by City")
        if not df_filtered["Revenue"].isnull().all():
            rev_city = df_filtered.groupby("City")["Revenue"].sum().sort_values(ascending=False)
            st.bar_chart(rev_city)

        # Revenue by Month
        st.markdown("### Revenue by Month")
        if not df_filtered["Revenue"].isnull().all():
            rev_month = df_filtered.groupby("Month")["Revenue"].sum()
            st.line_chart(rev_month)

        # Contact Status Distribution
        st.markdown("### Contact Status Distribution")
        status_counts = df_filtered["Contact Status"].value_counts()
        st.bar_chart(status_counts)

        # Property Distribution Pie Chart
        st.markdown("### Property Type Distribution")
        property_counts = df_filtered["Property"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(property_counts, labels=property_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    else:
        st.error("Sheet named 'Sample Data' not found in uploaded file.")
else:
    st.info("Please upload an Excel file to continue.")
