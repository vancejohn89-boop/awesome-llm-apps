import streamlit as st
from google.adk.runners import Runner
from agent import root_agent

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")
st.write("Powered by Google ADK & Gemini")

with st.sidebar:
    st.info("Agent team: Research -> Market -> Financials -> Risks -> Memo")

company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA or https://agno.com")

if st.button("Start Analysis"):
    if company:
        try:
            with st.spinner(f"🔍 Analyzing {company}... This involves multiple agents and may take a minute."):
                # Initialize the ADK Runner
                runner = Runner()
                
                # We call the 'root_agent' which handles the handoff to the pipeline
                result = runner.run(root_agent, input_text=company)
                
                st.subheader("Analysis Results")
                st.markdown(result.text)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a company name or URL.")
