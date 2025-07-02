Here’s a clear, professional **Product Requirements Document (PRD)** tailored to your Nexla AI website agent. This can be shared with stakeholders, teammates, or used as a base for sprint planning.

---

# 📄 Product Requirements Document (PRD)

**Product Name:** Ask Nexla (AI Website Assistant)
**Owner:** Krish Golcha
**Team:** Nexla AI
**Status:** Internal MVP

---

## 1. 🎯 Purpose

Enable users to query Nexla’s website content using natural language and receive intelligent, context-aware answers. This improves content discoverability and positions Nexla as an AI-forward company.

---

## 2. 🧠 Problem Statement

Nexla publishes high-value technical, thought-leadership, and customer content across multiple WordPress sections (Posts, Pages, Resources, Landing Pages). But:

* Users struggle to find relevant content quickly.
* Traditional search doesn’t handle nuance (e.g. “How does Nexla do R-ETL?”).
* Sales, marketing, and customer success need faster content access.

---

## 3. 🎯 Goals

| Goal                                 | Success Metric                               |
| ------------------------------------ | -------------------------------------------- |
| Let users ask free-form questions    | AI returns 90%+ relevant hits                |
| Cover full WordPress content base    | 100% coverage of Pages, Posts, etc.          |
| Build MVP chatbot UI                 | Works locally on `localhost:5000`            |
| Architect for future API/product use | Can be wrapped in Slackbot, GPT plugin, etc. |

---

## 4. 🧩 Features

### ✅ MVP Features (Completed)

| Feature               | Description                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| Data Crawler          | Indexed all WordPress content types: `posts`, `pages`, `resources`, `landing-pages` using REST API |
| Content Parser        | HTML stripped, structured as JSON, saved in `nexla_indexed_content.json`                           |
| RAG Engine            | Chunking + embeddings (via `sentence-transformers`) + FAISS similarity search                      |
| Lightweight Flask App | Exposes web UI and `/query` endpoint                                                               |
| Web UI                | Minimal `chat.html` with input box and chat-style output                                           |
| Query Loop            | Top-k semantic match returned to user using cosine similarity                                      |

---

### 🔜 Planned Features (V2)

| Feature                           | Priority | Description                                                |
| --------------------------------- | -------- | ---------------------------------------------------------- |
| ✳️ Cached FAISS Index             | High     | Speed up cold starts, avoid recomputation                  |
| ✳️ GPT/Claude Summarizer          | High     | Generate human-like, summarized answers from top documents |
| ✳️ Source Snippets                | Medium   | Show link preview + highlights in answers                  |
| ✳️ Slack/Gmail/Widget integration | Medium   | Embed into comms stack                                     |
| ✳️ Feedback loop                  | Low      | "Was this helpful?" toggle → logs for retraining           |

---

## 5. 🧱 Architecture Overview

```text
     +-------------+        +----------------+       +-------------+
     | User Query  | --->   |   Flask App     | --->  |  RAG Engine |
     | (chat.html) |        | (app.py)        |       | (rag.py)    |
     +-------------+        +----------------+       +-------------+
                                      |                        |
                                      v                        v
                            Load Indexed JSON        FAISS + Embeddings
                         (nexla_indexed_content.json)
```

---

## 6. 🧪 Testing Plan

| Test       | Method                                                    |
| ---------- | --------------------------------------------------------- |
| API Load   | `curl` or Postman to `/query`                             |
| Latency    | Log timings on FAISS vs GPT summary                       |
| Relevance  | Ask 10 pre-defined user queries and verify ranked answers |
| Edge Cases | Empty query, non-English query, long paragraphs           |

---

## 7. ⚙️ Tech Stack

| Component     | Tech                  |
| ------------- | --------------------- |
| Backend       | Python + Flask        |
| Embeddings    | Sentence Transformers |
| Vector Search | FAISS                 |
| Data Source   | WordPress REST API    |
| Frontend      | HTML + JS (static)    |
| Deployment    | Localhost (MVP)       |

---

## 8. 📁 Repository Layout

```
ask-nexla/
├── app.py                 # Flask server
├── rag.py                 # RAG engine logic
├── indexing_script.py     # WordPress scraper
├── nexla_indexed_content.json  # Indexed content
├── static/
│   └── chat.html          # Frontend
├── requirements.txt
```

---