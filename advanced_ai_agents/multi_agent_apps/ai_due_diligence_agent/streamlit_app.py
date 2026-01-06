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
                
                # 1. Initialize the session service (this is the agent's memory)
                session_service = InMemorySessionService()
                
                # 2. Setup the Runner with the agent and memory
                runner = Runner(
                    agent=root_agent,
                    session_service=session_service
                )
                
                # 3. Create a session for this specific run
                # We use 'await' because ADK is built on asyncio
                async def run_analysis():
                    # Generate unique IDs for this user session
                    user_id = "streamlit_user"
                    session_id = "current_analysis"
                    
                    # Run the agent (this yields events as they happen)
                    result_text = ""
                    events = runner.run(
                        user_id=user_id,
                        session_id=session_id,
                        input_text=company
                    )
                    
                    for event in events:
                        # Check if this is the final answer from the agents
                        if event.is_final_response():
                            return event.content.parts[0].text
                    return "No final report generated."

                # Execute the async function
                final_report = asyncio.run(run_analysis())
                
                st.subheader("Analysis Results")
                st.markdown(final_report)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Ensure your GOOGLE_API_KEY is correct in the Streamlit Secrets.")
    else:
        st.warning("Please enter a company name or URL.")
