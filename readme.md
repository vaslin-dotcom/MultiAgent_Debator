# ⚔️ MultiAgent Debater — Let AIs Fight It Out

> *"Two AIs walk into a debate. Only one argument survives."*

Ever wondered what happens when you pit two AI agents against each other, arm them with real-time internet research, and make them argue for 5 rounds while their topics **evolve** based on what they said before?

**This project does exactly that.**

---

## 🤔 What Makes This Different?

Most "AI debate" projects do this:
```
AI A says something → AI B says something → done.
```

This project does this:
```
Round 1: AI A researches + argues → AI B researches + counters
         ↓
         Organiser reads both arguments and finds NEW angles
         ↓
Round 2: Both agents research the NEW angles + argue harder
         ↓
         ... 5 rounds of escalating intellectual warfare ...
         ↓
Judge reads everything → delivers structured verdict with reasoning
```

The debate **gets smarter every round** because the topics evolve based on what was actually argued. No two runs are ever the same.

---

## ✨ Features That Actually Matter

**🔄 Self-Evolving Topics**
The organiser agent reads every argument after each round and finds new angles, deeper perspectives, and unexplored sub-topics. Round 1 might be broad. Round 5 will be razor-specific.

**🔍 Real-Time Web Research Per Agent**
Before each argument, every agent searches the internet for evidence. They're not just using training data — they're actively researching to counter the opponent's last move.

**🏗️ One Subgraph, Two Debaters**
Both debaters run the same internal pipeline: `generate → research → regenerate`. Built once as a LangGraph subgraph, reused independently for each agent. Clean, elegant, no code duplication.

**⚖️ Structured Judge Verdict**
The judge doesn't just pick a winner. It summarizes both sides, states a conclusion, and gives numbered reasoning. Like a real courtroom verdict.

---

## 🏛️ Architecture

```
USER INPUT (topic)
      │
      ▼
┌─────────────────────────────────────────────┐
│                 MAIN GRAPH                  │
│                                             │
│  organiser_node                             │
│  → splits topic into two debater positions │
│  → after each round: evolves the topics    │
│         │                                   │
│         ▼                                   │
│  debate_node                                │
│  → runs Agent A subgraph                   │
│  → runs Agent B subgraph                   │
│         │                                   │
│         ▼                                   │
│  condition: count <= 5? ──→ organiser_node  │
│             count > 5?  ──→ judge_node      │
│                                             │
│  judge_node                                 │
│  → summarise → conclude → reason → verdict │
└─────────────────────────────────────────────┘

Each agent runs this SUBGRAPH independently:

  generator_node          research_node         regenerator_node
  ───────────────    →    ─────────────    →    ────────────────
  Build 3 strong          Search internet       Combine initial
  initial points          for evidence to       points + research
  for the topic           counter opponent      into final argument
```

---

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/multiagent-debater.git
cd multiagent-debater
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up your API key**

Create a `.env` file in the root folder:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

**4. Run it**
```bash
python run.py
```

**5. Enter any debate topic when prompted**
```
Enter your topic: Is remote work better than office work?
```

Then sit back and watch two AIs go to war. 🍿

---

## 📦 Project Structure

```
multiagent-debater/
│
├── run.py              ← start here, streaming output
├── main_graph.py       ← main LangGraph orchestration
├── subgraph.py         ← debater agent subgraph (reused for both agents)
├── schemas.py          ← state definitions + LLM setup
├── prompts.py          ← all prompt templates
├── requirements.txt
└── .env                ← your API keys (never committed)
```

---

## 🎬 Sample Output

```
🏛️  DEBATE IN PROGRESS...
──────────────────────────────────────────────────

📋 ORGANISER — Round topics assigned:
   Debater A: T20I — Speed, Spectacle and Global Reach
   Debater B: Test Cricket — Strategy, Legacy and Depth

⚔️  ROUND 1 ARGUMENTS:
────────────────────────────────────────
🔵 DEBATER A:
The T20 format has revolutionized cricket by merging speed and
innovation, creating a seismic shift in fan engagement...

🔴 DEBATER B:
Test cricket's strategic complexity — where captains plan for
days, not overs — offers a nuance absent in formats dominated
by instant spectacle...

📋 ORGANISER — Round 2 topics assigned:
   Debater A: Short-Form Formats as Catalysts for Grassroots Growth
   Debater B: Commercialization vs Sporting Integrity
              ↑ topics evolved based on round 1 arguments

... 3 more rounds of escalation ...

🔨 JUDGE'S VERDICT
──────────────────────────────────────────────────
After reviewing all arguments, Test cricket remains the
best format. Reasoning: 1) Strategic uniqueness...
2) Cultural preservation... 3) Symbiotic coexistence...
──────────────────────────────────────────────────
✅ Debate complete.
```

---

## 🛠️ Built With

| Tool | Role |
|------|------|
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Multi-agent graph orchestration |
| [LangChain](https://www.langchain.com/) | LLM abstractions and tool use |
| [Groq](https://groq.com/) | Fast LLM inference (Qwen3, GPT-OSS) |
| [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) | Real-time web research |
| [Pydantic](https://docs.pydantic.dev/) | Structured LLM outputs |

---

## 💡 What I Learned Building This

- How to design **separate states** for parent and child graphs
- How to **reuse one subgraph** for multiple agents without code duplication
- How `stream_mode="updates"` works for real-time node-by-node output
- Why `Annotated[int, add]` reducers need careful off-by-one thinking
- How to strip `<think>` tags from reasoning models cleanly

---

## 🗺️ What's Next

- [ ] Streamlit UI with live streaming debate feed
- [ ] Human-in-the-loop: pause before verdict, let user add their take
- [ ] Configurable round count at runtime
- [ ] Parallel agent research using LangGraph's `Send` API
- [ ] Export debate transcript as PDF

---

## 🤝 Contributing

Found a bug? Have a wild debate topic idea? Want to add a third agent as a devil's advocate?

PRs are welcome. Open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT — use it, break it, improve it, debate about it.

---

<div align="center">
  <i>Built with curiosity, LangGraph, and a desire to watch AIs argue.</i>
</div>
