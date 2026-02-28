from crewai import Task
from agents import financial_analyst, risk_analyst, investment_advisor


# =====================================
# Task 1: Financial Analysis
# =====================================

financial_analysis_task = Task(
    description="""
Document Context:
{document_context}

User Query:
{query}

Provide a structured financial analysis including:

1. Revenue performance
2. Profitability
3. Liquidity position
4. Operational highlights

Rules:
- Use ONLY Document Context.
- Do NOT fabricate numbers.
- If required information is missing, state clearly.
""",
    expected_output="""
Structured report with headings:
- Financial Performance
- Profitability
- Liquidity Position
- Operational Summary
""",
    agent=financial_analyst,
)


# =====================================
# Task 2: Risk Assessment
# =====================================

risk_assessment_task = Task(
    description="""
Using the financial analysis from the previous step:

Identify:
- Liquidity risks
- Profitability risks
- Operational risks
- Revenue sustainability risks

Base everything strictly on the financial analysis.
Do not introduce new facts.
""",
    expected_output="""
Structured risk report with sections:
- Liquidity Risk
- Profitability Risk
- Operational Risk
- Revenue Sustainability Risk
""",
    agent=risk_analyst,
)


# =====================================
# Task 3: Investment Recommendation
# =====================================

investment_task = Task(
    description="""
Document Context:
{document_context}

External Market Context:
{external_context}

Using:

1. Financial Analysis
2. Risk Assessment
3. External Market Context (if provided)

Provide:

A. Investment Recommendation (Buy / Hold / Sell)
B. Supporting Financial Rationale
C. Risk-Adjusted Perspective

If External Market Context is not empty:
- Summarize it under:
  "External Market Insights"

If it is empty:
- State: "No external market data available."

Keep document-derived insights separate from external insights.
Do not fabricate statistics.
""",
    expected_output="""
Structured investment report including:

- Investment Recommendation
- Financial Justification
- Risk Summary
- External Market Insights
""",
    agent=investment_advisor,
)





