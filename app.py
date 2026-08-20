import os
import json
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Streamlit page dashboard
st.set_page_config(page_title="AutoRecover AI", page_icon="🛒", layout="wide")

st.title("🛒 AutoRecover AI — Agentic Commerce Dashboard")
st.markdown("Autonomous AI Agent for Real-Time Cart Recovery & Transaction Dispute Handling")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    model_name = st.selectbox("Model", ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"])
    st.markdown("---")
    st.markdown("**Note:** Get your free API key from [Google AI Studio](https://aistudio.google.com/).")

# Simulated Checkout Event Data
st.subheader("📡 Simulate Webhook / Checkout Event")
col1, col2 = st.columns(2)

with col1:
    customer_name = st.text_input("Customer Name", "Rohan Sharma")
    cart_value = st.number_input("Cart Total (INR)", value=3499, step=100)
    items = st.text_input("Cart Items", "Wireless Mechanical Keyboard")

with col2:
    failure_reason = st.selectbox(
        "Failure / Drop-off Reason",
        [
            "Payment Gateway Timeout / 504 Error",
            "Card Declined: Insufficient Limit",
            "Abandoned at Delivery Address Stage",
            "UPI Intent App Not Responding"
        ]
    )
    customer_tier = st.selectbox("Customer Tier", ["New User", "Returning Customer", "VIP"])

# Trigger Button
if st.button("🚀 Trigger AI Agent Execution", type="primary"):
    if not api_key:
        st.error("Please enter a valid Gemini API Key in the sidebar.")
    else:
        with st.spinner("Agent analyzing event and generating recovery plan..."):
            try:
                # Initialize the unified Google GenAI SDK client
                client = genai.Client(api_key=api_key)
                
                # System instructions to configure the agent's behavior
                system_instruction = """You are an autonomous Agentic Commerce Recovery AI working for an e-commerce fintech merchant.
                Your job is to parse transaction failure events and output a strategic recovery plan in strict JSON format.
                Always include a dynamic discount (max 10%), a personalized recovery message, and a recommended channel (SMS/WhatsApp/Email).
                Output JSON only."""

                # The event payload passed to the AI
                prompt = f"""
                Event Details:
                - Customer: {customer_name}
                - Cart Value: ₹{cart_value}
                - Cart Items: {items}
                - Drop-off/Failure Reason: {failure_reason}
                - Customer Tier: {customer_tier}
                
                Provide the recovery payload in JSON format with keys: urgency_level, recommended_channel, dynamic_discount_applied, personalized_message, next_autonomous_action.
                """
                
                # Execute the model with strict JSON formatting and low temperature for accuracy
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.2, 
                        response_mime_type="application/json", 
                    )
                )
                
                # Parse and display the response
                result = json.loads(response.text)
                
                st.success("Recovery Action Generated Successfully!")
                st.markdown("### 🤖 Autonomous Agent Plan")
                
                # Display metrics visually
                m1, m2, m3 = st.columns(3)
                m1.metric("Urgency Level", result.get("urgency_level", "Medium"))
                m2.metric("Discount Applied", result.get("dynamic_discount_applied", "0%"))
                m3.metric("Channel", result.get("recommended_channel", "Email"))
                
                # Display the message and action
                st.info(f"**Personalized Message to Customer:**\n\n{result.get('personalized_message', '')}")
                st.warning(f"**Next Autonomous Action (System Execution):** {result.get('next_autonomous_action', '')}")
                
                st.markdown("### 📄 Raw Backend JSON Payload")
                st.json(result)
                
            except Exception as e:
                st.error(f"Error executing agent: {e}")
