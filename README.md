# Ask Nexla

Ask Nexla is an AI-powered assistant that lets you query Nexla's website content using natural language and receive intelligent, context-aware answers. It uses semantic search (Sentence Transformers + FAISS) over all WordPress content (posts, pages, resources, landing pages).

## Features
- Crawls and indexes all Nexla WordPress content
- Strips HTML and chunks content for semantic search
- Embeds text using Sentence Transformers
- Fast similarity search with FAISS
- Flask web app with chat UI

## Setup
1. **Clone the repo:**
   ```bash
   git clone https://github.com/golchakrish/ask-nexla.git
   cd ask-nexla
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the root directory:
     ```env
     GEMINI_API_KEY=your_google_gemini_api_key_here
     ```
   - The app uses `python-dotenv` to load this key for Google Generative AI.

4. **Index website content:**
   ```bash
   python indexing_script.py
   ```
   This will create/update `nexla_indexed_content.json`.

5. **Run the app:**
   ```bash
   python app.py
   ```
   Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Repository
- GitHub: https://github.com/golchakrish/ask-nexla

## Security
- **No API keys or secrets are committed to the repo.**
- Ensure your `.env` file is in `.gitignore` (add it if not present).

## License
MIT
