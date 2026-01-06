import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agent import root_agent

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")
st.write("Powered by Google ADK & Gemini")

company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA or https://agno.com")

if st.button("Start Analysis"):
    if company:
        try:
            with st.spinner(f"🔍 The agents are collaborating on {company}..."):
                
                # 1. Initialize memory (Session Service)
                session_service = InMemorySessionService()
                
                # 2. Setup the Runner with the required 'app_name'
                # We name it 'ai_due_diligence' so the runner has an identity
                runner = Runner(
                    app_name="ai_due_diligence", 
                    agent=root_agent,
                    session_service=session_service
                )
                
                # 3. Create an async function to run the agent
                async def run_analysis():
                    user_id = "streamlit_user"
                    session_id = "current_analysis"
                    
                    # In newer ADK versions, we pass the query as 'input_text'
                    event_stream = runner.run(
                        user_id=user_id,
                        session_id=session_id,
                        input_text=company
                    )
                    
                    final_text = ""
                    for event in event_stream:
                        # Stream the result if it contains text
                        if hasattr(event, 'content') and event.content.parts:
                            final_text += event.content.parts[0].text
                    
                    return final_text if final_text else "No response generated."

                # Execute
                final_report = asyncio.run(run_analysis())
                
                st.subheader("Analysis Results")
                st.markdown(final_report)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Ensure your GOOGLE_API_KEY is in Streamlit Secrets.")
    else:
        st.warning("Please enter a company name or URL.")
