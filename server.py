from fastapi import FastAPI
from pydantic import BaseModel
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

app = FastAPI(title="Customer Ticket Priority Analyzer")

# ---------------------------------------------------------------------------
# Sample dataset – raw customer messages only, as a customer would type them
# ---------------------------------------------------------------------------
SAMPLE_DATASET = [
    "I was charged twice for my subscription and need a refund.",
    "My account got hacked and I can't log in anymore.",
    "How do I change my email address in settings?",
    "The app keeps crashing every time I open it on iPhone.",
    "I cancelled my plan but still got charged this month.",
    "I need to download an invoice for my company records.",
    "My data was deleted after the update. I need it restored immediately.",
    "Can you explain the difference between Pro and Basic plans?",
]

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

llm = ChatAnthropic(model="claude-sonnet-4-20250514", max_tokens=1024)

chain = prompt | llm | JsonOutputParser()

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/dataset")
def get_dataset():
    return SAMPLE_DATASET

@app.post("/analyze", response_model=TicketResponse)
def analyze_ticket(req: TicketRequest):
    return chain.invoke({"message": req.message})
