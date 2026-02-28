import warnings
import os
# This must happen BEFORE any other imports
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.simplefilter("ignore")

# Specific Pydantic suppression
try:
    from pydantic import PydanticDeprecatedSince20
    warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)
except ImportError:
    pass


from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst
from task import analyze_financial_document

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )
    
    result = financial_crew.kickoff({'query': query, 'file_path': file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

# 1. Rename the endpoint function to avoid collision with the Task import
@app.post("/analyze")
async def handle_analysis_request(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    file_id = str(uuid.uuid4())
    # Ensure directory exists before defining path
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", f"document_{file_id}.pdf")
    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 2. Use run_in_executor to prevent blocking the event loop
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None, 
            run_crew, 
            query.strip() or "Analyze document", 
            file_path
        )
        
        return {
            "status": "success",
            "analysis": str(response),
            "file": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def run_crew(query: str, file_path: str):
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_financial_document],
        process=Process.sequential,
    )
    # 3. Add the 'inputs=' keyword
    return financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})

if __name__ == "__main__":
    import uvicorn
    # 4. Use string notation for reliable reloading
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)