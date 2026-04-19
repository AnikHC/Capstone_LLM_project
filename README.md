# 🤖 AI Course Assistant (RAG + LangGraph)

## 📌 Overview

This project is a Retrieval-Augmented Generation (RAG) based AI assistant built using LangGraph. It answers user queries based on a knowledge base of DBMS (Database Management Systems) documents.

The system combines:

* Vector database (ChromaDB)
* Local LLM (Mistral via Ollama)
* LangGraph workflow (modular nodes)
* Streamlit UI for interaction

---

## 🚀 Features

* 🔍 **RAG-based Question Answering**
* 🧠 **Conversation Memory (multi-turn chat)**
* 🔀 **Router Node** (decides between retrieval or tool)
* 🧮 **Tool Support** (basic calculations)
* 📊 **Evaluation Node** (checks relevance & faithfulness)
* 🌐 **Streamlit Web Interface**

---

## 🏗️ Project Structure

```
capstone_project/
│
├── data/                # PDF documents
├── db/                  # Vector database (ChromaDB)
├── modules/
│   ├── loader.py
│   ├── splitter.py
│   ├── vectorstore.py
│   └── retriever.py
│
├── graph.py             # LangGraph workflow
├── app.py               # Streamlit UI
├── capstone.ipynb       # Development notebook
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd capstone_project
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install Ollama (for local LLM)

Download from:
👉 https://ollama.com

Then run:

```bash
ollama pull mistral
```

---

## 📂 Preparing the Database

1. Add PDF documents to:

```
data/
```

2. Run the notebook (`capstone.ipynb`) to:

* Load documents
* Split into chunks
* Create vector database

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

Then open browser:

```
http://localhost:8501
```

---

## 💡 How to Use

1. Enter a question in the input box
2. Click **Ask**
3. View:

   * 🧠 Answer
   * 📊 Evaluation (relevance & faithfulness)
4. Continue asking follow-up questions (memory supported)

---

## 🧪 Example Queries

* What is normalization in DBMS?
* Why is it important?
* What is indexing?
* What is 25 * 12? (tool usage)

---

## 🧠 Architecture

```
User
 ↓
Memory Node
 ↓
Router Node
 ↓        ↓
Retrieve   Tool
 ↓          ↓
      Answer Node
          ↓
    Evaluation Node
          ↓
       Output
```

---

## 🔮 Future Improvements

* Add RAGAS evaluation metrics
* Improve retrieval with hybrid search
* Add streaming responses in UI
* Support multiple domains

---

## 👨‍💻 Author

Anik Hussain Chatterjee
