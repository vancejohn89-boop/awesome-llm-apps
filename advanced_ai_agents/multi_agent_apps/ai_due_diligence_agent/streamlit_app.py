import streamlit as st
from google.adk.runners import Runner
from agent import due_diligence_team

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")
st.write("Powered by Google ADK & Gemini")

# Sidebar for API Key if not in secrets
with st.sidebar:
    st.info("Agent team: Researcher -> Financial Analyst -> Reporter")

company = st.text_input("Enter Company Name for Research:", placeholder="e.g. NVIDIA")

if st.button("Start Analysis"):
    if company:
        try:
            with st.spinner(f"🔍 Analyzing {company}... This may take a minute."):
                # ADK requires a Runner to handle the agent execution
                runner = Runner()
                # We use .run() to get the final output from the team
                result = runner.run(due_diligence_team, input_text=company)
                
                st.subheader("Analysis Results")
                st.markdown(result.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a company name first.")
