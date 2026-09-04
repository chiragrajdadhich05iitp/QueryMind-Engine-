# QueryMind AI — Natural Language to SQL Analytics Engine

QueryMind AI is an intelligent data querying assistant built on top of LangChain, LangGraph, and Google Gemini. It bridges the gap between natural language questions and relational SQL databases, allowing users and stakeholders to extract actionable business insights without writing manual queries.

**Author:** Chirag Raj Dadhich


---

## Key Highlights

- **Automated Dialect Translation**: Translates ambiguous human questions into robust, dialect-accurate SQL queries.
- **Dynamic Schema Inspection**: Proactively inspects database tables, constraints, and sample data prior to query formulation.
- **Safety Enforcement**: Hardcoded guardrails prevent destructive DDL/DML execution (`DROP`, `DELETE`, `UPDATE`, `ALTER`).
- **Resilient Execution Loop**: Automatically catches syntax and schema errors, adjusts query logic, and retries.
- **Rich Terminal UI**: Delivers formatted tables and natural language summaries directly inside the console.

---

## Architectural Workflow

The agent follows an iterative ReAct execution pattern:

1. **Schema Discovery**: Evaluates table names and selects only the tables relevant to the prompt.
2. **Context Inspection**: Pulls column schemas and sample data rows to ensure accurate joins.
3. **Query Formulation**: Constructs SQL queries adhering to database dialect standards.
4. **Execution & Parsing**: Runs queries securely against the database engine.
5. **Synthesis**: Synthesizes the raw relational records into a human-readable summary.

---

## Project Structure

```text
querymind-ai/
├── agent.py              # Main execution logic and agent graph
├── chinook.db            # Sample SQLite relational database
├── requirements.txt      # Frozen environment dependencies
├── pyproject.toml        # Build configuration and project metadata
├── .env                  # Environment keys (gitignored)
├── .gitignore            # Version control exclusions
└── README.md             # Project documentation