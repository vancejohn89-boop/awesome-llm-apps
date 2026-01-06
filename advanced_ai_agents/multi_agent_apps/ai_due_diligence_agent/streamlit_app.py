import streamlit as st
from agent import due_diligence_team

st.title("🕵️‍♂️ AI Due Diligence Agent")
st.write("Enter a company name to start the research.")

company = st.text_input("Company Name:", placeholder="e.g. Nvidia")

if st.button("Run Research"):
    if company:
        with st.spinner("Team is working..."):
            # This calls the 'brain' from your agent.py
            result = due_diligence_team.run(company)
            st.markdown(result)
    else:
        st.warning("Please enter a company name.")
