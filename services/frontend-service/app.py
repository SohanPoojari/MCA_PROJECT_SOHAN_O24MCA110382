import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

# --- 0. SERVICE CONNECTIONS (The missing links!) ---
# These names must match your Kubernetes Service names exactly
USER_SERVICE_URL = "http://user-service-service:5001"
PRODUCT_SERVICE_URL = "http://product-service-service:5002"
ORDER_SERVICE_URL = "http://order-service-service:5003"

# --- 1. SETTINGS & GLASS-MORPHISM UI ---
st.set_page_config(page_title="Azure Cloud Command", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* 1. Global Font Size & Background */
    html, body, [class*="ViewContainer"] {
        font-size: 1.1rem;
        background-color: #f0f2f6;
    }
    
    /* 2. Massive Gradient Title */
    .super-title {
        background: linear-gradient(90deg, #0078D4, #00BCF2, #886CE4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 70px !important;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 0px;
    }
    
    /* 3. High-Impact Metric Cards */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 30px !important;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        transition: 0.4s;
    }
    [data-testid="stMetric"]:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 32px 0 rgba(0, 120, 212, 0.3);
    }
    
    /* 4. Increase Labels & Sidebar text */
    .st-emotion-cache-16idsys p {
        font-size: 1.3rem !important;
        font-weight: 600 !important;
    }
    
    /* 5. Custom Button - Make it BIG */
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        border-radius: 12px !important;
        background: linear-gradient(45deg, #0078D4, #00BCF2) !important;
        color: white !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/144/cloud-lighting.png", width=100)
    st.markdown("# CLOUD OS")
    st.caption("ADMIN CONSOLE v3.0")
    st.divider()
    menu = st.selectbox("CHOOSE MODULE", ["📊 ANALYTICS", "👥 USER ENGINE", "📦 PRODUCT HUB", "🛒 ORDER FLOW"])
    st.divider()
    st.status("NETWORK: SECURE", state="complete")

# --- 4. ANALYTICS (THE "WOW" PAGE) ---
if menu == "📊 ANALYTICS":
    st.markdown('<p class="super-title">Cloud Intelligence</p>', unsafe_allow_html=True)
    st.markdown("#### Real-time Global Cluster Telemetry")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("CPU LOAD", "14.2%", "Optimal", delta_color="normal")
    m2.metric("MEM USAGE", "2.1 GB", "-0.4 GB", delta_color="inverse")
    m3.metric("NODES", "12 Active", "0 Failure")
    m4.metric("REGION", "IND-CENTRAL", "LATENCY: 4ms")

    st.divider()
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### 🛰️ Global Request Traffic")
        chart_data = pd.DataFrame(np.random.randn(25, 3), columns=['User', 'Product', 'Order'])
        st.area_chart(chart_data, use_container_width=True)
        
    with col_right:
        st.markdown("### 🔔 System Events")
        st.success("✅ AKS Deployment successful")
        st.info("ℹ️ Load Balancer Scaled to 3")
        st.warning("⚠️ Database backup at 04:00")
        st.error("🚨 Unauthorized attempt blocked")

# --- 5. USER ENGINE ---
elif menu == "👥 USER ENGINE":
    st.markdown('<p class="super-title">Identity Manager</p>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["➕ PROVISION NEW IDENTITY", "📋 MASTER REGISTRY"])
    
    with tab1:
        with st.container():
            st.markdown("### 📥 Register Cloud User")
            with st.form("user_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                name = col1.text_input("FULL NAME")
                email = col2.text_input("CORPORATE EMAIL")
                if st.form_submit_button("EXECUTE PROVISIONING", type="primary"):
                    try:
                        res = requests.post(f"{USER_SERVICE_URL}/users", json={"name": name, "email": email})
                        if res.status_code == 201:
                            st.balloons()
                            st.success(f"Identity {name} synced to Azure SQL.")
                    except:
                        st.error("🚨 User Service Offline")

    with tab2:
        if st.button("🔄 REFRESH USER DATA"):
            try:
                res = requests.get(f"{USER_SERVICE_URL}/users")
                st.dataframe(pd.DataFrame(res.json()), use_container_width=True)
            except:
                st.info("No active users found in cluster.")

# --- 6. PRODUCT HUB ---
elif menu == "📦 PRODUCT HUB":
    st.markdown('<p class="super-title">Inventory Core</p>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["➕ ADD ASSET", "📦 STOCK LEDGER"])
    
    with tab1:
        with st.form("prod_form"):
            p_name = st.text_input("PRODUCT NAME")
            p_price = st.number_input("UNIT PRICE ($)", min_value=0.0)
            p_stock = st.number_input("INITIAL STOCK", min_value=0)
            if st.form_submit_button("ADD TO INVENTORY"):
                try:
                    res = requests.post(f"{PRODUCT_SERVICE_URL}/products", 
                                       json={"name": p_name, "price": p_price, "stock": p_stock})
                    if res.status_code == 201:
                        st.toast("Product Catalog Updated!", icon="📦")
                        st.success("Asset logged in Inventory Database.")
                except:
                    st.error("🚨 Product Service Offline")

    with tab2:
        if st.button("🔄 SYNC STOCK"):
            try:
                res = requests.get(f"{PRODUCT_SERVICE_URL}/products")
                st.dataframe(pd.DataFrame(res.json()), use_container_width=True)
            except:
                st.info("Inventory is empty.")

# --- 7. ORDER FLOW ---
elif menu == "🛒 ORDER FLOW":
    st.markdown('<p class="super-title">Transaction Engine</p>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["⚡ PLACE ORDER", "📜 ORDER HISTORY"])
    
    with tab1:
        with st.form("order_form"):
            u_id = st.text_input("USER UUID")
            p_id = st.text_input("PRODUCT UUID")
            qty = st.number_input("QUANTITY", min_value=1)
            if st.form_submit_button("COMPLETE TRANSACTION"):
                try:
                    res = requests.post(f"{ORDER_SERVICE_URL}/orders", 
                                       json={"user_id": u_id, "product_id": p_id, "quantity": qty})
                    if res.status_code == 201:
                        st.snow()
                        st.success("Transaction Finalized on AKS.")
                except:
                    st.error("🚨 Order Service Offline")

    with tab2:
        if st.button("🔄 PULL ORDER LOGS"):
            try:
                res = requests.get(f"{ORDER_SERVICE_URL}/orders")
                st.dataframe(pd.DataFrame(res.json()), use_container_width=True)
            except:
                st.info("No transaction logs found.")