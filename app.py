import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide", page_title="Shopify-Style BI Dashboard")
st.set_option('client.showErrorDetails', True)
st.title("📈 Shopify-Style Business Intelligence Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    df = xls.parse(xls.sheet_names[0])
    df.columns = df.columns.str.strip()  # clean column names

    # Filters
    with st.sidebar:
        st.header("🔍 Filters")
        year = st.multiselect("Year", sorted(df["Year"].dropna().unique()), default=df["Year"].dropna().unique())
        month = st.multiselect("Month", sorted(df["Month"].dropna().unique()), default=df["Month"].dropna().unique())
        city = st.multiselect("City", sorted(df["City"].dropna().unique()), default=df["City"].dropna().unique())
        status = st.multiselect("Contact Status", sorted(df["Contact Status"].dropna().unique()), default=df["Contact Status"].dropna().unique())

    # Filtered data
    df_filtered = df[
        df["Year"].isin(year) &
        df["Month"].isin(month) &
        df["City"].isin(city) &
        df["Contact Status"].isin(status)
    ]

    # --- LOTTIE ICONS ---
    def load_lottieurl(url):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        except:
            return None

    icon_customer = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_jzszqf7u.json")
    icon_city = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_ukb6onbi.json")
    icon_variant = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_xlky4kvn.json")

    # --- KPI CARDS ---
    st.markdown("## 🚀 Key Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        if icon_customer:
            st_lottie(icon_customer, height=60, key="customer")
        st.markdown("### 👥 Top Customer")
        if "Company Org. Name" in df_filtered.columns:
            top_customers = df_filtered["Company Org. Name"].value_counts().head(5)
            if not top_customers.empty:
                st.markdown(f"""
                    <div style='padding: 10px; background: linear-gradient(to right, #e0f7fa, #80deea); border-radius: 12px;'>
                        <h4 style='margin-bottom: 5px;'>{top_customers.index[0]}</h4>
                        <p style='color: gray;'>{top_customers.iloc[0]} orders</p>
                    </div>
                """, unsafe_allow_html=True)

    with col2:
        if icon_city:
            st_lottie(icon_city, height=60, key="city")
        st.markdown("### 🏙️ Top City")
        if "City" in df_filtered.columns:
            top_cities = df_filtered["City"].value_counts().head(5)
            if not top_cities.empty:
                st.markdown(f"""
                    <div style='padding: 10px; background: linear-gradient(to right, #fce4ec, #f8bbd0); border-radius: 12px;'>
                        <h4 style='margin-bottom: 5px;'>{top_cities.index[0]}</h4>
                        <p style='color: gray;'>{top_cities.iloc[0]} orders</p>
                    </div>
                """, unsafe_allow_html=True)

    with col3:
        if icon_variant:
            st_lottie(icon_variant, height=60, key="variant")
        st.markdown("### 🛒 Top Variant")
        variant_col = "Variant" if "Variant" in df_filtered.columns else "Property"
        if variant_col in df_filtered.columns:
            top_variants = df_filtered[variant_col].value_counts().head(5)
            if not top_variants.empty:
                st.markdown(f"""
                    <div style='padding: 10px; background: linear-gradient(to right, #e8f5e9, #a5d6a7); border-radius: 12px;'>
                        <h4 style='margin-bottom: 5px;'>{top_variants.index[0]}</h4>
                        <p style='color: gray;'>{top_variants.iloc[0]} sold</p>
                    </div>
                """, unsafe_allow_html=True)

    # --- CHARTS ---
    st.markdown("## 📊 Data Visualizations")

    if "Revenue" in df_filtered.columns:
        st.markdown("#### 💰 Revenue by City")
        rev_city = df_filtered.groupby("City")["Revenue"].sum().sort_values(ascending=False)
        st.bar_chart(rev_city)

        st.markdown("#### 📅 Revenue Trend (by Month)")
        rev_trend = df_filtered.groupby("Month")["Revenue"].sum().sort_values(ascending=False)
        st.bar_chart(rev_trend)
    else:
        st.warning("⚠️ 'Revenue' column not found.")

    if "Contact Status" in df_filtered.columns:
        st.markdown("#### 📞 Leads by Contact Status")
        status_counts = df_filtered["Contact Status"].value_counts().sort_values(ascending=False)
        st.bar_chart(status_counts)

    # Download filtered data
    st.markdown("---")
    st.download_button("📥 Download Filtered Data as CSV", df_filtered.to_csv(index=False), "filtered_data.csv")
