import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")

company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA")

if st.button("Start Analysis"):
    if company:
        status_text = st.empty()
        report_container = st.empty()
        
        try:
            # Simple setup: one session service, one runner
            session_service = InMemorySessionService()
            runner = Runner(
                app_name="due_diligence_app", 
                agent=root_agent,
                session_service=session_service
            )
            
            user_message = types.Content(role="user", parts=[types.Part(text=company)])

            async def run_analysis():
                full_text = ""
                # We use the simplest runner.run signature
                events = runner.run(
                    user_id="default_user",
                    session_id="default_session",
                    new_message=user_message
                )
                
                for event in events:
                    # Capture which agent is talking
                    if hasattr(event, 'author') and event.author:
                        status_text.info(f"⚙️ **Processing Stage:** {event.author}")
                    
                    # Capture text chunks
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                full_text += part.text
                                # Live update the UI
                                report_container.markdown(full_text)
                return full_text

            # Execute
            final_result = asyncio.run(run_analysis())
            
            if final_result:
                status_text.success("✅ Analysis Complete!")
            else:
                st.error("No text was returned. Check if your API Key is valid and tools are working.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a company name.")
