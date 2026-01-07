import streamlit as st
import asyncio
import time
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

# UI Setup
st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")
st.markdown("---")

# User Input
company = st.text_input("Enter Company Name or URL for Analysis:", placeholder="e.g. NVIDIA or https://agno.com")

if st.button("Start Analysis"):
    if company:
        # Containers for real-time updates
        status_text = st.empty()
        report_container = st.empty()
        
        try:
            # 1. Initialize Services
            session_service = InMemorySessionService()
            APP_NAME = "due_diligence_app"
            USER_ID = "user_primary"
            SESSION_ID = "session_active"

            runner = Runner(
                app_name=APP_NAME, 
                agent=root_agent,
                session_service=session_service
            )
            
            # 2. Setup Message
            user_message = types.Content(role="user", parts=[types.Part(text=company)])

            async def run_pipeline():
                full_text = ""
                # Run the agent stream
                events = runner.run(
                    user_id=USER_ID,
                    session_id=SESSION_ID,
                    new_message=user_message
                )
                
                for event in events:
                    # Update status based on acting agent
                    if hasattr(event, 'author') and event.author:
                        status_text.info(f"⚙️ **Active Agent:** {event.author} is processing...")
                    
                    # Capture streaming text
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                full_text += part.text
                                report_container.markdown(full_text + " ▌")
                
                # 3. State Recovery Logic (The "Backup Plan")
                # If the stream is empty or the agent didn't "speak" the final memo
                if not full_text:
                    status_text.warning("🏁 Pipeline finished. Reaching into agent memory for report...")
                    await asyncio.sleep(2) # Brief pause for state commitment
                    
                    session = await session_service.get_session(
                        app_name=APP_NAME, 
                        user_id=USER_ID, 
                        session_id=SESSION_ID
                    )
                    
                    if session and session.state:
                        # List of possible keys defined in your agent.py pipeline
                        keys_to_try = ["investor_memo", "html_report_result", "market_analysis", "company_info"]
                        
                        for key in keys_to_try:
                            if key in session.state and session.state[key]:
                                return session.state[key]
                        
                        # Last resort: grab the most recent non-empty value in the state
                        all_vals = [v for v in session.state.values() if isinstance(v, str) and len(v) > 100]
                        if all_vals:
                            return all_vals[-1]
                    
                    # If we get here, it means the state was truly empty
                    return None
                
                return full_text

            # Execute the async function
            final_report = asyncio.run(run_pipeline())
            
            # Final Result Display
            if final_report:
                status_text.success("✅ Analysis Complete!")
                report_container.markdown("### Final Investment Memo")
                report_container.markdown(final_report)
                
                # Add a download button for the result
                st.download_button(
                    label="Download Report as Text",
                    data=final_report,
                    file_name=f"{company.replace(' ', '_')}_due_diligence.txt",
                    mime="text/plain"
                )
            else:
                status_text.error("Agents completed, but the report content was not found in memory.")
                # Self-Correction: Let's see what keys actually exist
                st.info("Debugging: Inspecting Agent Memory...")
                session = asyncio.run(session_service.get_session(APP_NAME, USER_ID, SESSION_ID))
                if session and session.state:
                    st.write("Available memory keys:", list(session.state.keys()))
                else:
                    st.write("Memory is empty. This usually indicates an API Authentication or Tool error.")

        except Exception as e:
            st.error(f"Execution Error: {e}")
            st.info("Check your Streamlit Logs for specific traceback details.")
    else:
        st.warning("Please enter a company name or URL.")
