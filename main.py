import os
import uuid
import asyncio
import warnings

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from crewai import Crew, Process

from agents import financial_analyst, risk_analyst, investment_advisor
from task import (
    financial_analysis_task,
    risk_assessment_task,
    investment_task
)
from tools import (
    extract_pdf_text,
    chunk_text,
    get_embedding,
    retrieve_relevant_chunks,
    search_tool
)

warnings.filterwarnings("ignore")

app = FastAPI(title="Financial Document Analyzer")


# =====================================
# Run Crew
# =====================================

def run_crew(query: str, document_context: str, external_context: str):

    crew = Crew(
        agents=[financial_analyst, risk_analyst, investment_advisor],
        tasks=[
            financial_analysis_task,
            risk_assessment_task,
            investment_task
        ],
        process=Process.sequential
    )

    return crew.kickoff(
        inputs={
            "query": query,
            "document_context": document_context,
            "external_context": external_context
        }
    )


# =====================================
# Health Check
# =====================================

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


# =====================================
# Analyze Endpoint
# =====================================

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a comprehensive financial analysis.")
):

    file_id = str(uuid.uuid4())
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", f"{file_id}.pdf")

    try:
        # Save file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        # =====================================
        # RAG: Document Retrieval
        # =====================================

        full_text = extract_pdf_text(file_path)
        chunks = chunk_text(full_text, chunk_size=1200)

        chunk_embeddings = [get_embedding(chunk) for chunk in chunks]

        relevant_chunks = retrieve_relevant_chunks(
            chunks,
            chunk_embeddings,
            query,
            top_k=5
        )

        document_context = "\n\n".join(relevant_chunks)

        # =====================================
        # Deterministic External Search
        # =====================================

        industry_keywords = [
            "industry",
            "market",
            "competitor",
            "sector",
            "macro",
            "trend",
            "compare",
            "performance"
        ]

        external_context = ""

        if any(word in query.lower() for word in industry_keywords):
            try:
                enhanced_query = (
                    "Tesla Q2 2025 financial performance comparison "
                    "with BYD and Rivian current EV industry trends"
                )
                external_context = search_tool.run(enhanced_query)
            except Exception:
                external_context = ""

        # =====================================
        # Run Crew (Non-blocking)
        # =====================================

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            run_crew,
            query.strip(),
            document_context,
            external_context
        )

        return {
            "status": "success",
            "filename": file.filename,
            "analysis": str(response)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# =====================================
# Dev Server
# =====================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)