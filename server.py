from fastapi import FastAPI
from pydantic import BaseModel
import anthropic
import json

app = FastAPI()
client = anthropic.Anthropic()

SAMPLE_DATASET = [
    {"message": "I was charged twice for my subscription and need a refund.", "category": "Billing", "priority": "High"},
    {"message": "My account got hacked and I can't log in anymore.", "category": "Security", "priority": "Critical"},
    {"message": "How do I change my email address in settings?", "category": "Account", "priority": "Low"},
    {"message": "The app keeps crashing every time I open it on iPhone.", "category": "Technical", "priority": "Medium"},
    {"message": "I cancelled my plan but still got charged this month.", "category": "Billing", "priority": "High"},
    {"message": "I need to download an invoice for my company records.", "category": "Billing", "priority": "Low"},
    {"message": "My data was deleted after the update. I need it restored immediately.", "category": "Technical", "priority": "Critical"},
    {"message": "Can you explain the difference between Pro and Basic plans?", "category": "General", "priority": "Low"},
]

class TicketRequest(BaseModel):
    message: str

class TicketResponse(BaseModel):
    category: str
    priority: str
    extracted_details: list[str]
    response_draft: str
    escalation: str

@app.get("/dataset")
def get_dataset():
    return SAMPLE_DATASET

@app.post("/analyze", response_model=TicketResponse)
def analyze_ticket(req: TicketRequest):
    prompt = f"""You are a customer support analyst. Analyze the following support message and return a JSON object with exactly these fields:

- category: one of [Billing, Technical, Account, Security, General]
- priority: one of [Low, Medium, High, Critical]
- extracted_details: a list of 2-4 short key phrases summarizing the issue
- response_draft: a professional, empathetic reply to the customer (2-3 sentences)
- escalation: either "Required" or "Not Required"

Rules for escalation: mark Required if priority is Critical or High, or if it involves security/fraud/data loss.

Support message: "{req.message}"

Return ONLY valid JSON, no extra text."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)
    return data
