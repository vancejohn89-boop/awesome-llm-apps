import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search

# 1. Researcher: Using the brand new Gemini 3 Flash
researcher_agent = LlmAgent(
    name="CompanyResearcher",
    model="gemini-3-flash", # <--- UPDATED MODEL ID
    description="Researches company background and news using Google Search.",
    instruction="""
    Use Google Search to find current information about the target company. 
    Focus on business operations, recent quarterly news, and market position.
    """,
    tools=[google_search],
    output_key="research_data"
)

# 2. Market Analyst: Using Gemini 3 Flash
analyst_agent = LlmAgent(
    name="MarketAnalyst",
    model="gemini-3-flash",
    description="Analyzes competition and market moats.",
    instruction="""
    Analyze the company's competitive moats based on this research: {research_data}.
    Identify strengths and market threats.
    """,
    output_key="market_analysis"
)

# ... [Financial and Memo agents follow the same pattern] ...

# 5. The Sequential Pipeline
due_diligence_pipeline = SequentialAgent(
    name="DueDiligencePipeline",
    sub_agents=[researcher_agent, analyst_agent, financial_agent, memo_writer]
)

# 6. The Manager (Root Agent)
root_agent = LlmAgent(
    name="DueDiligenceManager",
    model="gemini-3-flash",
    instruction="""
    Delegate the user's request to the 'DueDiligencePipeline'.
    Repeat the full 'investor_memo' starting with 'FINAL REPORT:'.
    """,
    sub_agents=[due_diligence_pipeline]
)
