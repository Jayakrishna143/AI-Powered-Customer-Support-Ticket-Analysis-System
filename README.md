# AI-Powered Customer Support Ticket Analyzer

A lightweight AI application that reads a plain customer support message and instantly tells you what it's about, how urgent it is, whether it needs escalation, and even drafts a professional reply — powered by **Gemini 2.5 Flash** via **LangChain**.

---

## What It Does

When a customer sends a support message like:

> "I was charged twice for my subscription and need a refund."

The system analyzes it and returns:

| Field | Example Output |
|---|---|
| Category | Billing |
| Priority | High |
| Extracted Details | payment issue, duplicate charge, refund request |
| Response Draft | A ready-to-send professional reply |
| Escalation | Required |

The customer types a plain message — they don't know about internal categories or priority levels. The model figures out everything.

---

## Project Structure

```
project/
├── server.py         # FastAPI backend — LangChain chain + analysis logic
├── streamlit_app.py  # Streamlit frontend — the UI you interact with
├── run.py            # Launcher — starts both server and UI together
├── requirements.txt  # Python dependencies
└── README.md
```

---

## Approach & Architecture

### Framework: LangChain

The analysis logic is built using a minimal LangChain chain:

```
prompt | llm | JsonOutputParser
```

- **`ChatPromptTemplate`** — defines the system instruction and injects the user message
- **`ChatGoogleGenerativeAI`** — calls Gemini 2.5 Flash to process the ticket
- **`JsonOutputParser`** — parses the model's JSON output directly into a Python dict

### Model: Gemini 2.5 Flash (`gemini-2.5-flash`)

Previously the project used Claude (Anthropic). It has been migrated to **Google's Gemini 2.5 Flash** via `langchain-google-genai`. Key settings:

| Setting | Value |
|---|---|
| Model | `gemini-2.5-flash` |
| `max_tokens` | `2000` |
| `temperature` | `0.2` |

`temperature=0.2` keeps the output consistent and factual — low enough to be reliable for classification tasks, with a little room for natural language in the response draft.

### Chain in code

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

prompt = ChatPromptTemplate.from_messages([
    ("system", "...system instructions..."),
    ("human", "{message}"),
])

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", max_tokens=2000, temperature=0.2)

chain = prompt | llm | JsonOutputParser()
```

The FastAPI route then just calls:

```python
chain.invoke({"message": req.message})
```

### Input validation: Pydantic

The API uses Pydantic models to validate input and document the output shape:

```python
class TicketRequest(BaseModel):
    message: str          # plain customer message string

class TicketResponse(BaseModel):
    category: str
    priority: str
    extracted_details: list[str]
    response_draft: str
    escalation: str
```

### Sample Dataset

The dataset is a plain list of customer message strings — no labels, no categories, no priorities. Those fields are internal to the company; a customer simply describes their problem.

```python
SAMPLE_DATASET = [
    "I was charged twice for my subscription and need a refund.",
    "My account got hacked and I can't log in anymore.",
    ...
]
```

---

## How It Works

```
User types a plain message
        |
        v
Streamlit UI (port 8501)
        |
  HTTP POST /analyze  { "message": "..." }
        |
        v
FastAPI Server (port 8000)
        |
  LangChain chain:
  prompt | llm | JsonOutputParser
        |
        v
Gemini 2.5 Flash returns structured JSON
        |
        v
UI displays: category, priority, details, draft, escalation
```

---

## Setup and Installation

### 1. Clone or download the project

Make sure you have all files: `server.py`, `streamlit_app.py`, `run.py`, `requirements.txt`

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Google API key

You need a Gemini API key from [https://aistudio.google.com](https://aistudio.google.com)

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_api_key_here
```

Or set it as an environment variable:

**Mac/Linux:**
```bash
export GOOGLE_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

### 5. Run the app

```bash
python run.py
```

Open your browser at:

```
http://localhost:8501
```

---

## Using the App

The UI has two tabs:

**Analyze Ticket**
Type any customer support message in the text box and click Analyze. You'll see the category, priority, escalation status, key details, and a suggested reply.

**Sample Dataset**
8 pre-loaded customer messages across different issue types. Click "Analyze this" on any message to see the AI output for it.

---

## API Endpoints

**Analyze a ticket**
```
POST http://localhost:8000/analyze
Content-Type: application/json

{
  "message": "I was charged twice for my subscription and need a refund."
}
```

**Get sample dataset**
```
GET http://localhost:8000/dataset
```

Auto-generated API docs:
```
http://localhost:8000/docs
```

---

## Requirements

- Python 3.9 or higher
- A Google Gemini API key (get one at https://aistudio.google.com)
- `langchain-google-genai`, `langchain-core`, `fastapi`, `uvicorn`, `streamlit`

---

## Troubleshooting

**`GOOGLE_API_KEY` not set**
Make sure the key is set in your `.env` file or in the terminal session where you run the app.

**Port already in use**
If 8000 or 8501 is occupied, stop other running processes or change the port numbers in `run.py` and `streamlit_app.py`.

**JSON parse error**
Rare. Gemini occasionally wraps output in markdown fences. `JsonOutputParser` from LangChain handles stripping these automatically.
