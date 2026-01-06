import streamlit as st
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

# Standard Streamlit Page Setup
st.set_page_config(page_title="AI Due Diligence", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ AI Due Diligence Agent Team")
st.markdown("""
This multi-agent team performs deep research, market analysis, financial modeling, 
and risk assessment to generate a professional investment memo.
""")

# Sidebar for information
with st.sidebar:
    st.header("Team Workflow")
    st.info("""
    1. **Researcher**: Gathers company data.
    2. **Market Analyst**: Evaluates competition.
    3. **Financial Lead**: Projects growth.
    4. **Risk Officer**: Identifies pitfalls.
    5. **Partner**: Writes final memo.
    """)

# User Input
company = st.text_input("Enter Company Name or URL:", placeholder="e.g. NVIDIA or https://agno.com")

if st.button("Start Analysis"):
    if company:
        try:
            with st.spinner(f"🔍 The agents are collaborating on {company}... This usually takes 45-60 seconds."):
                
                # 1. Initialize the Session Service (Temporary Memory)
                session_service = InMemorySessionService()
                
                # 2. Setup the Runner
                # We provide an app_name and link the root_agent from your agent.py
                runner = Runner(
                    app_name="due_diligence_app", 
                    agent=root_agent,
                    session_service=session_service
                )
                
                # 3. Prepare the message in the format ADK expects
                user_message = types.Content(
                    role="user",
                    parts=[types.Part(text=company)]
                )
                
                # 4. Run the Agent Pipeline
                # We use the 'new_message' argument which is the standard for ADK Runners
                event_stream = runner.run(
                    user_id="streamlit_user",
                    session_id="current_analysis",
                    new_message=user_message
                )
                
                # 5. Process the output from the stream
                final_text = ""
                for event in event_stream:
                    # ADK yields events. We look for 'is_final_response' or text parts.
                    if hasattr(event, 'content') and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                final_text += part.text
                    
                    # If the runner explicitly flags the final response, we can stop
                    if hasattr(event, 'is_final_response') and event.is_final_response():
                        break

                # 6. Display the result
                if final_text:
                    st.success("Analysis Complete!")
                    st.subheader("Investment Memo")
                    st.markdown(final_text)
                else:
                    st.warning("The agents completed the task but didn't return text. Check your logs for tool outputs.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Technical Tip: Ensure your Google API Key has access to both Gemini 1.5 Flash and Pro.")
    else:
        st.warning("Please enter a company name or URL.")
