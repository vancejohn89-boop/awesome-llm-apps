import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import LocalSessionService # Added this
from agent import root_agent

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")
st.write("Powered by Google ADK & Gemini")

company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA or https://agno.com")

if st.button("Start Analysis"):
    if company:
        try:
            with st.spinner(f"🔍 The agents are collaborating on {company}..."):
                
                # 1. Create a local session service to hold the agent's memory
                session_service = LocalSessionService()
                
                # 2. Pass that service into the Runner
                runner = Runner(session_service=session_service)
                
                # 3. Execute the analysis
                result = runner.run(root_agent, input_text=company)
                
                st.subheader("Analysis Results")
                st.markdown(result.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a company name or URL.")
