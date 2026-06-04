# AI-Powered Customer Support Ticket Analyzer

Analyzes customer support messages using **Gemini 2.5 Flash** and returns structured output — category, priority, escalation status, and a suggested reply. Every analysis is saved to an Excel file for further use.

---

## How It Works

You paste a customer message like:

> "I was charged twice for my subscription and need a refund."

The AI reads it and returns:

| Field | Example |
|---|---|
| Category | Billing |
| Priority | High |
| Escalation | Required |
| Extracted Details | duplicate charge, refund request |
| Response Draft | A ready-to-send professional reply |

Every result is **automatically appended** to `ticket_analysis.xlsx`. You can download the full history anytime from the UI and share it with the relevant team (billing, tech support, security, etc.) or use it for reporting and analysis.

---

## Workflow

```
Customer message (typed in UI)
        ↓
Streamlit UI  →  POST /analyze  →  FastAPI Server
                                        ↓
                              LangChain: prompt | Gemini | JSON
                                        ↓
                         Category, Priority, Escalation, Draft
                                        ↓
                      Auto-saved to ticket_analysis.xlsx
                                        ↓
                  Download Excel from UI → share with team
```

---

## Run It on Your PC

### 1. Clone the repo

```bash
git clone https://github.com/Jayakrishna143/AI-Powered-Customer-Support-Ticket-Analysis-System.git
cd AI-Powered-Customer-Support-Ticket-Analysis-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Install dependencies

```bash
.venv\Scripts\pip install -r requirements.txt   # Windows
# or
.venv/bin/pip install -r requirements.txt        # Mac/Linux
```

### 4. Add your Gemini API key

Create a `.env` file in the project root:

```
GOOGLE_API_KEY=your_api_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com)

### 5. Start the app

```bash
python run.py
```

Open **http://localhost:8501** in your browser.

---

## Excel Export

- Every ticket analysis is saved to `ticket_analysis.xlsx` automatically
- Click **"Download Excel Report"** in the UI to download the full history
- Use the file to route tickets to the right team, track trends, or import into any CRM/spreadsheet tool

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Gemini 2.5 Flash |
| AI Framework | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| Export | pandas + openpyxl |
