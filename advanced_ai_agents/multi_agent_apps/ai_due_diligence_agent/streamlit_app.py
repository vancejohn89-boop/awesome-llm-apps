import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

# UI Setup
st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️", layout="wide")
st.title("🕵️‍♂️ AI Due Diligence Agent Team")

company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA or https://agno.com")

if st.button("Start Analysis"):
    if company:
        try:
            with st.spinner("🚀 Agents are starting the research pipeline..."):
                
                # 1. Setup Session & Runner
                session_service = InMemorySessionService()
                runner = Runner(
                    app_name="due_diligence_app", 
                    agent=root_agent,
                    session_service=session_service
                )
                
                # 2. Prepare Message
                user_message = types.Content(
                    role="user",
                    parts=[types.Part(text=company)]
                )
                
                # 3. Execution Container
                async def run_analysis():
                    user_id = "user_123"
                    session_id = "session_456"
                    
                    event_stream = runner.run(
                        user_id=user_id,
                        session_id=session_id,
                        new_message=user_message
                    )
                    
                    accumulated_text = ""
                    status_bar = st.empty()
                    
                    for event in event_stream:
                        # Update status based on which agent is talking
                        if hasattr(event, 'author') and event.author:
                            status_bar.info(f"Currently Active: **{event.author}**")
                        
                        # Capture text from content parts
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, 'text') and part.text:
                                    accumulated_text += part.text
                        
                        # Check for a "Final Response" flag
                        if hasattr(event, 'is_final_response') and event.is_final_response():
                            if event.content and event.content.parts:
                                return event.content.parts[0].text

                    # 4. BACKUP PLAN: If stream text is empty, pull directly from state
                    if not accumulated_text:
                        session = await session_service.get_session(
                            app_name="due_diligence_app", 
                            user_id=user_id, 
                            session_id=session_id
                        )
                        # We look for the 'investor_memo' key defined in Stage 5 of your agent.py
                        return session.state.get("investor_memo", "Analysis complete, but no memo was found in state.")
                    
                    return accumulated_text

                # Run the async loop
                final_report = asyncio.run(run_analysis())
                
                # Display Result
                st.success("✅ Analysis Complete!")
                st.markdown("---")
                st.markdown(final_report)
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a company name.")
