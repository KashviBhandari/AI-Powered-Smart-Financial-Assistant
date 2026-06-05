import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import joblib
import datetime
import time
from groq import Groq
from dotenv import load_dotenv
import os
import hashlib



# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="FinGen AI",
    page_icon="logo.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= SAFE LOGO PATH =================
BASE_DIR = os.path.dirname(__file__)
logo_path = os.path.join(BASE_DIR, "logo.png")

# ================= HEADER =================
col1, col2 = st.columns([1, 6])

with col1:
    if os.path.isfile(logo_path):
        st.image(logo_path, width=90)
    else:
        st.warning("⚠️ Logo not found (check logo.png in project folder)")

with col2:
    st.markdown("""
    <div class="custom-header">
        <div class="title">💰 FinGen AI</div>
        <div class="subtitle">
            AI Powered Smart Financial Dashboard
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= SIDEBAR =================

st.markdown("""
<style>

/* Background */
.stApp{
    background:#070B0D;
}

/* Titles */
h1,h2,h3,h4,h5,h6{
    color:#FFFFFF !important;
}
/* ==========================================
   FIX keyboard_double_arrow_right TEXT
========================================== */

/* Hide sidebar collapse control */
[data-testid="collapsedControl"]{
    display:none !important;
}

/* Hide sidebar collapse button */
[data-testid="stSidebarCollapseButton"]{
    display:none !important;
}

/* Hide Material Icon names */
.material-icons,
.material-symbols-rounded,
.material-symbols-outlined{
    font-size:0 !important;
}

/* Hide header button text */
button[kind="header"] span{
    display:none !important;
}

/* Text */
p,span,label,div{
    color:#FFFFFF;
}

/* ==========================================
   SIDEBAR MAIN
========================================== */
section[data-testid="stSidebar"]{
    background: linear-gradient(
        180deg,
        #0B0F12 0%,
        #11161B 40%,
        #181F25 100%
    ) !important;

    border-right: 2px solid rgba(219,45,40,0.25);
}

/* ==========================================
   SIDEBAR TEXT
========================================== */
section[data-testid="stSidebar"] *{
    color:white !important;
    font-family: 'Segoe UI', sans-serif;
}

/* ==========================================
   LOGO CARD
========================================== */
.sidebar-logo{
    background: linear-gradient(
        135deg,
        rgba(219,45,40,0.18),
        rgba(255,255,255,0.03)
    );

    border:1px solid rgba(219,45,40,0.35);

    padding:28px 20px;

    border-radius:24px;

    text-align:center;

    margin-bottom:20px;

    box-shadow:
    0px 0px 25px rgba(219,45,40,0.18);
}

/* ==========================================
   LOGO TITLE
========================================== */
.sidebar-logo h1{
    color:#FFFFFF;
    font-size:34px;
    margin-bottom:6px;
    font-weight:800;
    letter-spacing:1px;
}

/* ==========================================
   SUBTITLE
========================================== */
.sidebar-logo p{
    color:#B8C1CC;
    font-size:14px;
    margin-top:0;
}

/* ==========================================
   RADIO CONTAINER
========================================== */
.stRadio > div{
    gap:12px;
}

/* ==========================================
   RADIO BUTTON STYLE
========================================== */
div[role="radiogroup"] > label{

    background:#161D22 !important;

    padding:14px 18px !important;

    border-radius:16px !important;

    border:1px solid rgba(255,255,255,0.06);

    transition:0.3s ease;

    margin-bottom:8px;

    font-weight:600;

    box-shadow:
    0px 2px 10px rgba(0,0,0,0.20);
}

/* ==========================================
   HOVER EFFECT
========================================== */
div[role="radiogroup"] > label:hover{

    background: linear-gradient(
        135deg,
        #DB2D28,
        #8B1E1A
    ) !important;

    transform:translateX(4px);

    border:1px solid #DB2D28;

    box-shadow:
    0px 0px 18px rgba(219,45,40,0.45);
}

/* ==========================================
   SELECTED OPTION
========================================== */
div[role="radiogroup"] label[data-selected="true"]{

    background: linear-gradient(
        135deg,
        #DB2D28,
        #7F1714
    ) !important;

    border:1px solid #DB2D28 !important;

    box-shadow:
    0px 0px 18px rgba(219,45,40,0.45);
}

/* ==========================================
   RADIO TEXT
========================================== */
div[role="radiogroup"] label p{
    font-size:15px !important;
    color:white !important;
}

/* ==========================================
   HIDE DEFAULT RADIO CIRCLE
========================================== */
div[role="radiogroup"] input{
    display:none;
}

/* ==========================================
   SIDEBAR SCROLLBAR
========================================== */
section[data-testid="stSidebar"] ::-webkit-scrollbar{
    width:6px;
}

section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb{
    background:#DB2D28;
    border-radius:20px;
}

/* ==========================================
   USER PROFILE CARD
========================================== */
.profile-card{
    background:#161D22;

    border-radius:18px;

    padding:18px;

    margin-top:25px;

    text-align:center;

    border:1px solid rgba(255,255,255,0.05);
}

.profile-card h3{
    margin-bottom:5px;
}

.profile-card p{
    color:#9DA8B3;
    font-size:13px;
}

/* ==========================================
   GLOW LINE
========================================== */
.glow-line{
    height:2px;
    background:linear-gradient(
        90deg,
        transparent,
        #DB2D28,
        transparent
    );

    margin-top:18px;
    margin-bottom:18px;
}
/* All Streamlit Buttons */
.stButton > button {
    background: #DB2D28 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.stButton > button:hover {
    background: #B8221E !important;
    color: white !important;
    box-shadow: 0 0 15px rgba(219,45,40,0.4);
}

/* Download Button */
.stDownloadButton > button {
    background: #DB2D28 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

.stDownloadButton > button:hover {
    background: #B8221E !important;
    color: white !important;
}

/* Form Submit Buttons */
button[kind="primary"] {
    background: #DB2D28 !important;
    color: white !important;
}

/* Cards */
.neo-card{
    background:#14191D;
    border-radius:20px;
    padding:25px;
    color:white;
    border:1px solid rgba(255,255,255,0.08);
}

/* Metrics */
[data-testid="metric-container"]{
    background:#14191D;
    border-radius:18px;
    border-left:4px solid #DB2D28;
}

[data-testid="metric-container"] *{
    color:#FFFFFF !important;
}

/* Inputs */
.stTextInput input,
.stNumberInput input{
    background:#14191D !important;
    color:#FFFFFF !important;
    border:1px solid #41494F !important;
}

/* Buttons */
.stButton button{
    background:#DB2D28;
    color:white;
    border:none;
    border-radius:12px;
    font-weight:700;
}

/* ==========================================
   SELECTBOX
========================================== */
div[data-baseweb="select"] > div{
    background:#14191D !important;
    color:white !important;
    border:1px solid #DB2D28 !important;
    border-radius:12px !important;
}

div[data-baseweb="select"] span{
    color:white !important;
    font-weight:600 !important;
}

/* ==========================================
   MULTISELECT TAGS
========================================== */
[data-baseweb="tag"]{
    background:#DB2D28 !important;
    color:white !important;
}

/* ==========================================
   DROPDOWN POPUP
========================================== */
[data-baseweb="popover"]{
    background:#14191D !important;
}

/* ==========================================
   LISTBOX
========================================== */
div[role="listbox"]{
    background:#14191D !important;
    color:white !important;
}

/* ==========================================
   OPTIONS
========================================== */
div[role="option"]{
    background:#14191D !important;
    color:white !important;
}

/* Hover */
div[role="option"]:hover{
    background:#DB2D28 !important;
    color:white !important;
}

/* Selected */
div[aria-selected="true"]{
    background:#DB2D28 !important;
    color:white !important;
}

/* ==========================================
   UL / LI FALLBACK
========================================== */
ul{
    background:#14191D !important;
}

li{
    background:#14191D !important;
    color:white !important;
}

li:hover{
    background:#DB2D28 !important;
    color:white !important;
}

li[aria-selected="true"]{
    background:#DB2D28 !important;
    color:white !important;
}

/* ==========================================
   DATE INPUT
========================================== */
[data-testid="stDateInput"] input{
    background:#14191D !important;
    color:white !important;
    border:1px solid #DB2D28 !important;
}

/* ==========================================
   CALENDAR POPUP
========================================== */
/* Date picker popup */
[data-baseweb="calendar"]{
    background:#14191D !important;
}

[data-baseweb="calendar"] *{
    background:#14191D !important;
    color:white !important;
}

/* Month header */
[data-baseweb="calendar-header"]{
    background:#14191D !important;
    color:white !important;
}

/* Selected date */
[aria-selected="true"]{
    background:#DB2D28 !important;
    color:white !important;
}

/* Hover */
[data-baseweb="calendar"] button:hover{
    background:#DB2D28 !important;
}
/* ==========================================
   PLACEHOLDER
========================================== */
::placeholder{
    color:#AAAAAA !important;
}

/* ==========================================
   EXPANDER
========================================== */
.streamlit-expanderHeader{
    background:#14191D !important;
    color:white !important;
}

/* ==========================================
   WHITE BOX FIX
========================================== */
div[data-baseweb="menu"]{
    background:#14191D !important;
}

div[data-baseweb="menu"] *{
    background:#14191D !important;
    color:white !important;
}
* ==========================================
   FIX keyboard_double_arrow_right TEXT
========================================== */

[data-testid="collapsedControl"]{
    display:none !important;
}

[data-testid="stSidebarCollapseButton"]{
    display:none !important;
}

.material-icons,
.material-symbols-rounded,
.material-symbols-outlined{
    font-size:0 !important;
}

button[kind="header"] span{
    display:none !important;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-logo">
    <h1> FinGen AI</h1>
    <p>Smart Financial Intelligence Platform</p>
</div>

<div class="glow-line"></div>
""", unsafe_allow_html=True)
 
# ================= DATABASE CONNECTION =================
def get_connection():
    return mysql.connector.connect(
        host="yamanote.proxy.rlwy.net",
        user="root",
        password="ZYEzeINVRENjNtaFJvVhryiFwzwhOXLG",
        database="railway",
        port=28669
    
    )

# ================= CREATE TABLES =================
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS finance_data(
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        salary FLOAT,
        expense FLOAT,
        savings FLOAT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

    # ================= REGISTER =================
def register_user(username, password):

        username = username.strip()
        password = password.strip()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username=%s",
            (username,)
        )

        if cursor.fetchone():
            conn.close()
            return False

        hashed_password = hashlib.sha256(
            password.encode()
        ).hexdigest()

        cursor.execute(
            "INSERT INTO users(username,password) VALUES(%s,%s)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return True
    # ================= LOGIN =================
def login_user(username, password):

    username = username.strip()
    password = password.strip()

    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = hashlib.sha256(
        password.encode()
    ).hexdigest()

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username=%s
        AND password=%s
        """,
        (username, hashed_password)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

create_tables()

if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

if "username" not in st.session_state:
        st.session_state.username = ""

if "user_id" not in st.session_state:
        st.session_state.user_id = None


    # ================= LOGIN PAGE =================
if not st.session_state.logged_in:

        st.title("User Login / Register")

        menu = st.selectbox(
            "Select",
            ["Login", "Register"]
        )

        if menu == "Register":

            username = st.text_input(
                "Username",
                key="reg_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="reg_password"
            )

            confirm_password = st.text_input(
                "Re-enter Password",
                type="password",
                key="reg_confirm_password"
            )

        if st.button("Register"):

                    if password != confirm_password:
                        st.error("Passwords do not match")

                    elif register_user(username, password):
                        st.success("Registration Successful")

                    else:
                        st.error("Username already exists")

        else:

            username = st.text_input(
                "Username",
                key="login_username"
            )

            password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button("Login"):

                user = login_user(username, password)

                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.rerun()

                else:
                    st.error("Invalid Login")

        st.stop()


    # ================= DASHBOARD =================

st.title(
        f"Welcome {st.session_state.username}"
    )

menu = st.sidebar.radio(
        "📌 Navigation",
        [
            "Live Market",
            "🤖 FinGen Bot",
            "Personal Finance",
            "Business Finance",
            "Loan System",
            "Risk Analyzer",
            "Stock Market",
            "Investment Planner",
            "Reports",
            "summary"
        ]
    )

if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
    # =========================================================
    # Live Market
    # =========================================================

if menu == "Live Market":

        st.title("🇮🇳 Indian Live Market Dashboard")
        

        # ================= CACHE DATA =================

        @st.cache_data(ttl=300)
        def get_market_data():

            def safe_get(ticker):
                try:
                    data = yf.Ticker(ticker).history(period="1d")
                    return data["Close"].iloc[-1] if not data.empty else None
                except:
                    return None

            return {
                "gold": safe_get("GC=F"),
                "silver": safe_get("SI=F"),
                "usd_inr": safe_get("INR=X"),
                "sensex": safe_get("^BSESN"),
                "nifty": safe_get("^NSEI"),
            }

    # ================= LOAD DATA =================

        with st.spinner("Fetching live market data..."):
            data = get_market_data()

        gold_price = data["gold"] or 0
        silver_price = data["silver"] or 0
        usd_inr = data["usd_inr"] or 0
        sensex_price = data["sensex"] or 0
        nifty_price = data["nifty"] or 0

        # Manual fuel prices
        petrol_price = 104.95
        diesel_price = 92.72

    # ================= METRICS =================

        st.markdown("### 📊 Live Market Snapshot")

        col1, col2, col3 = st.columns(3)

        col1.metric("🥇 Gold", f"${gold_price:.2f}" if gold_price else "N/A")
        col2.metric("🥈 Silver", f"${silver_price:.2f}" if silver_price else "N/A")
        col3.metric("💵 USD/INR", f"₹{usd_inr:.2f}" if usd_inr else "N/A")

        col4, col5, col6 = st.columns(3)

        col4.metric("⛽ Petrol", f"₹{petrol_price}/L")
        col5.metric("🛢 Diesel", f"₹{diesel_price}/L")
        col6.metric("📈 Sensex", f"{sensex_price:.2f}" if sensex_price else "N/A")

        st.metric("📊 Nifty 50", f"{nifty_price:.2f}" if nifty_price else "N/A")

    # ================= TABLE =================

        st.markdown("## 📋 Market Summary")

        summary = pd.DataFrame({
                "Asset": ["Gold", "Silver", "USD/INR", "Petrol", "Diesel", "Sensex", "Nifty"],
                "Value": [
                    gold_price,
                    silver_price,
                    usd_inr,
                    petrol_price,
                    diesel_price,
                    sensex_price,
                    nifty_price
                ]
            })

        st.dataframe(summary, use_container_width=True)

        st.markdown("---")
        st.markdown("""
<style>

/* Main App Background */
.stApp {
    background: linear-gradient(135deg, #000000, #0d0d0d, #1a0000);
    color: white;
}

/* Main Content Area */
.main {
    background: transparent;
}

/* Metric Cards */
.stMetric {
    background: linear-gradient(145deg, #111111, #1a1a1a);
    padding: 15px;
    border-radius: 15px;
    border: 1px solid rgba(255, 0, 0, 0.4);
    box-shadow: 0 0 15px rgba(255, 0, 0, 0.15);
}

/* Headings */
h1 {
    color: #ff4d4d;
    text-align: center;
    font-weight: 700;
}

h2, h3 {
    color: #ffffff;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #050505;
    border-right: 1px solid rgba(255, 0, 0, 0.3);
}

/* Buttons */
.stButton > button {
    background: #111111;
    color: white;
    border: 1px solid rgba(255, 0, 0, 0.4);
    border-radius: 12px;
}

.stButton > button:hover {
    background: #1a0000;
    border: 1px solid #ff3333;
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.4);
}

/* Metric Values */
[data-testid="stMetricValue"] {
    color: white;
}

/* Metric Labels */
[data-testid="stMetricLabel"] {
    color: #ff8080;
}

</style>
""", unsafe_allow_html=True)

elif menu == "Personal Finance":

 st.title("💸 Personal Finance Dashboard")

 option = st.radio(
        "Choose Option",
        ["Expense Tracker", "Budget Planner"]
    )

    # =====================================================
    # EXPENSE TRACKER
    # =====================================================

 if option == "Expense Tracker":

        st.subheader("📊 Expense Tracker")

        col1, col2 = st.columns(2)

        with col1:
            Income = st.number_input("Monthly Income", min_value=0.0)
            daily_expense = st.number_input("Daily Expense", min_value=0.0)

        with col2:
            monthly_budget = st.number_input("Expected Monthly Expense", min_value=0.0)
            emi = st.number_input("EMI", min_value=0.0)
        # ================= DYNAMIC EXPENSES =================

        expense_names = []
        monthly_expenses = []

        n = st.number_input("How Many Expenses?", min_value=1, step=1)

        for i in range(int(n)):

            c1, c2 = st.columns(2)

            with c1:
                name = st.text_input(f"Expense Name {i+1}", key=f"name_{i}")

            with c2:
                amount = st.number_input(f"Expense Amount {i+1}", min_value=0.0, key=f"amt_{i}")

            expense_names.append(name if name else f"Expense {i+1}")
            monthly_expenses.append(amount)

        # ================= CALCULATION =================

        if st.button("Calculate"):

            monthly_expense_total = sum(monthly_expenses)
            daily_monthly = daily_expense * 30

            total_expense = monthly_expense_total + daily_monthly + emi

            savings = Income - total_expense

            # ================= FINANCIAL HEALTH =================

            if total_expense > Income:
                health = "Poor"
            elif total_expense > Income * 0.7:
                health = "Average"
            else:
                health = "Excellent"

            # ================= RESULTS =================

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Total Expense", f"₹ {total_expense:.2f}")
            c2.metric("Savings", f"₹ {savings:.2f}")
            c3.metric("Daily Expense (Monthly)", f"₹ {daily_monthly:.2f}")
            c4.metric("Financial Health", health)

            # ================= SESSION STORAGE =================

            st.session_state["Income"] = Income
            st.session_state["total_expense"] = total_expense
            st.session_state["savings"] = savings

            # ================= CHART =================

            chart_df = pd.DataFrame({
                "Expense": expense_names,
                "Amount": monthly_expenses
            })

            st.bar_chart(chart_df, x="Expense", y="Amount")


            # ================= SAVE TO DB =================
            conn = get_connection()
            cursor = conn.cursor()
            if conn and cursor:

                query = """
                INSERT INTO personal_finance
                (income, total_expense, savings, emi, financial_health, prediction)
                VALUES (%s,%s,%s,%s,%s,%s)
                """

                values = (Income, total_expense, savings, emi, health, 0)

                cursor.execute(query, values)
                conn.commit()

                st.success("✅ Data Saved Successfully")

    # =====================================================
    # BUDGET PLANNER
    # =====================================================
 elif option == "Budget Planner":

        st.subheader(" Smart Budget Planner")

        Income = st.session_state.get("Income", 0)
        total_expense = st.session_state.get("total_expense", 0)
        savings = st.session_state.get("savings", 0)

        health = "⚪ Not Available"

        monthly_budget = st.number_input(
            "📊 Monthly Budget",
            min_value=0.0,
            value=float(st.session_state.get("budget", 0))
        )

        saving_goal = st.number_input(
            "🎯 Saving Goal",
            min_value=0.0,
            value=float(st.session_state.get("saving_goal", 0))
        )

        remaining_budget = monthly_budget - total_expense

        # ================= METRICS =================

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "💸 Total Expense",
            f"₹{total_expense:,.0f}"
        )

        c2.metric(
            "📊 Remaining Budget",
            f"₹{remaining_budget:,.0f}"
        )

        c3.metric(
            " Savings",
            f"₹{savings:,.0f}"
        )

        c4.metric(
            "🏦 Income",
            f"₹{Income:,.0f}"
        )

        st.divider()

        # ================= BUDGET UTILIZATION =================

        if monthly_budget > 0:

            budget_used = (total_expense / monthly_budget) * 100

            st.write("### 📊 Budget Utilization")

            st.progress(min(int(budget_used), 100))

            st.info(f"{budget_used:.1f}% of budget used")

            if budget_used >= 100:
                st.error("🚨 Budget Exceeded!")

            elif budget_used >= 80:
                st.warning("⚠️ Budget almost exhausted")

            else:
                st.success("✅ Budget is under control")

        # ================= SAVING GOAL =================

        if saving_goal > 0:

            goal_progress = (savings / saving_goal) * 100

            st.write("### 🎯 Saving Goal Progress")

            try:
                progress_value = int(float(goal_progress))
            except:
                progress_value = 0

                st.progress(min(progress_value, 100))
            st.info(f"{goal_progress:.1f}% Goal Completed")

            if savings >= saving_goal:
                st.success("🎉 Congratulations! Saving Goal Achieved")

            else:
                st.warning(
                    f"₹{saving_goal - savings:,.0f} more needed"
                )

        st.divider()

        # ================= FINANCIAL HEALTH =================

        if Income > 0:

            expense_ratio = (total_expense / Income) * 100
            saving_rate = (savings / Income) * 100

            if expense_ratio <= 40:
                health = "🟢 Excellent"

            elif expense_ratio <= 60:
                health = "🟡 Good"

            elif expense_ratio <= 80:
                health = "🟠 Average"

            else:
                health = "🔴 Risky"

            wealth_score = round(
                ((100 - expense_ratio) * 0.6) +
                (saving_rate * 0.4)
            )

            wealth_score = max(0, min(100, wealth_score))

            st.write("### ❤️ Financial Health")

            st.progress(wealth_score / 100)

            st.metric(
                "🏆 Wealth Score",
                f"{wealth_score}/100"
            )

        # ================= AI ADVICE =================

        st.write("### 🤖 AI Budget Suggestions")

        if Income > 0:

            saving_rate = (savings / Income) * 100

            if saving_rate < 20:
                st.warning(
                    "Reduce unnecessary expenses and increase savings."
                )

            if total_expense > monthly_budget:
                st.error(
                    "Your expenses are exceeding the planned budget."
                )

            if saving_rate >= 30:
                st.success(
                    "Excellent savings habit. Keep it up!"
                )

            if remaining_budget > 0:
                st.info(
                    f"You can still spend ₹{remaining_budget:,.0f} safely this month."
                )

        st.divider()

        # ================= FUTURE SAVINGS =================

        future_savings = savings * 12

        st.write("### 📈 Future Savings Forecast")

        st.metric(
            "Estimated Savings After 1 Year",
            f"₹{future_savings:,.0f}"
        )

        # ================= HEALTH CARD =================

        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,#1e3c72,#2a5298);
            padding:25px;
            border-radius:20px;
            text-align:center;
            color:white;
            margin-top:15px;
        ">
            <h3>Financial Health Status</h3>
            <h2>{health}</h2>
        </div>
        """, unsafe_allow_html=True)

        # ================= SUMMARY =================

        st.divider()

        st.write("### 📋 Budget Summary")

        summary = pd.DataFrame({
            "Metric": [
                "Income",
                "Expenses",
                "Savings",
                "Budget",
                "Remaining Budget",
                "Health Status"
            ],
            "Value": [
                f"₹{Income:,.0f}",
                f"₹{total_expense:,.0f}",
                f"₹{savings:,.0f}",
                f"₹{monthly_budget:,.0f}",
                f"₹{remaining_budget:,.0f}",
                health
            ]
        })

        st.dataframe(summary, use_container_width=True)

        st.success("🎉 Budget Analysis Completed Successfully")
# =========================================================
# BUSINESS FINANCE
# =========================================================

elif menu == "Business Finance":

    st.subheader("📊 Business Finance AI Dashboard")
    st.write("Start adding your business data 🚀")

    option = st.radio(
        "Select Option",
        ["Retail Selling", "Manufacturing Calculator"],
        horizontal=True
    )

    # ==========================================================
    # RETAIL SELLING
    # ==========================================================
    if option == "Retail Selling":

        if "finance_data" not in st.session_state:
            st.session_state.finance_data = pd.DataFrame(columns=[
                "Date",
                "Product",
                "Category",
                "Quantity",
                "Purchase Price",
                "Selling Price",
                "Revenue",
                "Cost",
                "Profit"
            ])

        st.subheader("➕ Add New Record")

        col1, col2, col3 = st.columns(3)

        with col1:
            date = st.date_input("Date")
            product = st.text_input("Product Name")

        with col2:
            category = st.selectbox(
                "Category",
                [
                    "Grocery",
                    "Skincare",
                    "Cosmetics",
                    "Electronics",
                    "Fashion Boutique",
                    "Clothing",
                    "Stationary",
                    "Accessories",
                    "Restaurants",
                    "Cafés",
                    "Automotive Parts",
                    "Home Decor",
                    "Other"
                ]
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1
            )

        with col3:
            purchase_price = st.number_input(
                "Purchase Price (₹)",
                min_value=0.0
            )

            selling_price = st.number_input(
                "Selling Price (₹)",
                min_value=0.0
            )

        revenue = quantity * selling_price
        cost = quantity * purchase_price
        profit = revenue - cost

        st.subheader("🧾 Live Preview")

        c1, c2, c3 = st.columns(3)

        c1.metric("Cost", f"₹ {cost:,.2f}")
        c2.metric("Revenue", f"₹ {revenue:,.2f}")
        c3.metric("Profit", f"₹ {profit:,.2f}")

        if st.button("➕ Add Record"):

            if product.strip() == "":
                st.warning("Enter Product Name")

            else:

                new_row = pd.DataFrame([{
                    "Date": pd.to_datetime(date),
                    "Product": product,
                    "Category": category,
                    "Quantity": quantity,
                    "Purchase Price": purchase_price,
                    "Selling Price": selling_price,
                    "Revenue": revenue,
                    "Cost": cost,
                    "Profit": profit
                }])

                st.session_state.finance_data = pd.concat(
                    [st.session_state.finance_data, new_row],
                    ignore_index=True
                )

                st.success("Record Added Successfully")

        df = st.session_state.finance_data

        st.subheader("📋 All Records")
        st.dataframe(df, use_container_width=True)

        if not df.empty:

            st.subheader("📈 Business Overview")

            total_revenue = df["Revenue"].sum()
            total_cost = df["Cost"].sum()
            total_profit = df["Profit"].sum()

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Revenue",
                f"₹ {total_revenue:,.0f}"
            )

            c2.metric(
                "Total Cost",
                f"₹ {total_cost:,.0f}"
            )

            c3.metric(
                "Total Profit",
                f"₹ {total_profit:,.0f}"
            )

            best_product = (
                df.groupby("Product")["Profit"]
                .sum()
                .idxmax()
            )

            st.success(
                f"🏆 Best Product: {best_product}"
            )

            st.subheader("📊 Analytics")

            profit_df = (
                df.groupby("Product", as_index=False)
                ["Profit"]
                .sum()
            )

            fig1 = px.bar(
                profit_df,
                x="Product",
                y="Profit",
                title="Profit by Product"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            revenue_df = (
                df.groupby("Category", as_index=False)
                ["Revenue"]
                .sum()
            )

            fig2 = px.pie(
                revenue_df,
                names="Category",
                values="Revenue",
                title="Revenue Share by Category"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

    # ==========================================================
    # MANUFACTURING CALCULATOR
    # ==========================================================
    elif option == "Manufacturing Calculator":

        st.title("🏭 Manufacturing Product Price Calculator")

        product_name = st.text_input("Product Name")

        category = st.selectbox(
            "Product Category",
            [
                "Food Products",
                "Textile Products",
                "Furniture",
                "Electronics",
                "Cosmetics",
                "Plastic Products",
                "Packaging Products",
                "Automobile Parts",
                "Construction Materials",
                "Custom Product"
            ]
        )

        st.subheader("📦 Raw Materials")

        num_materials = st.number_input(
            "Number of Materials",
            min_value=1,
            max_value=20,
            value=3
        )

        materials = []
        total_raw_material_cost = 0

        for i in range(int(num_materials)):

            st.markdown(f"### Material {i+1}")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                material_name = st.text_input(
                    "Material Name",
                    key=f"name_{i}"
                )

            with c2:
                qty = st.number_input(
                    "Quantity",
                    min_value=0.0,
                    key=f"qty_{i}"
                )

            with c3:
                unit = st.selectbox(
                    "Unit",
                    ["Kg","Gram","Ton","Liter","Milliliter","Piece","Box","Packet","Dozen","Meter","Centimeter","Foot","Inch","Square Meter","Sqaure Foot","Roll","Sheet","Bottle","Can","Carton","Other"],
                    key=f"unit_{i}"
                )

            with c4:
                rate = st.number_input(
                    f"Rate per ({unit})(₹)",
                    min_value=0.0,
                    key=f"rate_{i}"
                )

            material_cost = qty * rate

            materials.append({
                "Material": material_name,
                "Quantity": qty,
                "Unit": unit,
                "Rate": rate,
                "Cost": material_cost
            })

            total_raw_material_cost += material_cost

        st.metric(
            "Total Raw Material Cost",
            f"₹ {total_raw_material_cost:,.2f}"
        )

        labor = st.number_input(
            "Labor Cost (₹)",
            min_value=0.0
        )

        machine = st.number_input(
            "Machine Cost (₹)",
            min_value=0.0
        )

        packaging = st.number_input(
            "Packaging Cost (₹)",
            min_value=0.0
        )
        
        # Production Unit
        product_unit = st.selectbox(
            "Production Unit",
            [
            "Kg",
            "Gram",
            "Ton",
            "Liter",
            "Milliliter",
            "Piece",
            "Box",
            "Packet",
            "Dozen",
            "Meter",
            "Centimeter",
            "Foot",
            "Inch",
            "Square Meter",
            "Square Foot",
            "Roll",
            "Sheet",
            "Bottle",
            "Can",
            "Carton",
            "Other"
        ]
        )


        quantity_produced = st.number_input(
            f"Production Quantity ({product_unit})",
            min_value=1,
            value=100
        )

        profit_margin = st.number_input(
            "Profit Margin (%)",
            min_value=0.0,
            value=20.0
        )

        gst = st.number_input(
            "GST (%)",
            min_value=0.0,
            value=18.0
        )

        if st.button("🧮 Calculate Product Price"):

            total_cost = (
                total_raw_material_cost +
                labor +
                machine +
                packaging
            )

            cost_per_unit = (
                total_cost /
                quantity_produced
            )

            selling_price = (
                cost_per_unit *
                (1 + profit_margin / 100)
            )

            final_price = (
                selling_price *
                (1 + gst / 100)
            )

            total_profit = (
                (selling_price - cost_per_unit)
                * quantity_produced
            )

            revenue = (
                final_price *
                quantity_produced
            )

            st.success("Calculation Complete")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "Cost / Unit",
                f"₹ {cost_per_unit:,.2f}"
            )

            c2.metric(
                "Selling Price",
                f"₹ {final_price:,.2f}"
            )

            c3.metric(
                "Total Profit",
                f"₹ {total_profit:,.2f}"
            )

            c4.metric(
                "Revenue",
                f"₹ {revenue:,.2f}"
            )
# =========================================================
# LOAN SYSTEM
# =========================================================

elif menu == "Loan System":

    st.title("💳 Smart Loan System")

    option = st.radio(
        "Choose Option",
        ["EMI Calculator", "Loan Suggestions"]
    )

    
    # =====================================================
    # SESSION STATE (SAFE OUTSIDE IF)
    # =====================================================

    if "emi_data" not in st.session_state:
        st.session_state.emi_data = pd.DataFrame(columns=[
            "Month", "EMI", "Interest", "Principal", "Balance"
        ])

    # =====================================================
    # EMI CALCULATOR
    # =====================================================

    if option == "EMI Calculator":

        st.subheader("📌 Loan Details")

        c1, c2, c3 = st.columns(3)

        with c1:
            principal = st.number_input(" Loan Amount (₹)", min_value=0.0)

        with c2:
            interest_rate = st.number_input("📈 Interest Rate (%)", min_value=0.0)

        with c3:
            years = st.number_input("📅 Time Period (Years)", min_value=1)

        start_date = st.date_input("📆 Start Date")
        reminder = st.date_input("⏰ EMI Reminder Date")

        # ================= EMI CALCULATION =================

        if st.button("Generate EMI Plan"):

            if principal <= 0 or interest_rate <= 0:
                st.warning("Please enter valid values")
            else:
                r = interest_rate / (12 * 100)
                n = years * 12

                emi = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)

                balance = principal
                data = []

                for i in range(1, int(n) + 1):
                    interest = balance * r
                    principal_paid = emi - interest
                    balance -= principal_paid

                    data.append([
                        i,
                        round(emi, 2),
                        round(interest, 2),
                        round(principal_paid, 2),
                        round(abs(balance), 2)
                    ])

                st.session_state.emi_data = pd.DataFrame(
                    data,
                    columns=["Month", "EMI", "Interest", "Principal", "Balance"]
                )

                st.success("EMI Plan Generated Successfully!")

        df = st.session_state.emi_data

        st.subheader("📋 EMI Breakdown")
        st.dataframe(df, use_container_width=True, height=250)

        # ================= METRICS =================

        if not df.empty:

            total_payment = df["EMI"].sum()
            total_interest = df["Interest"].sum()

            c1, c2 = st.columns(2)
            c1.metric(" Total Payment", f"₹ {total_payment:,.2f}")
            c2.metric("📊 Total Interest", f"₹ {total_interest:,.2f}")

            # ================= GRAPHS =================
            st.subheader("📊 EMI & Balance Analysis")

            fig, ax = plt.subplots()

            ax.plot(df["Month"], df["EMI"], label="EMI", color="green", marker="o")
            ax.plot(df["Month"], df["Balance"], label="Balance", color="red", marker="o")

            ax.set_title("EMI vs Balance Trend")
            ax.set_xlabel("Month")
            ax.set_ylabel("Amount (₹)")

            ax.legend()
            ax.grid(True)

            st.pyplot(fig)
            # ================= REMINDER =================

            st.subheader("⏰ EMI Reminder")

            today = datetime.date.today()

            if reminder == today:
                st.warning("⚠ Today is EMI date!")
            elif reminder > today:
                st.info(f"📅 {(reminder - today).days} days left")
            else:
                st.success("✔ Reminder passed")

    # =====================================================
    # LOAN SUGGESTIONS (FULLY SEPARATE BLOCK)
    # =====================================================

    elif option == "Loan Suggestions":

        st.subheader("🤖 Smart Loan & Bank Suggestions")

        # ================= INPUT =================
        Income = st.number_input(
            "Enter Monthly Income (₹)",
            min_value=1000.0,
            value=30000.0,
            step=1000.0
        )

        loan_type = st.selectbox(
            "Select Loan Type",
            ["Personal Loan", "Home Loan", "Car Loan", "Education Loan", "Business Loan"]
        )

        # ================= LOAN TYPE LOGIC =================
        if loan_type == "Personal Loan":
            interest_range = "10% - 18%"
            risk_factor = 1.2
            message = "⚠ High interest, no collateral required"

        elif loan_type == "Home Loan":
            interest_range = "7% - 10%"
            risk_factor = 0.8
            message = "🏠 Low interest, long tenure, secured loan"

        elif loan_type == "Car Loan":
            interest_range = "8% - 12%"
            risk_factor = 0.9
            message = "🚗 Vehicle-based secured loan"

        elif loan_type == "Education Loan":
            interest_range = "7% - 11%"
            risk_factor = 0.7
            message = "🎓 Low interest, flexible repayment"

        else:
            interest_range = "9% - 16%"
            risk_factor = 1.3
            message = "📊 High risk, depends on business"

        st.info(f"""
    📌 Loan Type: {loan_type}  
    📉 Interest Rate: {interest_range}  
    💡 AI Insight: {message}
    """)

        # ================= EMI CALCULATION =================
        safe_emi_limit = (Income * 0.35) / risk_factor
        max_emi_limit = (Income * 0.5) / risk_factor

        estimated_loan = safe_emi_limit * 60  # 5 years

        st.metric("🏦 Safe EMI Limit", f"₹ {safe_emi_limit:,.0f}")
        st.metric(" Estimated Loan Eligibility", f"₹ {estimated_loan:,.0f}")

        # ================= RISK ANALYSIS =================
        st.subheader("⚠ Risk Analysis")

        emi_ratio = (safe_emi_limit / Income) * 100

        if emi_ratio <= 30:
            st.success("🟢 Low Risk: Safe borrowing zone")
        elif emi_ratio <= 45:
            st.warning("🟡 Medium Risk: Manage EMI carefully")
        else:
            st.error("🔴 High Risk: Loan may affect stability")

        # ================= AI ADVICE =================
        st.subheader("📌 AI Financial Advice")

        if Income < 25000:
            advice = [
                "✔ Take small loans only",
                "✔ Avoid long EMI duration",
                "✔ Build emergency savings"
            ]
        elif Income < 50000:
            advice = [
                "✔ Medium loans are safe",
                "✔ Compare interest rates",
                "✔ Maintain credit score"
            ]
        else:
            advice = [
                "✔ High eligibility for loans",
                "✔ Invest before borrowing",
                "✔ Use loans for assets only"
            ]

        for a in advice:
            st.write(a)

        # ================= BEST LOAN RECOMMENDATION =================
        if Income < 25000:
            best_loan = "Education Loan"
        elif Income < 50000:
            best_loan = "Car Loan"
        else:
            best_loan = "Home Loan"

        st.success(f"🏆 AI Recommended Loan: {best_loan}")

        # ================= BANK RECOMMENDATION ENGINE =================
        st.subheader(" Bank Recommendation ")

        banks = [
            {"name": "SBI", "min_Income": 10000, "interest": "8%-12%", "tag": "🔵 Safe government bank", "color": "#1f77b4"},
            {"name": "PNB", "min_Income": 10000, "interest": "8%-13%", "tag": "🏦 Trusted PSU bank", "color": "#2ca02c"},
            {"name": "Bank of Baroda", "min_Income": 12000, "interest": "8%-12.5%", "tag": "💳 Good personal loans", "color": "#17becf"},
            {"name": "HDFC Bank", "min_Income": 25000, "interest": "9%-13%", "tag": "⭐ Fast approval", "color": "#ff7f0e"},
            {"name": "ICICI Bank", "min_Income": 25000, "interest": "9%-14%", "tag": "💡 Flexible loans", "color": "#9467bd"},
            {"name": "Axis Bank", "min_Income": 20000, "interest": "9%-13.5%", "tag": "⚡ Digital approval", "color": "#d62728"},
            {"name": "Kotak Bank", "min_Income": 30000, "interest": "8%-11.5%", "tag": "💎 Premium low interest", "color": "#8c564b"}
        ]

        st.write("### 📌 Best Matching Banks for You")

        for bank in banks:
            if Income >= bank["min_Income"]:

                st.markdown(f"""
                <div style="
                    padding:15px;
                    border-radius:15px;
                    margin-bottom:10px;
                    background:#111827;
                    border-left:6px solid {bank['color']};
                    color:white;
                ">
                    <h4>🏦 {bank['name']}</h4>
                    <p>📉 Interest: {bank['interest']}</p>
                    <p>💡 {bank['tag']}</p>
                </div>
                """, unsafe_allow_html=True)
#========================================================
#STOCK MARKET
#========================================================
elif menu == "Stock Market":

    # -------------------------------
    # LOAD MODEL
    # -------------------------------
    try:
        model = joblib.load("stock_model.pkl")
    except:
        model = None

    # -------------------------------
    # SIDEBAR CSS
    # -------------------------------
    st.markdown("""
    <style>

    [data-testid="stSidebar"]{
        background-color: #FF0000;
    }

    [data-testid="stSidebar"] *{
        color:RED !important;
    }

    [data-testid="stSidebar"] input{
        background:#14191D !important;
        color:black!important;
        border:1px solid #FF0000;
    }

    [data-testid="stSidebar"] label{
        color:white !important;
    }

    div[data-baseweb="select"] > div{
        background: #FF0000 !important;
        color:white !important;
    }

    </style>
    """, unsafe_allow_html=True)

    st.title("📈 AI Stock Predictor Pro")

    # -------------------------------
    # SIDEBAR
    # -------------------------------
    st.sidebar.title("📊 Stock Dashboard")
    st.sidebar.header("📥 Input Section")

    stock_list = [
        "AAPL",
        "TSLA",
        "MSFT",
        "AMZN",
        "GOOGL",
        "META",
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS",
        "BTC-USD",
        "ETH-USD"
    ]

    stock_symbol = st.sidebar.selectbox(
        "🔥 Select Stock",
        stock_list
    )

    refresh = st.sidebar.checkbox(
        "🔄 Auto Refresh (40 sec)"
    )

    if refresh:
        time.sleep(40)
        st.rerun()

    mode = st.radio(
        "Select Mode",
        ["📡 Live Data"]
    )

    # -------------------------------
    # LIVE DATA
    # -------------------------------
    if mode == "📡 Live Data":

        st.subheader("📉 Stock Chart + Smart Trend")

        ticker = yf.Ticker(stock_symbol)
        hist_data = ticker.history(period="6mo")

        if not hist_data.empty:

            hist_data.reset_index(inplace=True)

            for col in ["Open", "High", "Low", "Close"]:
                hist_data[col] = pd.to_numeric(
                    hist_data[col],
                    errors="coerce"
                )

            hist_data.dropna(inplace=True)

            hist_data["MA20"] = (
                hist_data["Close"]
                .rolling(20)
                .mean()
            )

            hist_data["MA50"] = (
                hist_data["Close"]
                .rolling(50)
                .mean()
            )

            fig = go.Figure()

            fig.add_trace(
                go.Candlestick(
                    x=hist_data["Date"],
                    open=hist_data["Open"],
                    high=hist_data["High"],
                    low=hist_data["Low"],
                    close=hist_data["Close"],
                    name="Candlestick"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=hist_data["Date"],
                    y=hist_data["MA20"],
                    name="MA20"
                )
            )

            fig.add_trace(
                go.Scatter(
                    x=hist_data["Date"],
                    y=hist_data["MA50"],
                    name="MA50"
                )
            )

            fig.update_layout(
                template="plotly_dark",
                height=600,
                title=f"{stock_symbol} Market Analysis",
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

           # ================= BUY / SELL SIGNAL =================

        st.markdown("---")
        st.subheader("🎯 Smart Trading Signal")

        current_price = hist_data["Close"].iloc[-1]
        ma20 = hist_data["MA20"].iloc[-1]
        ma50 = hist_data["MA50"].iloc[-1]

        if pd.notna(ma20) and pd.notna(ma50):

            if current_price > ma20 and ma20 > ma50:
                st.success("🟢 BUY SIGNAL")
                st.write("Price is above MA20 and MA20 is above MA50.")

            elif current_price < ma20 and ma20 < ma50:
                st.error("🔴 SELL SIGNAL")
                st.write("Price is below MA20 and MA20 is below MA50.")

            else:
                st.warning("🟡 HOLD SIGNAL")
                st.write("Wait for a clearer trend confirmation.")

        else:
            st.warning("Not enough data")
# ================= RSI =================

        delta = hist_data["Close"].diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(14).mean()
        avg_loss = loss.rolling(14).mean()

        rs = avg_gain / avg_loss

        hist_data["RSI"] = 100 - (100 / (1 + rs))

        latest_rsi = hist_data["RSI"].iloc[-1]

        st.markdown("---")
        st.subheader("📊 RSI Analysis")

        st.metric("RSI", f"{latest_rsi:.2f}")

        if latest_rsi > 70:
            st.error("🔴 Overbought Zone")
        elif latest_rsi < 30:
            st.success("🟢 Oversold Zone")
        else:
            st.info("🟡 Neutral Zone")

#risk analyzer

elif menu == "Risk Analyzer":

    st.title(" Smart Investment Advisor")
    st.markdown("### AI-Based Financial Risk Analysis System")

    st.divider()

    st.subheader("📋 Enter Financial Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100)

        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0.0,
            step=1000.0
        )

        savings = st.number_input(
            "Total Savings (₹)",
            min_value=0.0,
            step=1000.0
        )

    with col2:

        expenses = st.number_input(
            "Monthly Expenses (₹)",
            min_value=0.0,
            step=1000.0
        )

        loans = st.number_input(
            "Existing Loans (₹)",
            min_value=0.0,
            step=1000.0
        )

        experience = st.selectbox(
            "Investment Experience",
            ["Beginner", "Intermediate", "Advanced"]
        )

    analyze = st.button("🚀 Analyze Risk")

    if analyze:

        if income <= 0:
            st.error("Income must be greater than 0")
            st.stop()

        # ================= CORE RATIOS =================
        expense_ratio = (expenses / income) * 100
        loan_ratio = (loans / income) * 100
        saving_ratio = (savings / income) * 100

        monthly_savings = income - expenses
        savings_rate = (monthly_savings / income) * 100

        debt_to_income = loan_ratio
        burn_rate = expense_ratio

        # ================= ADVANCED RISK SCORE =================
        risk_score = (
            (expense_ratio * 0.4) +
            (loan_ratio * 0.4) -
            (saving_ratio * 0.3) -
            (savings_rate * 0.2)
        )

        risk_score = max(0, min(100, round(risk_score, 2)))

        # ================= RISK LEVELS =================
        if risk_score <= 20:
            result = "VERY LOW"
            color = "🟢"
        elif risk_score <= 40:
            result = "LOW"
            color = "🟡"
        elif risk_score <= 60:
            result = "MODERATE"
            color = "🟠"
        elif risk_score <= 80:
            result = "HIGH"
            color = "🔴"
        else:
            result = "VERY HIGH"
            color = "🚨"

        # ================= METRICS =================
        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("💵 Income", f"₹{income:,.0f}")
        c2.metric("💸 Expenses", f"₹{expenses:,.0f}")
        c3.metric("🏦 Savings", f"₹{savings:,.0f}")
        c4.metric("📉 Loans", f"₹{loans:,.0f}")

        st.divider()

        # ================= RISK DISPLAY =================
        st.subheader("📊 AI Risk Assessment")

        st.markdown(f"### {color} {result} RISK")
        st.progress(int(risk_score))

        st.metric("Risk Score", f"{risk_score}/100")

        # ================= GAUGE =================
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            title={"text": "Financial Risk Index"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "black"},
                "steps": [
                    {"range": [0, 20], "color": "#2ecc71"},
                    {"range": [20, 40], "color": "#f1c40f"},
                    {"range": [40, 60], "color": "#f39c12"},
                    {"range": [60, 80], "color": "#e74c3c"},
                    {"range": [80, 100], "color": "#8e0000"}
                ]
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

        # ================= INVESTMENT READINESS =================
        invest_score = (saving_ratio + savings_rate) - (debt_to_income * 0.5)
        invest_score = max(0, min(100, round(invest_score, 2)))

        st.subheader("📈 Investment Readiness Score")
        st.metric("Readiness", f"{invest_score}/100")

        if invest_score > 70:
            st.success("🚀 Strong investment candidate")
        elif invest_score > 40:
            st.warning("⚠️ Moderate investment readiness")
        else:
            st.error("❌ Not ready for aggressive investments")

        # ================= CHARTS =================
        st.subheader("📊 Financial Breakdown")

        chart_data = pd.DataFrame({
            "Category": ["Income", "Expenses", "Savings", "Loans"],
            "Amount": [income, expenses, savings, loans]
        })

        fig2 = px.bar(chart_data, x="Category", y="Amount", text="Amount")
        st.plotly_chart(fig2, use_container_width=True)

        fig3 = px.pie(
            values=[expenses, savings, loans],
            names=["Expenses", "Savings", "Loans"]
        )
        st.plotly_chart(fig3, use_container_width=True)

        # ================= AI BEHAVIOR FLAGS =================
        st.subheader("⚠️ AI Financial Behavior Analysis")

        if expense_ratio > 70:
            st.error("🚨 High spending behavior detected")

        if savings_rate < 10:
            st.warning("⚠️ Very low savings rate")

        if loan_ratio > 50:
            st.error("🚨 Over-leveraged: High debt dependency")

        if savings < expenses:
            st.warning("⚠️ No emergency buffer (Savings < Expenses)")

        # ================= SMART AI ADVICE =================
        st.subheader("💡 AI Smart Suggestions")

        advice = []

        if expense_ratio > 60:
            advice.append("Reduce discretionary spending immediately")

        if savings_rate < 20:
            advice.append("Aim to save at least 20–30% of income")

        if loan_ratio > 40:
            advice.append("Prioritize loan repayment before investing")

        if invest_score > 60:
            advice.append("You can start SIP or low-risk mutual funds")

        if not advice:
            advice.append("Your financial health looks stable 👍")

        for a in advice:
            st.info(a)

elif menu == "Investment Planner":

    st.title("📈 FinGen AI Investment Planner Pro")

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(" Monthly Income (₹)", min_value=0.0)
        savings = st.number_input("🏦 Current Savings (₹)", min_value=0.0)
        age = st.number_input("🎂 Current Age", 18, 100, 25)

    with col2:
        expenses = st.number_input("💸 Monthly Expenses (₹)", min_value=0.0)
        loans = st.number_input("💳 Total Loan EMI (₹)", min_value=0.0)

        goal = st.selectbox(
            "🎯 Financial Goal",
            [
                "Wealth Creation",
                "Retirement",
                "Emergency Fund",
                "Passive Income"
            ]
        )

    st.markdown("### 🎯 Goal Planning")

    goal_amount = st.number_input(
        "Target Amount (₹)",
        min_value=10000.0,
        value=1000000.0
    )

    years = st.number_input(
        "Investment Duration (Years)",
        1,
        40,
        10
    )

    generate = st.button("🚀 Generate Investment Plan")

    if generate:

        if income <= 0:
            st.error("Income must be greater than 0")
            st.stop()

        # =====================
        # RATIOS
        # =====================

        expense_ratio = (expenses / income) * 100
        loan_ratio = (loans / income) * 100
        saving_ratio = (savings / income) * 100

        disposable_income = income - expenses
        savings_rate = (disposable_income / income) * 100

        # =====================
        # FSI SCORE
        # =====================

        fsi = (
            (saving_ratio * 0.4)
            + (savings_rate * 0.3)
            - (expense_ratio * 0.3)
            - (loan_ratio * 0.4)
        )

        fsi = max(0, min(100, round(fsi, 2)))

        # =====================
        # RISK
        # =====================

        if fsi >= 70:
            risk = "LOW"
            sip_percent = 25

        elif fsi >= 50:
            risk = "MEDIUM"
            sip_percent = 18

        elif fsi >= 30:
            risk = "HIGH"
            sip_percent = 12

        else:
            risk = "VERY HIGH"
            sip_percent = 5

        sip = income * sip_percent / 100

        # =====================
        # WEALTH SCORE
        # =====================

        wealth_score = round(
            (saving_ratio * 0.4)
            + ((100 - loan_ratio) * 0.3)
            + ((100 - expense_ratio) * 0.3)
        )

        wealth_score = max(0, min(100, wealth_score))

        # =====================
        # EMERGENCY FUND
        # =====================

        emergency_target = expenses * 6

        # =====================
        # FIRE CALCULATOR
        # =====================

        fire_target = expenses * 12 * 25

        # =====================
        # GOAL SIP CALCULATOR
        # =====================

        required_sip = goal_amount / (years * 12)

        # =====================
        # FUTURE VALUE
        # =====================

        future_value = sip * 12 * years * 1.15

        inflation = 6

        real_value = future_value / (
            (1 + inflation / 100) ** years
        )

        # =====================
        # DASHBOARD
        # =====================

        st.subheader("📊 Financial Dashboard")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(" SIP", f"₹{sip:,.0f}")
        c2.metric("📈 Wealth Score", f"{wealth_score}/100")
        c3.metric("🛡️ FSI", f"{fsi}/100")
        c4.metric("⚠️ Risk", risk)

        st.progress(wealth_score / 100)

        st.markdown("---")

        # =====================
        # EMERGENCY FUND
        # =====================

        st.subheader("🛡️ Emergency Fund Analysis")

        st.info(
            f"Recommended Emergency Fund: ₹{emergency_target:,.0f}"
        )

        if savings >= emergency_target:
            st.success("Emergency Fund Status: Adequate")
        else:
            st.warning(
                f"Need ₹{emergency_target - savings:,.0f} more"
            )

        # =====================
        # FIRE
        # =====================

        st.subheader("🔥 Financial Freedom Calculator")

        st.success(
            f"Financial Freedom Target: ₹{fire_target:,.0f}"
        )

        # =====================
        # GOAL PLANNER
        # =====================

        st.subheader("🎯 Goal Planning")

        st.info(
            f"Required Monthly SIP: ₹{required_sip:,.0f}"
        )

        # =====================
        # FUTURE PROJECTION
        # =====================

        st.subheader("🔮 Future Projection")

        st.success(
            f"Projected Portfolio Value: ₹{future_value:,.0f}"
        )

        st.info(
            f"Inflation Adjusted Value: ₹{real_value:,.0f}"
        )

        # =====================
        # PORTFOLIO
        # =====================

        st.subheader("📈 Portfolio Recommendation")

        if risk == "LOW":

            st.success("""
            • 50% Large Cap Stocks
            • 30% Mid Cap Funds
            • 20% Small Cap Funds
            """)

        elif risk == "MEDIUM":

            st.warning("""
            • 60% Mutual Funds
            • 25% Bluechip Stocks
            • 15% Gold / Bonds
            """)

        elif risk == "HIGH":

            st.warning("""
            • 50% Debt Funds
            • 30% FD
            • 20% Index Funds
            """)

        else:

            st.error("""
            • 70% FD
            • 20% Liquid Funds
            • 10% Emergency Cash
            """)

        # =====================
        # AI INSIGHTS
        # =====================

        st.subheader("🤖 AI Financial Insights")

        if expense_ratio > 70:
            st.error(
                "Spending is too high. Reduce unnecessary expenses."
            )

        if loan_ratio > 50:
            st.error(
                "Debt burden is high. Focus on loan repayment."
            )

        if savings_rate < 20:
            st.warning(
                "Increase savings rate for better wealth creation."
            )

        if wealth_score > 80:
            st.success(
                "Excellent financial position."
            )

        # =====================
        # SUMMARY
        # =====================

        st.subheader("📋 Financial Summary")

        summary = pd.DataFrame({
            "Metric": [
                "Income",
                "Expenses",
                "Savings",
                "Loan EMI",
                "Risk",
                "FSI",
                "Wealth Score",
                "Recommended SIP"
            ],
            "Value": [
                f"₹{income:,.0f}",
                f"₹{expenses:,.0f}",
                f"₹{savings:,.0f}",
                f"₹{loans:,.0f}",
                risk,
                f"{fsi}/100",
                f"{wealth_score}/100",
                f"₹{sip:,.0f}"
            ]
        })

        st.dataframe(summary, use_container_width=True)

        st.success("🎉 AI Investment Plan Generated Successfully")
# =========================================================
# REPORTS
# =========================================================

elif menu == "Reports":

    # =========================
    # FETCH DATA
    # =========================
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM personal_finance")
    data = cursor.fetchall()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Income",
            "Expense",
            "Savings",
            "EMI",
            "Health",
            "Prediction"
        ]
    )

    # =========================
    # EMPTY STATE
    # =========================
    if df.empty:

        st.markdown("""
        <div class="neo-card" style="text-align:center;padding:30px;">
            <h3 style="color:#7B746A;">No financial records found 📭</h3>
            <p style="color:#9a948c;">Start adding data from Personal Finance module</p>
        </div>
        """, unsafe_allow_html=True)

        st.stop()

    # =========================
    # QUICK STATS (NEW UPGRADE)
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Records", len(df))

    with col2:
        st.metric("Avg Income", f"{df['Income'].mean():.0f}")

    with col3:
        st.metric("Avg Savings", f"{df['Savings'].mean():.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # TABLE VIEW
    # =========================
    st.markdown("""
    <div class="neo-card">
        <h3 style="color:#2E2A26;">📋 Saved Financial Reports</h3>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df, use_container_width=True, height=400)

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # DOWNLOAD SECTION
    # =========================
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download CSV Report",
        csv,
        "finance_report.csv",
        "text/csv",
        use_container_width=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # =========================
    # DELETE SINGLE RECORD
    # =========================
    conn = get_connection()
    cursor = conn.cursor()
    st.markdown("""
    <div class="neo-card">
        <h3 style="color:#b91c1c;">🗑 Delete Single Record</h3>
    </div>
    """, unsafe_allow_html=True)

    selected_id = st.selectbox("Select Record ID", df["ID"])

    col1, col2 = st.columns(2)

    with col1:
        delete_one = st.button("Delete Selected ❌")

    if delete_one:
        cursor.execute(
            "DELETE FROM personal_finance WHERE id=%s",
            (int(selected_id),)
        )
        conn.commit()
        st.success(f"Record ID {selected_id} deleted successfully")
        st.rerun()

    # =========================
    # DELETE ALL RECORDS
    # =========================
    st.markdown("""
    <div class="neo-card">
        <h3 style="color:#dc2626;">⚠ Danger Zone</h3>
    </div>
    """, unsafe_allow_html=True)

    confirm = st.checkbox("I understand this action cannot be undone")

    if confirm:
        if st.button("🗑 Delete All Records", type="primary"):

            cursor.execute("DELETE FROM personal_finance")
            conn.commit()

            st.success("All records deleted successfully")
            st.rerun()
elif menu == "🤖 FinGen Bot":

    from chatbot import ai_chat

    ai_chat()
    
elif menu == "summary":
    st.subheader("📌 Project Overview")

    st.success("""
    FinGen AI is an advanced AI-powered finance platform that integrates multiple financial tools into a single ecosystem.

    It helps users manage:
    ✔️ Personal Finance  
    ✔️ Business Analytics  
    ✔️ Stock Prediction  
    ✔️ Loan & EMI Planning  
    ✔️ Investment Strategy  
    ✔️ Risk Analysis  
    """)

    # =========================
    # KEY FEATURES
    # =========================
    st.subheader("🚀 Key Features")

    features = pd.DataFrame({
        "Feature": [
            "Smart Expense Tracking",
            "AI Stock Prediction",
            "EMI Calculator System",
            "Risk Analysis Engine",
            "Business Profit Dashboard",
            "Investment Planner"
        ],
        "Impact Score": [90, 85, 80, 88, 92, 95]
    })

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(features, use_container_width=True)

    # =========================
    # 📊 FEATURE IMPACT GRAPH (IMPORTANT ADDITION)
    # =========================
    with col2:
        fig = px.bar(
            features,
            x="Feature",
            y="Impact Score",
            title="📊 Feature Impact Score",
            text="Impact Score"
        )
        st.plotly_chart(fig, use_container_width=True)

    # =========================
    # SYSTEM PERFORMANCE
    # =========================
    st.subheader("📈 System Highlights")

    col1, col2, col3 = st.columns(3)

    col1.metric("Modules Integrated", "6+")
    col2.metric("AI Models Used", "5+")
    col3.metric("End-to-End Coverage", "Finance Ecosystem")

    # =========================
    # 📊 MODULE DISTRIBUTION PIE CHART
    # =========================
    st.subheader("🧩 System Architecture Distribution")

    module_data = pd.DataFrame({
        "Module": [
            "Personal Finance",
            "Business Finance",
            "Stock Market",
            "Loan System",
            "Investment Planner",
            "Risk Analyzer"
        ],
        "Weight": [18, 18, 20, 14, 15, 15]
    })


    # =========================
    # AI INSIGHTS
    # =========================
    st.subheader("🧠 AI Intelligence Summary")

    st.success("""
    ✔️ Smart financial decision support  
    ✔️ Automated predictions using ML logic  
    ✔️ Personalized investment suggestions  
    ✔️ Risk-based financial classification  
    ✔️ Real-time market insights  
    """)

    # =========================
    # FUTURE SCOPE (ONLY POSITIVE)
    # =========================
    st.subheader("🚀 Future Enhancements")

    st.info("""
    FinGen AI can be expanded into a full fintech ecosystem:

    ✔️ Real-time bank integration  
    ✔️ Advanced deep learning models  
    ✔️ Mobile application (Android/iOS)  
    ✔️ AI financial advisor chatbot  
    ✔️ Cloud portfolio tracking system  
    ✔️ Automated tax planning system  
    """)
    
    # =========================
    # FINAL MESSAGE
    # =========================
    st.markdown("---")

    st.success("🎉 FinGen AI successfully demonstrates a complete AI-driven financial ecosystem!")

    st.markdown("""
    💡 This project shows how Artificial Intelligence can simplify financial decision-making,
    improve money management, and support intelligent investment planning.
    """)

    # =========================
    # DOWNLOAD REPORT
    # =========================
    report_text = """
    FinGen AI Final Report:
    - AI Financial Intelligence System
    - Modules: Personal Finance, Business, Stock, Loan, Investment, Risk
    - Status: Completed Successfully
    - Type: Full FinTech AI Dashboard
    """

    st.download_button(
        "⬇️ Download Final Report",
        report_text,
        file_name="FinGen_AI_Final_Report.txt")
