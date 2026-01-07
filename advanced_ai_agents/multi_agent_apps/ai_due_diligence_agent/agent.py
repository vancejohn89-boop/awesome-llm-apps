import os
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search

# 1. Researcher: Uses built-in Google Search grounding
# No separate API keys or CX IDs needed; it uses your main Gemini key.
researcher_agent = LlmAgent(
    name="CompanyResearcher",
    model="gemini-1.5-flash",
    description="Researches company background and recent news using Google Search.",
    instruction="""
    Use Google Search to find current information about the target company. 
    Look for:
    - Core business operations and recent news.
    - Key financial indicators or recent quarterly performance mentions.
    - Major competitors and market position.
    """,
    tools=[google_search],
    output_key="research_data"  # This saves the output into session memory
)

# 2. Market Analyst: Consumes data from the Researcher
analyst_agent = LlmAgent(
    name="MarketAnalyst",
    model="gemini-1.5-flash",
    description="Analyzes the market landscape and competition.",
    instruction="""
    Analyze the company's competitive moats based on this research: {research_data}.
    Identify at least three strengths and two market threats.
    """,
    output_key="market_analysis"
)

# 3. Financial Lead: Projects growth
financial_agent = LlmAgent(
    name="FinancialLead",
    model="gemini-1.5-flash",
    description="Evaluates growth prospects and risks.",
    instruction="""
    Review the findings: {research_data}. 
    Summarize the potential for future revenue growth and identify 
    any red flags found in recent news or financials.
    """,
    output_key="financial_summary"
)

# 4. Investor Memo Agent: Synthesizes final report
memo_writer = LlmAgent(
    name="MemoWriter",
    model="gemini-1.5-flash",
    description="Synthesizes all findings into a professional memo.",
    instruction="""
    You are a Senior Investment Associate. Combine these inputs:
    - Research: {research_data}
    - Analysis: {market_analysis}
    - Financials: {financial_summary}
    
    Produce a final professional Investment Memo. Use Markdown headers 
    (# Summary, ## Analysis, etc.) and a clear Recommendation.
    """,
    output_key="investor_memo"
)

# 5. The Sequential Pipeline (The Assembly Line)
# This ensures agents run in order: 1 -> 2 -> 3 -> 4
due_diligence_pipeline = SequentialAgent(
    name="DueDiligencePipeline",
    description="Executes a step-by-step company analysis workflow.",
    sub_agents=[
        researcher_agent, 
        analyst_agent, 
        financial_agent, 
        memo_writer
    ]
)

# 6. The Manager (Root Agent): The one Streamlit talks to
root_agent = LlmAgent(
    name="DueDiligenceManager",
    model="gemini-1.5-flash",
    description="Entry point for the due diligence team.",
    instruction="""
    1. Delegate the user's request to the 'DueDiligencePipeline'.
    2. Once the pipeline finishes, retrieve the content from 'investor_memo'.
    3. IMPORTANT: Your response MUST be the full text of that memo. 
       Start your response with 'FINAL REPORT:' so the UI knows it is complete.
    """,
    sub_agents=[due_diligence_pipeline]
)
