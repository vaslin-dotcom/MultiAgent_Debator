# Multi-Agent Debate System

A LangGraph-based multi-agent system where two AI debaters argue 
opposing sides of a topic across multiple rounds, with a judge 
delivering a final verdict.

## Architecture
- **Main Graph** — organiser → debate → judge
- **Subgraph** — generator → researcher → regenerator (runs per debater per round)

## Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your API key:
GROQ_API_KEY=your_key_here

## Run
python run.py
```

Ctrl + K  →  write message  →  Commit and Push