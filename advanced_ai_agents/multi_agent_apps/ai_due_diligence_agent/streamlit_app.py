import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ AI Due Diligence Agent: X-Ray Mode")

company = st.text_input("Enter Company Name:", placeholder="e.g. NVIDIA")

if st.button("Start Analysis"):
    if company:
        # We use a code block to show raw agent "chatter" for debugging
        debug_area = st.expander("🛠️ Agent Logs (X-Ray Mode)", expanded=True)
        report_area = st.empty()
        
        try:
            session_service = InMemorySessionService()
            runner = Runner(
                app_name="due_diligence_app", 
                agent=root_agent,
                session_service=session_service
            )
            
            user_message = types.Content(role="user", parts=[types.Part(text=company)])

            async def run_with_logs():
                full_text = ""
                event_stream = runner.run(
                    user_id="debug_user",
                    session_id="debug_session",
                    new_message=user_message
                )
                
                for event in event_stream:
                    # 1. Print RAW event info to the Debug Area
                    with debug_area:
                        if hasattr(event, 'author'):
                            st.write(f"👉 **{event.author}** is active...")
                        
                        # Check for Tool Calls (The likely culprit)
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, 'function_call'):
                                    st.warning(f"🔧 Tool Call: {part.function_call.name}")
                                    st.code(part.function_call.args)
                                
                                if hasattr(part, 'text') and part.text:
                                    full_text += part.text
                                    report_area.markdown(full_text)
                
                return full_text

            # Execute
            result = asyncio.run(run_with_logs())
            
            if not result:
                st.error("🏁 The pipeline finished but returned ZERO text. This almost always means the first tool (google_search) failed.")
                st.info("Check: Is your GOOGLE_API_KEY valid and does it have the 'Google Search Service' enabled in the Google Cloud Console?")

        except Exception as e:
            st.error(f"Critical Error: {e}")
    else:
        st.warning("Please enter a company name.")
