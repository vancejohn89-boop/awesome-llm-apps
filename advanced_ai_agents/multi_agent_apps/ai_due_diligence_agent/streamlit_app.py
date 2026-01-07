import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")

company = st.text_input("Enter Company Name:", placeholder="e.g. NVIDIA")

if st.button("Start Analysis"):
    if company:
        status_text = st.empty()
        report_area = st.empty()
        
        try:
            # 1. Initialize Service and Runner
            session_service = InMemorySessionService()
            runner = Runner(
                app_name="due_diligence_app", 
                agent=root_agent,
                session_service=session_service
            )
            
            # Constants for session
            USER_ID = "user_123"
            SESSION_ID = "session_456"

            async def run_pipeline():
                # --- THE FIX: Create the session before running ---
                await session_service.create_session(
                    app_name="due_diligence_app",
                    user_id=USER_ID,
                    session_id=SESSION_ID
                )
                
                user_message = types.Content(
                    role="user", 
                    parts=[types.Part(text=company)]
                )
                
                full_text = ""
                # Stream events from the runner
                event_stream = runner.run(
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=user_message
                )
                
                for event in event_stream:
                    # Show which agent is currently active
                    if hasattr(event, 'author') and event.author:
                        status_text.info(f"⚙️ **Processing:** {event.author}...")
                    
                    # Accumulate and display text
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                full_text += part.text
                                report_area.markdown(full_text + " ▌")
                
                return full_text

            # Execute the async loop
            final_report = asyncio.run(run_pipeline())
            
            if final_report:
                status_text.success("✅ Analysis Complete!")
            else:
                st.error("Pipeline finished but returned no text. Check API grounding settings.")

        except Exception as e:
            st.error(f"Critical Error: {e}")
    else:
        st.warning("Please enter a company name.")
