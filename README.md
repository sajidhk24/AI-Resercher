# AI Research Assistant

A modular, agent-based academic research assistant powered by LLMs and Streamlit.  
This tool automates the process of searching, summarizing, evaluating, synthesizing, and drafting academic research documents.

---

## Architecture Overview

The solution is built as a pipeline of specialized agents, each responsible for a distinct stage in the research workflow:

1.   Search Agent  : Retrieves relevant academic papers from arXiv (with Serper web search fallback).
2.   Summariser Agent  : Summarizes each paper’s abstract into structured JSON.
3.   Evaluator Agent  : Evaluates each summary for reliability, methodology, and quality.
4.   Synthesizer Agent  : Integrates all summaries, weighting them by evaluation scores, to produce a synthesized report.
5.   Writer Agent  : Drafts a professional research document (IMRaD structure) from the synthesized report.
6.   Orchestration Layer (Streamlit UI)  : Manages user interaction and sequential execution of agent nodes.

---

## Architecture Diagram

![Agent Architecture Diagram](https://i.imgur.com/2Qw6QwF.png)

---

## Features

-   Automated Literature Search   (arXiv + Serper fallback)
-   LLM-powered Summarization and Evaluation  
-   Weighted Synthesis of Research Findings  
-   Professional Academic Writing (IMRaD format)  
-   Interactive Streamlit UI  
-   Caching and Rate Limiting for API efficiency
- LangGraph-style agent: a stateful, directed-graph workflow that coordinates multiple LLM or tool-call nodes, enabling multi-step reasoning and self-correction. It's a powerful modern agent architecture—far more structured and flexible than a simple chain of prompts.
- AgentState Class to maintain States 

---

## Getting Started

### Prerequisites

- Python 3.9+
- [Streamlit](https://streamlit.io/)
- [LangChain](https://python.langchain.com/)
- [arxiv](https://pypi.org/project/arxiv/)
- [langchain-google-genai](https://pypi.org/project/langchain-google-genai/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [requests](https://pypi.org/project/requests/)

### Installation

```bash
git clone https://github.com/yourusername/ai-research-assistant.git
cd ai-research-assistant
pip install -r requirements.txt
```
## Run
streamlit run main.py

/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m streamlit run main.py
