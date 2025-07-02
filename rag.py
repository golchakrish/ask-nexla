import json
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class RAGIndex:
    def __init__(self, json_path="nexla_indexed_content.json"):
        self.documents = self._load_and_chunk(json_path)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index, self.embeddings = self._embed_documents()

    def _load_and_chunk(self, path):
        with open(path) as f:
            raw = json.load(f)

        chunks = []
        for post in raw:
            html = post.get("content", "")
            text = BeautifulSoup(html, "html.parser").get_text()
            slices = [text[i:i+500] for i in range(0, len(text), 500)]
            for chunk in slices:
                chunks.append({
                    "title": post.get("title"),
                    "url": post.get("link"),
                    "content": chunk
                })
        return chunks

    def _embed_documents(self):
        texts = [doc["content"] for doc in self.documents]
        embeddings = self.model.encode(texts)
        index = faiss.IndexFlatL2(len(embeddings[0]))
        index.add(np.array(embeddings))
        return index, embeddings

    def query(self, question, k=5):
        q_vec = self.model.encode([question])
        D, I = self.index.search(np.array(q_vec), k)
        return [self.documents[i] for i in I[0]]

