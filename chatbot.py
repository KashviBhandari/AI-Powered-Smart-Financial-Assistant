import streamlit as st
import yfinance as yf
from groq import Groq
from dotenv import load_dotenv
import os
st.markdown("""
<style>

.stApp{
    background:#020617;
}

.block-container{
    max-width:1200px;
}

h1,h2,h3{
    color:white;
}

.action-card{
    background:#111827;
    padding:20px;
    border-radius:16px;
    text-align:center;
    color:white;
    border:1px solid #1f2937;
    transition:0.3s;
}

.action-card:hover{
    transform:translateY(-4px);
    border-color:#3b82f6;
}

</style>
""", unsafe_allow_html=True)
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
phi_key = os.getenv("PHI_API_KEY")
geminai_key = os.getenv("GEMINAI_API_KE")
if not groq_key:
    raise ValueError("GROQ_API_KEY not loaded from .env file")

client = Groq(api_key=groq_key)
# Initialize Groq client

def get_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return None

        return round(data["Close"].iloc[-1], 2)

    except:
        return None


# -------------------------
# AI FUNCTION
# -------------------------
def ask_ai(question):

    symbol = None

    words = question.upper().split()

    for w in words:
        if len(w) <= 5 and w.isalpha():
            symbol = w

    stock_info = ""

    if symbol:
        price = get_stock_price(symbol)

        if price:
            stock_info = f"\nCurrent stock price of {symbol}: ${price}\n"

    prompt = f"""
You are FinGen AI, a professional finance assistant.

User Question:
{question}

{stock_info}

Rules:
- Use stock data if available
- Answer finance related questions professionally
- Keep answers short and clear
- Give investment insights when possible
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# -------------------------
# MAIN CHAT FUNCTION
# -------------------------
def ai_chat():

    st.subheader("🤖 FinGen Bot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input(
        "Ask about stocks, crypto, mutual funds, finance..."
    )

    if user_input:

        answer = ask_ai(user_input)

        st.session_state.chat_history.append(
            ("user", user_input)
        )

        st.session_state.chat_history.append(
            ("assistant", answer)
        )

    for role, msg in st.session_state.chat_history:

        with st.chat_message(role):
            st.write(msg)