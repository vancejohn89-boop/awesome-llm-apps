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
        # Create a container for the streaming text
        report_container = st.empty()
        status_text = st.empty()
        
        try:
            with st.spinner("🚀 Initializing Pipeline..."):
                session_service = InMemorySessionService()
                runner = Runner(
                    app_name="due_diligence_app", 
                    agent=root_agent,
                    session_service=session_service
                )
                
                user_message = types.Content(
                    role="user",
                    parts=[types.Part(text=company)]
                )

                async def run_and_stream():
                    full_response = ""
                    # The stream yields events as they happen
                    event_stream = runner.run(
                        user_id="user_1",
                        session_id="session_1",
                        new_message=user_message
                    )
                    
                    for event in event_stream:
                        # 1. Update status based on the current agent
                        if hasattr(event, 'author') and event.author:
                            status_text.write(f"⚙️ **Agent Acting:** {event.author}")
                        
                        # 2. Append and display text parts immediately
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    full_response += part.text
                                    # This "streams" the text to the UI live
                                    report_container.markdown(full_response + " ▌")
                    
                    return full_response

                # Execute the stream
                final_output = asyncio.run(run_and_stream())
                
                # Final cleanup
                status_text.empty()
                report_container.markdown(final_output)
                if not final_output:
                    st.error("Agents completed but no text was captured. Check API Key quotas.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a company name.")
