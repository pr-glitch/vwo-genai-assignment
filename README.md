📊 Financial Document Analyzer
AI Internship Assignment – Debug Challenge Submission
👤 Candidate Information

Submission for AI Internship Debug Challenge

🧠 Project Overview

This project is a Financial Document Analyzer built using:

CrewAI (Multi-Agent Orchestration)

FastAPI

Ollama (llama3 LLM)

Embedding-based Retrieval (RAG)

Controlled External Search Integration

The original repository contained:

Deterministic runtime bugs 🐛

Hallucination-prone prompts

Circular imports

Async blocking issues

Broken tool orchestration

Unstable agent behavior

All issues have been fixed and the system has been redesigned into a clean, scalable architecture.

✅ Assignment Requirements Coverage
✔ Upload financial documents (PDF)

Implemented via FastAPI /analyze endpoint.

✔ AI-powered financial analysis

Financial Analyst agent performs structured document-grounded analysis.

✔ Risk assessment

Risk Analyst agent identifies liquidity, profitability, and operational risks.

✔ Investment recommendations

Investment Advisor agent produces Buy/Hold/Sell recommendations with reasoning.

✔ Market insights

Controlled search tool integration for optional external industry context.

🐛 Deterministic Bugs Fixed
Bug Category	Technical Error	Fix Applied
Circular Import	ImportError / Silent Hang	Removed cyclic imports between agents.py and tools.py.
Invalid Library	NameError: Pdf is not defined	Replaced invalid PDF usage with PyPDFLoader.
Attribute Call	AttributeError: Tool has no attribute	Fixed incorrect tool referencing in task.py.
Missing Instance	TypeError: missing self	Properly instantiated tool classes before usage.
Async Blocking	API hanging during processing	Wrapped crew.kickoff() inside run_in_executor to prevent event loop blocking.
Module Naming	ModuleNotFoundError	Corrected task.py vs tasks.py mismatch.
Uvicorn Reload	reload=True not working	Updated to uvicorn.run("main:app").

All deterministic errors are resolved.

🚀 Architectural Improvements
1️⃣ Prompt Optimization

The original prompts encouraged:

Fabricated financial advice

Fake URLs

Hallucinated market data

Dramatic speculation

Rewritten prompts now:

Enforce strict document grounding

Prevent hallucination

Define exact fallback behavior

Provide structured outputs

Maintain professional financial tone

2️⃣ Embedding-Based RAG

Instead of passing the entire document to the LLM, the system now uses:

PDF extraction

Text chunking

Embedding generation (nomic-embed-text)

Cosine similarity retrieval

Top-K relevant context injection

This ensures:

Scalable document handling

Reduced context overload

Improved factual accuracy

3️⃣ Clean Multi-Agent Architecture

Sequential CrewAI workflow:

PDF Upload
   ↓
Embedding Retrieval (RAG)
   ↓
Financial Analyst
   ↓
Risk Analyst
   ↓
Investment Advisor
Agent Responsibilities

Financial Analyst

Revenue analysis

Profitability breakdown

Liquidity summary

Risk Analyst

Liquidity risks

Margin pressure

Operational exposure

Investment Advisor

Buy/Hold/Sell recommendation

Risk-adjusted view

Optional external market insights

4️⃣ Controlled Search Tool Integration

Search tool is:

Restricted to Investment Advisor

Optional (not forced)

Clearly labeled under "External Market Insights"

Separated from document-derived facts

This prevents:

Data mixing

Fabricated statistics

ReAct parsing loops

🛠 Technology Stack

Python

FastAPI

CrewAI

Ollama (llama3)

nomic-embed-text embeddings

NumPy

LangChain PDF loader

⚙ Setup Instructions
1️⃣ Install Dependencies
pip install -r requirements.txt
2️⃣ Install Ollama

Download from:
https://ollama.com

3️⃣ Pull Required Models
ollama pull llama3
ollama pull nomic-embed-text
4️⃣ Set Environment Variable (for search tool)
export SERPER_API_KEY=your_key_here

(Windows PowerShell)

setx SERPER_API_KEY "your_key_here"
5️⃣ Run the Application
python main.py

Access API:

http://localhost:8000/docs
📡 API Documentation
🔹 Health Check
GET /

Response:

{
  "message": "Financial Document Analyzer API is running"
}
🔹 Analyze Financial Document
POST /analyze

Form Data:

file → PDF file

query → Optional user question

Example:

What was total revenue in Q2 2025?

Response:

{
  "status": "success",
  "filename": "report.pdf",
  "analysis": "..."
}
🧪 Example Test Queries
Financial Analysis

What was total revenue?

What was operating margin?

What were the key drivers of profitability?

Risk Assessment

What are the main liquidity risks?

Is margin compression a concern?

Investment Recommendation

Would you recommend buying this stock?

Is this suitable for conservative investors?

Market Insight (Search Tool)

How does this performance compare to current EV industry trends?

🧠 Design Decisions
Why Llama3?

Better ReAct formatting than smaller models

Stable multi-agent reasoning

Good balance of speed and quality


📈 Scalability Considerations

The system is modular and extensible:

Replace embeddings with FAISS/Chroma

Add database persistence layer

Add Redis/Celery worker queue

Swap LLM provider (OpenAI, Groq, Claude)

Deploy via Docker

🎯 Conclusion

This submission:

Fixes all deterministic bugs

Optimizes prompts for accuracy

Implements scalable RAG

Uses multi-agent orchestration correctly

Prevents hallucination

Maintains clean architecture

Meets all expected features

The system is stable, scalable, and production-aligned.
