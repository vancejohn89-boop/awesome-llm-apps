import streamlit as st
import asyncio
import time
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
            # 1. Initialize Services
            session_service = InMemorySessionService()
            runner = Runner(
                app_name="due_diligence_app", 
                agent=root_agent,
                session_service=session_service
            )
            
            # 2. Setup IDs and Message
            USER_ID = "user_primary"
            SESSION_ID = "session_active"
            user_message = types.Content(role="user", parts=[types.Part(text=company)])

            async def run_pipeline():
                full_text = ""
                # We use run_async to handle the event stream properly
                events = runner.run(
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=user_message
                )
                
                for event in events:
                    # Update the UI with the current acting agent
                    if hasattr(event, 'author') and event.author:
                        status_text.info(f"⚙️ **Processing Stage:** {event.author}")
                    
                    # Capture streaming text
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                full_text += part.text
                                report_container.markdown(full_text + " ▌")
                
                # 3. CRITICAL BACKUP: If stream is empty, wait and pull from State
                if not full_text:
                    status_text.warning("🏁 Pipeline finished. Finalizing report...")
                    # Give the state a moment to commit (common in multi-agent handoffs)
                    await asyncio.sleep(2) 
                    
                    # Retrieve the session manually from the service
                    session = await session_service.get_session(
                        app_name="due_diligence_app", 
                        user_id=USER_ID, 
                        session_id=SESSION_ID
                    )
                    
                    if session and session.state:
                        # Pull the key specifically defined in Stage 5 of agent.py
                        full_text = session.state.get("investor_memo", "")
                
                return full_response if full_text else None

            # Execute the async function in a sync Streamlit context
            result = asyncio.run(run_pipeline())
            
            if result:
                status_text.success("✅ Analysis Complete!")
                report_container.markdown(result)
            else:
                st.error("Agents completed but the report was not found. Please check your 'agent.py' output_key names.")

        except Exception as e:
            st.error(f"Execution Error: {e}")
    else:
        st.warning("Please enter a target company.")
