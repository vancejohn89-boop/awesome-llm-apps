import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search
# Import your other custom tools from your tools.py file
# from tools import generate_financial_chart, generate_html_report

# 1. Researcher: Gathers data using the built-in Google Search
researcher_agent = LlmAgent(
    name="CompanyResearcher",
    model="gemini-1.5-flash",
    description="Researches company background, recent news, and key data points.",
    instruction="""
    Use Google Search to find the latest information about the target company. 
    Focus on:
    - Recent news and press releases
    - Core business model and products
    - Key executives and headquarters
    """,
    tools=[google_search],
    output_key="research_data"
)

# 2. Market Analyst: Evaluates the landscape based on research
analyst_agent = LlmAgent(
    name="MarketAnalyst",
    model="gemini-1.5-flash",
    description="Analyzes market position and competition.",
    instruction="""
    Using the {research_data}, identify the top 3 competitors and 
    analyze the company's competitive advantages (moats).
    """,
    output_key="market_analysis"
)

# 3. Financial Lead: Projects growth and numbers
financial_agent = LlmAgent(
    name="FinancialLead",
    model="gemini-1.5-flash",
    description="Evaluates financial health and growth prospects.",
    instruction="""
    Based on the {research_data}, summarize the company's revenue 
    streams and identify potential financial risks or growth drivers.
    """,
    output_key="financial_summary"
)

# 4. Investor Memo Agent: Synthesizes everything into the final report
memo_agent = LlmAgent(
    name="MemoWriter",
    model="gemini-1.5-flash",
    description="Writes the final professional investment memo.",
    instruction="""
    Synthesize the following into a professional investment memo:
    - Research: {research_data}
    - Market Analysis: {market_analysis}
    - Financials: {financial_summary}
    
    Format the output with clear headers: # Summary, ## Market, ## Financials, and ### Recommendation.
    """,
    output_key="investor_memo"
)

# 5. The Pipeline: Coordinates the sequence of work
due_diligence_pipeline = SequentialAgent(
    name="DueDiligencePipeline",
    description="A step-by-step pipeline for deep company analysis.",
    sub_agents=[
        researcher_agent, 
        analyst_agent, 
        financial_agent, 
        memo_agent
    ]
)

# 6. The Root Agent: The "Manager" that interacts with Streamlit
root_agent = LlmAgent(
    name="DueDiligenceManager",
    model="gemini-1.5-flash",
    description="Main entry point for the Due Diligence team.",
    instruction="""
    You are the manager of a due diligence team. 
    1. Pass the user's company request to the 'DueDiligencePipeline'.
    2. Once the pipeline is complete, retrieve the final 'investor_memo'.
    3. IMPORTANT: You must repeat the full text of the 'investor_memo' 
       starting with 'FINAL REPORT:' in your response.
    """,
    sub_agents=[due_diligence_pipeline]
)
