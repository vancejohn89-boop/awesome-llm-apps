import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent  # Ensure root_agent is imported correctly

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")

company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA")

if st.button("Start Analysis"):
    if company:
        status_text = st.empty()
        report_container = st.empty()
        
        try:
            # 1. Standard ADK Initialization
            session_service = InMemorySessionService()
            runner = Runner(
                app_name="due_diligence_app", 
                agent=root_agent,
                session_service=session_service
            )
            
            user_message = types.Content(role="user", parts=[types.Part(text=company)])

            async def run_and_display():
                full_response = ""
                # runner.run() returns an event stream
                events = runner.run(
                    user_id="user_1",
                    session_id="session_1",
                    new_message=user_message
                )
                
                for event in events:
                    # Update which agent is currently 'thinking'
                    if hasattr(event, 'author') and event.author:
                        status_text.info(f"⚙️ **Processing:** {event.author}...")
                    
                    # Capture and stream the text parts
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                full_response += part.text
                                # Stream the text live to the UI
                                report_container.markdown(full_response + " ▌")
                
                return full_response

            # 2. Run the async function
            final_output = asyncio.run(run_and_display())
            
            if final_output:
                status_text.success("✅ Analysis Complete!")
                report_container.markdown(final_output)
            else:
                st.error("The agents finished but no text was returned. Check your API key and tools.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a company name.")
