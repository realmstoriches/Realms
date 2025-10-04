\# LangChain Overview



LangChain is a framework for building applications powered by language models. It enables chaining together LLMs with tools, memory, agents, and external data sources.



\## Core Concepts



\- \*\*Chains\*\*: Sequences of calls (e.g., prompt → LLM → output).

\- \*\*Agents\*\*: Autonomous decision-makers that choose tools based on user input.

\- \*\*Tools\*\*: External functions or APIs the agent can invoke.

\- \*\*Memory\*\*: Persistent context across interactions.

\- \*\*Retrievers\*\*: Interfaces to vector stores like ChromaDB.



\## Use Cases



\- RAG pipelines

\- Autonomous agents

\- Conversational apps

\- Code generation

\- Knowledge ingestion



\## Example



```python

from langchain.agents import initialize\_agent

from langchain.tools import Tool



tools = \[Tool(name="Search", func=search\_web)]

agent = initialize\_agent(tools, llm, agent\_type="zero-shot-react-description")

