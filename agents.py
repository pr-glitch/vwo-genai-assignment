from crewai import Agent, LLM
from tools import search_tool

# =====================================
# LLM Configuration (Ollama Llama3)
# =====================================

llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434",
    temperature=0
)

# =====================================
# Financial Analyst
# =====================================

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Extract and summarize financial performance strictly from provided document context.",
    backstory=(
        "You are an institutional-grade financial analyst. "
        "You rely strictly on document-derived data and never fabricate numbers."
    ),
    verbose=False,
    memory=False,
    allow_delegation=False,
    max_iter=2,
    llm=llm
)

# =====================================
# Risk Analyst
# =====================================

risk_analyst = Agent(
    role="Financial Risk Specialist",
    goal="Identify financial and operational risks based strictly on financial findings.",
    backstory=(
        "You specialize in liquidity risk, profitability pressure, "
        "operational exposure, and revenue sustainability."
    ),
    verbose=False,
    memory=False,
    allow_delegation=False,
    max_iter=2,
    llm=llm
)

# =====================================
# Investment Advisor (Search Enabled)
# =====================================

investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="Provide disciplined investment recommendations using financial analysis and external market context if provided.",
    backstory=(
        "You provide balanced Buy/Hold/Sell recommendations. "
        "If the context contains External Market Data, you must incorporate it "
        "under the section 'External Market Insights'."
    ),
    verbose=False,
    memory=False,
    allow_delegation=False,
    max_iter=2,
    llm=llm
)





