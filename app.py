import streamlit as st
from agents import run_evaluation

st.set_page_config(page_title="Multi-Agent Startup Validator", layout="centered")

st.title("🚀 AI Startup Idea Validator")
st.write("Powered by AWS Bedrock, Llama 3.3, and Strands Multi-Agent Orchestration.")

user_idea = st.text_area(
    "Describe your business idea:",
    placeholder="e.g., An AI-powered automated bookkeeping platform for freelance truck drivers in Texas."
)

if st.button("Evaluate Idea", type="primary"):
    if not user_idea.strip():
        st.warning("Please enter a business idea first!")
    else:
        with st.spinner("🤖 Multi-agent team at work (Market Analysis ➔ Financials ➔ VC Risk)..."):
            evaluation_result = run_evaluation(user_idea)
            
            st.success("Evaluation Complete!")
            st.markdown("### 📊 Investor Memo & Analysis")
            st.code(evaluation_result, language="json")
EOF