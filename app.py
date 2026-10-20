from agents import run_evaluation
import streamlit as st

def check_password():
    """Returns `True` if the user enters the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password in state
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show password input
        st.subheader("🔒 Restricted Access")
        st.text_input("Please enter the password to access the Pitch Simulator:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Incorrect password, show input and error message
        st.subheader("🔒 Restricted Access")
        st.text_input("Please enter the password to access the Pitch Simulator:", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect. Please try again.")
        return False
    else:
        # Correct password
        return True

# --- BLOCK APP UNLESS PASSWORD IS CORRECT ---
if check_password():
    
    # PUT ALL YOUR EXISTING APP CODE HERE 👇
    st.title("Pitch Simulator & AI Evaluator")
    # (Your existing Streamlit code, inputs, and Bedrock calls go under here...)

    st.set_page_config(page_title="Multi-Agent Startup Validator", layout="centered")

    st.title("🚀 AI Startup Idea Validator")
    st.write("Powered by AWS Bedrock, Llama 3.3, and Strands Multi-Agent Orchestration.")

    user_idea = st.text_area(
    "Describe your business idea:",
    placeholder="e.g., An AI-powered automated bookkeeping platform for freelance truck drivers in Texas.")

    if st.button("Evaluate Idea", type="primary"):
       if not user_idea.strip():
          st.warning("Please enter a business idea first!")
       else:
        with st.spinner("🤖 Multi-agent team at work (Market Analysis ➔ Financials ➔ VC Risk)..."):
            evaluation_result = run_evaluation(user_idea)
            
            st.success("Evaluation Complete!")
            st.markdown("### 📊 Investor Memo & Analysis")
            st.code(evaluation_result, language="json")
