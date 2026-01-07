from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.tools import google_search

# 1. Define INDIVIDUAL agents first
researcher_agent = LlmAgent(
    name="Researcher",
    model="gemini-3-flash",
    instruction="Research the company...",
    tools=[google_search]
)

analyst_agent = LlmAgent(
    name="Analyst",
    model="gemini-3-flash",
    instruction="Analyze the research data..."
)

financial_agent = LlmAgent( # <--- Define this BEFORE line 35
    name="FinancialAnalyst",
    model="gemini-3-flash",
    instruction="Evaluate financial health..."
)

memo_writer = LlmAgent( # <--- Define this BEFORE line 35
    name="MemoWriter",
    model="gemini-3-flash",
    instruction="Synthesize everything into an investor memo."
)

# 2. NOW define the pipeline using the variables created above
due_diligence_pipeline = SequentialAgent(
    name="DueDiligencePipeline",
    sub_agents=[researcher_agent, analyst_agent, financial_agent, memo_writer]
)

# 3. Define the root agent last
root_agent = LlmAgent(
    name="DueDiligenceManager",
    model="gemini-3-flash",
    instruction="Coordinate the due diligence process.",
    sub_agents=[due_diligence_pipeline]
)
root_agent = LlmAgent(
    name="DueDiligenceManager",
    model="gemini-3-flash",
    instruction="""
    1. Run the 'DueDiligencePipeline'.
    2. After it finishes, look at the state for 'investor_memo'.
    3. You MUST output the full text of that memo. Do not summarize it. 
    4. If 'investor_memo' is empty, explain why the search failed.
    """,
    sub_agents=[due_diligence_pipeline]
)
