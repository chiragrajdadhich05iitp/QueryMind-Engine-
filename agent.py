import os
import sys
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

# Load environment variables
load_dotenv()

console = Console()

def get_database_connection(db_path: str = "chinook.db") -> SQLDatabase:
    if not os.path.exists(db_path):
        console.print(f"[bold red]Error:[/bold red] Database file '{db_path}' not found.")
        sys.exit(1)
    return SQLDatabase.from_uri(f"sqlite:///{db_path}", sample_rows_in_table_info=3)

def build_sql_agent(db: SQLDatabase):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        console.print("[bold red]Configuration Error:[/bold red] GEMINI_API_KEY is missing in .env.")
        sys.exit(1)

    # Set Gemini LLM with native Google GenAI
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
        google_api_key=api_key,
    )
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools()

    system_prompt = (
        f"You are QueryMind, an expert SQL data assistant designed to answer database questions.\n"
        f"Database Dialect: {db.dialect}\n"
        f"Guidelines:\n"
        f"1. Check tables and schema before constructing queries.\n"
        f"2. Never execute destructive DDL/DML statements (DROP, DELETE, UPDATE, INSERT, ALTER).\n"
        f"3. Only use existing column and table names.\n"
        f"4. Limit SELECT queries to top 5 results unless specified otherwise.\n"
        f"5. Provide a clear summary alongside the raw numerical result."
    )

    return create_react_agent(llm, tools, prompt=system_prompt)

def query_database(user_prompt: str):
    db = get_database_connection()
    agent_executor = build_sql_agent(db)

    console.print(Panel.fit(f"[bold cyan]Prompt:[/bold cyan] {user_prompt}", title="QueryMind SQL Engine"))
    
    response = agent_executor.invoke({"messages": [("user", user_prompt)]})
    raw_content = response["messages"][-1].content

    # Gemini list of dicts/chunks return kare toh extract text
    if isinstance(raw_content, list):
        text_chunks = []
        for chunk in raw_content:
            if isinstance(chunk, dict) and "text" in chunk:
                text_chunks.append(chunk["text"])
            elif isinstance(chunk, str):
                text_chunks.append(chunk)
            elif hasattr(chunk, "text"):
                text_chunks.append(chunk.text)
        final_output = "\n".join(text_chunks)
    else:
        final_output = str(raw_content)

    console.print(Panel(Markdown(final_output), title="[bold green]Query Result[/bold green]"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Usage:[/yellow] python agent.py \"<your question here>\"")
        console.print("[dim]Example: python agent.py \"Show top 5 customers by total invoice spend\"[/dim]")
        sys.exit(0)
    
    user_query = " ".join(sys.argv[1:])
    query_database(user_query)