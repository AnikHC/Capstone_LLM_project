from typing import TypedDict, List
from langgraph.graph import StateGraph
from modules.retriever import query_db
from langchain_ollama import ChatOllama

llm = ChatOllama(model="mistral", temperature=0)

class State(TypedDict):
    question: str
    context: str
    answer: str
    history: List[str]
    route: str
    evaluation: str


def memory_node(state: State):
    history = state.get("history", [])
    history.append(f"User: {state['question']}")
    return {"history": history}


def router_node(state: State):
    question = state["question"]

    routing_prompt = f"""
Classify the question into:
- retrieval → DBMS / normalization related
- tool → math / calculation / general

Question: {question}

Answer only: retrieval or tool
"""

    decision = llm.invoke(routing_prompt).content.strip().lower()

    if "tool" in decision:
        return {"route": "tool"}
    return {"route": "retrieve"}


def retrieve_node(state: State):
    query = state["question"]
    history = state.get("history", [])

    follow_up_words = ["why", "how", "explain", "advantages", "disadvantages"]
    is_follow_up = any(query.lower().startswith(w) for w in follow_up_words)

    if history and is_follow_up:
        recent_history = "\n".join(history[-4:])

        rewrite_prompt = f"""
Rewrite the follow-up question into a standalone question.

Conversation:
{recent_history}

Follow-up:
{query}

Return only the rewritten question.
"""
        query = llm.invoke(rewrite_prompt).content.strip()

    docs = query_db(query, k=5)

    context = "\n\n".join([doc.page_content[:500] for doc in docs])

    return {"context": context}


def tool_node(state: State):
    question = state["question"]

    tool_prompt = f"""
Solve the following:

{question}

Give only the final answer.
"""

    result = llm.invoke(tool_prompt).content.strip()

    return {"context": result}


def answer_node(state: State):
    history_text = "\n".join(state.get("history", [])[-6:])

    prompt_text = f"""
You are a helpful assistant.

Use context + conversation.

Rules:
- Keep answers short (3–5 lines)
- Do not copy text directly
- Stay on topic
- If not found, say:
  "I don't know based on the provided documents"

Conversation:
{history_text}

Context:
{state.get('context', '')}

Question:
{state['question']}

Answer:
"""

    response = llm.invoke(prompt_text)
    answer = response.content.strip()

    history = state.get("history", [])
    history.append(f"Assistant: {answer}")

    return {"answer": answer, "history": history}


def evaluation_node(state: State):
    question = state["question"]
    answer = state["answer"]
    context = state.get("context", "")

    eval_prompt = f"""
Evaluate the answer:

Question: {question}
Answer: {answer}
Context: {context}

Return:
relevant: yes/no
faithful: yes/no
"""

    result = llm.invoke(eval_prompt).content.strip()

    return {"evaluation": result}


builder = StateGraph(State)

builder.add_node("memory", memory_node)
builder.add_node("router", router_node)
builder.add_node("retrieve", retrieve_node)
builder.add_node("tool", tool_node)
builder.add_node("answer", answer_node)
builder.add_node("evaluation", evaluation_node)

builder.set_entry_point("memory")

builder.add_edge("memory", "router")

def route_decision(state: State):
    return state["route"]

builder.add_conditional_edges(
    "router",
    route_decision,
    {
        "retrieve": "retrieve",
        "tool": "tool"
    }
)

builder.add_edge("retrieve", "answer")
builder.add_edge("tool", "answer")
builder.add_edge("answer", "evaluation")

graph = builder.compile()