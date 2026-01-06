import streamlit as st
from google.adk.runners import SimpleRunner # Changed this
from agent import root_agent

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")
st.write("Powered by Google ADK & Gemini")

company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA or https://agno.com")

if st.button("Start Analysis"):
    if company:
        try:
            with st.spinner(f"🔍 The agents are collaborating on {company}..."):
                
                # SimpleRunner handles the session and memory automatically
                runner = SimpleRunner()
                
                # Execute the analysis using root_agent
                result = runner.run(root_agent, input_text=company)
                
                st.subheader("Analysis Results")
                st.markdown(result.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Check your Logs in the bottom right for more details.")
    else:
        st.warning("Please enter a company name or URL.")
