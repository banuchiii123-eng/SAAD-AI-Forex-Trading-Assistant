
import streamlit as st
from groq import Groq
import os

# ==========================================
# BANUCHI - AI FOREX TRADING ASSISTANT
# ==========================================

st.set_page_config(
    page_title="BANUCHI | AI Forex Assistant",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #ffffff;
}

[data-testid="stSidebar"] {
    background-color: #111b2e;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #20c997;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #a0aec0;
    font-size: 16px;
}

.stChatMessage {
    border-radius: 12px;
}

div.stButton > button {
    background-color: #20c997;
    color: #06121f;
    border-radius: 8px;
    border: none;
    font-weight: bold;
}

div.stButton > button:hover {
    background-color: #16a085;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are BANUCHI, a professional AI Forex Trading
Education and Analysis Assistant.

Your purpose is to help users understand Forex trading
and improve their trading knowledge.

YOUR EXPERTISE:

1. Forex market fundamentals.
2. Technical analysis.
3. Candlestick patterns.
4. Support and resistance.
5. Market structure.
6. Smart Money Concepts (SMC).
7. ICT trading concepts.
8. RSI, MACD, EMA and moving averages.
9. Supply and demand zones.
10. Risk and money management.
11. Trading psychology.
12. Trading strategies.
13. Price action.
14. Trading plans and journaling.

IMPORTANT RULES:

- Always communicate professionally.
- Explain difficult concepts in simple language.
- Give examples whenever useful.
- Use headings and bullet points.
- Explain both advantages and disadvantages of strategies.
- Never guarantee profits.
- Never claim that a trade is 100% safe.
- Never invent live market prices or economic news.
- You do not have live Forex market data unless the
  user provides it in the conversation.
- If the user shares a chart or market data, analyze
  only what you can actually observe.
- Explain entry, stop loss and take profit concepts
  as educational examples, not guaranteed signals.
- Always emphasize risk management.
- Never encourage excessive leverage.
- Never tell users to risk money they cannot afford
  to lose.
- Clearly explain uncertainty in market analysis.

YOUR PERSONALITY:

Your name is BANUCHI.
You are friendly, intelligent, professional and helpful.
You are a dedicated Forex trading learning assistant.

When a user asks a Forex question, provide a clear,
structured and educational answer.

If a question is unrelated to Forex, you can still
help politely.
"""

# ==========================================
# API CONFIGURATION
# ==========================================

st.sidebar.title("⚙️ BANUCHI Settings")

api_key = None

try:
    api_key = st.secrets.get("GROQ_API_KEY")
except Exception:
    api_key = None

if not api_key:
    api_key = st.sidebar.text_input(
        "Enter Groq API Key",
        type="password",
        help="Get your API key from console.groq.com"
    )

MODEL = "openai/gpt-oss-20b"

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("---")

st.sidebar.markdown("### 📈 Trading Assistant")

st.sidebar.info(
    "BANUCHI is your AI-powered Forex trading "
    "education and analysis companion."
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🧠 Available Topics")

topics = [
    "Forex Basics",
    "Technical Analysis",
    "Candlestick Patterns",
    "Smart Money Concepts",
    "ICT Concepts",
    "Risk Management",
    "Trading Psychology",
    "Price Action",
    "Trading Strategies"
]

for topic in topics:
    st.sidebar.write("📌 " + topic)

st.sidebar.markdown("---")

if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

st.sidebar.caption("Powered by Groq AI")
st.sidebar.caption("Model: openai/gpt-oss-20b")

# ==========================================
# MAIN HEADER
# ==========================================

st.markdown(
    '<div class="main-title">📈 BANUCHI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your Personal AI Forex Trading Assistant'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# WELCOME SCREEN
# ==========================================

if not st.session_state.messages:

    st.markdown("## 👋 Welcome to BANUCHI!")

    st.write(
        "I am your AI Forex trading assistant. "
        "Ask me anything about the Forex market, "
        "technical analysis, trading strategies "
        "or risk management."
    )

    st.markdown("### 💡 Try asking me:")

    suggestions = [
        "What is Forex trading?",
        "Explain Smart Money Concepts (SMC).",
        "How does RSI indicator work?",
        "Explain support and resistance.",
        "What is a good risk management strategy?",
        "Explain the ICT trading concepts."
    ]

    for suggestion in suggestions:
        if st.button(suggestion, use_container_width=True):
            st.session_state.pending_question = suggestion
            st.rerun()

# ==========================================
# DISPLAY CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================
# CHAT INPUT
# ==========================================

pending = st.session_state.pop("pending_question", None)

user_input = st.chat_input(
    "Ask BANUCHI anything about Forex trading..."
)

if pending:
    user_input = pending

# ==========================================
# GROQ AI RESPONSE
# ==========================================

if user_input:

    if not api_key:

        st.error(
            "Please enter your Groq API key in the sidebar."
        )

    else:

        # Save user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        with st.chat_message("user"):
            st.markdown(user_input)

        try:

            client = Groq(api_key=api_key)

            api_messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ] + st.session_state.messages

            with st.chat_message("assistant"):

                response_placeholder = st.empty()
                full_response = ""

                stream = client.chat.completions.create(
                    model=MODEL,
                    messages=api_messages,
                    temperature=0.6,
                    max_completion_tokens=2048,
                    reasoning_effort="medium",
                    stream=True
                )

                for chunk in stream:

                    content = chunk.choices[0].delta.content

                    if content:
                        full_response += content
                        response_placeholder.markdown(
                            full_response + "▌"
                        )

                response_placeholder.markdown(full_response)

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })

        except Exception as e:

            error_message = (
                "Sorry! Something went wrong while "
                "connecting to the Groq API.\n\n"
                f"Error: {str(e)}"
            )

            st.error(error_message)

            # Remove failed user request so it can be retried
            st.session_state.messages.pop()

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#8795a8;">
        <b>BANUCHI</b> | AI Forex Trading Assistant
        <br>
        Learn Trading. Understand Markets. Manage Risk.
        <br><br>
        ⚠️ Educational purposes only. Not financial advice.
    </div>
    """,
    unsafe_allow_html=True
)
