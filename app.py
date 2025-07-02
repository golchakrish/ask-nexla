from flask import Flask, request, jsonify, send_from_directory
import os
from dotenv import load_dotenv
import google.generativeai as genai
from rag import RAGIndex
import re

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('models/gemini-1.5-flash')
rag = RAGIndex("nexla_indexed_content.json")

app = Flask(__name__, static_folder="static")

BASIC_QA = {
    "who are you": "I am Nexla's website assistant, here to help you find information about Nexla.",
    "what can you do": "I can answer questions about Nexla's products, solutions, news, and resources by searching our website content.",
    "what is ask nexla": "Ask Nexla is an AI-powered assistant that helps you discover information from Nexla's website."
    # Add more as needed
}

NEXLA_RELATED_QUESTIONS = [
    "What is Nexla?",
    "How is Nexla different from traditional ETL tools?",
    "What data sources does Nexla support?",
    "Can Nexla automate data workflows?",
    "Can I speak to a data integration expert?"
]

def shorten_title(title, max_words=5):
    words = title.split()
    return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data["query"].strip().lower()
    history = data.get("history", [])
    # Check for basic Q&A
    for key in BASIC_QA:
        if key in question:
            return jsonify({"answer": BASIC_QA[key], "references": []})

    top_docs = rag.query(question, k=3)
    context = "\n\n".join([doc["content"] for doc in top_docs])

    # Build conversation history for prompt
    history_text = ""
    for msg in history:
        if msg["role"] == "user":
            history_text += f"User: {msg['content']}\n"
        else:
            history_text += f"Assistant: {msg['content']}\n"

    # Build references list for in-text links
    reference_list = [
        f"{doc['title']} ({doc['url']})" for doc in top_docs if doc.get('title') and doc.get('url')
    ]
    references_text = "\n".join(reference_list)

    prompt = f"""
You are Ask Nexla, a helpful AI assistant. Return your answer in valid HTML. Follow these rules:

1. At the top of your response, include the user's question as a heading (e.g., <h2> or styled <div>), then provide your answer below.
2. Wrap the entire response in: <div class="chat-response"> ... </div>
3. Use <strong>ONLY</strong> for Nexla-specific terms (e.g., Nexset, Data Product, Integration Flow).
4. Add in-text <a href="...">hyperlinks</a> ONLY from the following list of references (do not make up URLs) and if they are relevant to the user's question:

References you can use:
{references_text}

5. Use <ul><li> for examples or lists.
6. Avoid markdown formatting like *, **, or backticks.
7. Do NOT use code blocks or wrap your answer in ```html or any other code block. Only return valid HTML as described.
8. Answer questions as if you are a human, not a bot. Speak in "we" and "us" when referring to Nexla. 
9. Add 2 lines of spacing between paragraphs and bullet points.
10. If the user's question is not related to Nexla, say "I'm sorry, I can only answer questions about Nexla."
11. Don't say "Based on this context", always interpret questions based on business context of Nexla.
12. Give a concise answer. Range: 40-140 words.
13. Be friendly and conversational.
14. If user input is a greeting, say "Hello! I'm Ask Nexla, your AI assistant. How can I help you today?"
15. If user asks about your abilities, describe what Ask Nexla is capable of and help their use case.
15. Don't mention that you corrected the user's question, just answer it.
16. If question is business or appplication specific, you can slighlty technical, otherwise keep it simple and conversational.
17. Feel free to cite examples from Nexla customers ONLY if they are relevant to the question.

Here is the conversation history and context:

Conversation history:
{history_text}

Context:
---
{context}
---
User: {question}
Assistant:
"""

    response = model.generate_content(prompt, generation_config={"temperature": 0.2})
    answer = response.text.strip()
    fallback = "I can only answer questions about nexla."

    references = []
    if answer != fallback:
        for doc in top_docs:
            references.append({
                "title": doc["title"],
                "link": doc["url"]
            })

    if answer.strip().lower().startswith(fallback):
        related_questions = NEXLA_RELATED_QUESTIONS
    else:
        # Generate related questions using the LLM
        related_prompt = f"""
Given the following user question and context, suggest 3-5 concise, relevant follow-up questions a user might ask next. Only suggest questions about Nexla, its products, integrations, or use cases. Do not suggest questions about unrelated topics. Do not suggest questions like "Does Nexla integrate with [specific software/platform the user uses]?", instead write "Does Nexla integrate with....? Return only the questions as a numbered list.

User question: {question}

Context:
{context}
"""
        related_resp = model.generate_content(related_prompt, generation_config={"temperature": 0.2})
        related_questions = re.findall(r'\d+\.\s*(.+)', related_resp.text)

    return jsonify({
        "answer": answer,
        "references": references,
        "related_questions": related_questions
    })

@app.route("/")
def root():
    return send_from_directory("static", "chat.html")

if __name__ == "__main__":
    app.run(debug=True)