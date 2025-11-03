import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Cafeteria Insights Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    .main {
        background-color: #F8F9FA;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .stMetric {
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_excel("Cleaned_Cafeteria_Data.xlsx")
    return df

df = load_data()
st.sidebar.success("✅ Data Loaded Successfully!")


st.sidebar.title("📊 Cafeteria Reports Menu")
menu = st.sidebar.radio(
    "Select Report",
    ["🏠 Dashboard", "🏢 Floor-wise Report", "🚚 Delivery Report"]
)


if menu == "🏠 Dashboard":
    st.title("📈 Cafeteria Order Performance Dashboard")
    st.markdown("Gain quick insights into overall cafeteria performance metrics.")

    total_orders = len(df["Track ID"].unique())
    total_amount = df["Order Amount"].sum()
    avg_order_value = df["Order Amount"].mean()
    active_students = df["Admission No"].nunique()
    pending_orders = df[df["Order Status"].str.lower() == "pending"].shape[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🧾 Total Orders", total_orders)
    col2.metric("💰 Total Order Amount", f"₹{total_amount:,.0f}")
    col3.metric("📊 Average Order Value", f"₹{avg_order_value:,.0f}")
    col4.metric("🎓 Active Students", active_students)
    col5.metric("⏳ Pending Orders", pending_orders)

    st.markdown("---")

    # Monthly Order Trends
    st.subheader("📅 Monthly Order Trends")
    if "Created Month" in df.columns:
        monthly_orders = df.groupby("Created Month")["Track ID"].count().reset_index()
        fig = px.bar(
            monthly_orders,
            x="Created Month",
            y="Track ID",
            text_auto=True,
            title="Orders per Month",
            color="Track ID",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Created Month column not found in dataset.")

#  FLOOR REPORT 
elif menu == "🏢 Floor-wise Report":
    st.title("🏢 Floor-wise Order Distribution")
    st.markdown("Compare the order volume and amount across different floors.")

    if "Floor" in df.columns:
        floor_summary = df.groupby("Floor").agg(
            Total_Orders=("Track ID", "count"),
            Total_Amount=("Order Amount", "sum")
        ).reset_index()

        tab1, tab2 = st.tabs(["📦 Orders", "💰 Revenue"])

        with tab1:
            fig1 = px.bar(
                floor_summary,
                x="Floor",
                y="Total_Orders",
                title="Orders by Floor",
                color="Total_Orders",
                color_continuous_scale="Teal"
            )
            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            fig2 = px.pie(
                floor_summary,
                values="Total_Amount",
                names="Floor",
                title="Revenue Share by Floor",
                color_discrete_sequence=px.colors.sequential.Blues
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Floor column not found in dataset.")

#  DELIVERY REPORT 
elif menu == "🚚 Delivery Report":
    st.title("🚚 Delivery Status Report")
    st.markdown("Monitor the performance of order deliveries and statuses.")

    if "Order Status" in df.columns:
        delivery_summary = df["Order Status"].value_counts().reset_index()
        delivery_summary.columns = ["Status", "Count"]

        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(delivery_summary.style.background_gradient(cmap="Greens"))
        with col2:
            fig = px.pie(
                delivery_summary,
                values="Count",
                names="Status",
                title="Delivery Status Distribution",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Order Status column not found in dataset.")






