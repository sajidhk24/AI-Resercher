import streamlit as st
import os, requests, json, re
from dotenv import load_dotenv
import arxiv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def search_papers(query):
    try:
        results = arxiv.Search(query=query, max_results=3, sort_by=arxiv.SortCriterion.Relevance)
        papers = [{
            "title": r.title,
            "authors": [a.name for a in r.authors],
            "abstract": r.summary.strip(),
            "url": r.entry_id
        } for r in results.results()]
        if papers: return papers
    except: pass
    # Fallback: Serper
    try:
        resp = requests.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": SERPER_API_KEY},
            json={"q": f"{query} research paper", "num": 3}
        )
        snippets = [o.get("snippet", "") for o in resp.json().get("organic", [])]
        return [{"title": "Web result", "authors": [], "abstract": "\n".join(snippets), "url": ""}]
    except: return []

def summarize(abstract):
    prompt = f'''Summarize this academic abstract as JSON with keys: summary, findings, themes, data_insights, surprises, implications. Only output JSON. Text: {abstract}'''
    resp = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    txt = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    match = re.search(r"(\{.*\})", txt, re.DOTALL)
    try: return json.loads(match.group(1)) if match else {"summary": abstract}
    except: return {"summary": abstract}

def evaluate(summary):
    prompt = f'''Evaluate this summary for reliability, methodology, quality (0-1 each). Output JSON. Summary: {summary}'''
    resp = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    txt = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    match = re.search(r"(\{.*\})", txt, re.DOTALL)
    try: return json.loads(match.group(1)) if match else {"reliability": 0, "methodology": 0, "quality": 0}
    except: return {"reliability": 0, "methodology": 0, "quality": 0}

def synthesize(summaries, evals):
    items = [f"Summary: {json.dumps(s)}\nEval: {json.dumps(e)}" for s, e in zip(summaries, evals)]
    prompt = f"Synthesize these into a report, weighting by eval scores. If data is insufficient, still provide any findings or analysis you can extract:\n{chr(10).join(items)}"
    resp = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    txt = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    # Always return whatever the LLM gives, even if minimal
    return txt.strip() if txt.strip() else "No synthesis available, but here are the raw findings:\n" + "\n".join([json.dumps(s) for s in summaries])

def draft(report):
    prompt = f"Write an academic IMRaD paper (~1500 words) from this report. Cite as 'Synthesized data'. If data is limited, still present whatever findings and analysis are available.\nReport: {report}"
    resp = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
        params={"key": GEMINI_API_KEY},
        json={"contents": [{"parts": [{"text": prompt}]}]}
    )
    txt = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    return txt.strip() if txt.strip() else "No document could be generated, but here is the synthesized report:\n" + report

def main():
    st.title("AI Research Assistant")
    query = st.text_input("Research Query", "")
    if st.button("Start Research") and query:
        with st.spinner("Processing..."):
            papers = search_papers(query)
            if not papers:
                st.error("No papers found.")
                return
            summaries = [summarize(p["abstract"]) for p in papers]
            evals = [evaluate(json.dumps(s)) for s in summaries]
            report = synthesize(summaries, evals)
            doc = draft(report)
        st.subheader("Papers")
        for p in papers:
            st.markdown(f"- [{p['title']}]({p['url']})")
        st.subheader("Summaries & Evaluations")
        for s, e in zip(summaries, evals):
            st.write("Summary:", s)
            st.write("Evaluation:", e)
        st.subheader("Synthesized Report")
        st.write(report)
        st.subheader("Drafted Document")
        st.text_area("Document", doc, height=400)
        st.download_button("Download Document", doc, "research_document.txt")
if __name__ == "__main__": main()