from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import pandas as pd
from datetime import datetime

app = FastAPI(title="Customer Ticket Priority Analyzer")

EXCEL_FILE = "ticket_analysis.xlsx"

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class TicketRequest(BaseModel):
    message: str

class TicketResponse(BaseModel):
    category: str
    priority: str
    extracted_details: list[str]
    response_draft: str
    escalation: str

# ---------------------------------------------------------------------------
# LangChain chain: prompt | llm | JsonOutputParser
# ---------------------------------------------------------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a customer support analyst.
Analyze the customer message and return a JSON object with exactly these fields:

{{
  "category":          one of [Billing, Technical, Account, Security, General],
  "priority":          one of [Low, Medium, High, Critical],
  "extracted_details": list of 2-4 short key phrases summarizing the issue,
  "response_draft":    a professional, empathetic reply in 2-3 sentences,
  "escalation":        "Required" if priority is High or Critical, else "Not Required"
}}

Return ONLY valid JSON, no extra text."""),
    ("human", "{message}"),
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", max_tokens=2000, temperature=0.2)

chain = prompt | llm | JsonOutputParser()

# Helper: append a result row to the Excel file
def append_to_excel(message: str, result: dict):
    row = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Customer Message": message,
        "Category": result.get("category", ""),
        "Priority": result.get("priority", ""),
        "Extracted Details": " | ".join(result.get("extracted_details", [])),
        "Response Draft": result.get("response_draft", ""),
        "Escalation": result.get("escalation", ""),
    }

    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
        df_new = pd.concat([df_existing, pd.DataFrame([row])], ignore_index=True)
    else:
        df_new = pd.DataFrame([row])

    df_new.to_excel(EXCEL_FILE, index=False)

# Routes
@app.post("/analyze", response_model=TicketResponse)
def analyze_ticket(req: TicketRequest):
    result = chain.invoke({"message": req.message})
    append_to_excel(req.message, result)
    return result

@app.get("/export-excel")
def export_excel():
    if not os.path.exists(EXCEL_FILE):
        # Return an empty sheet if no data yet
        pd.DataFrame(columns=[
            "Timestamp", "Customer Message", "Category",
            "Priority", "Extracted Details", "Response Draft", "Escalation"
        ]).to_excel(EXCEL_FILE, index=False)

    return FileResponse(
        path=EXCEL_FILE,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="ticket_analysis.xlsx",
    )
