A high-performance, privacy-first RAG system for instant document analysis.

Universal AI allows you to chat with PDF, DOCX files locally. By leveraging an in-memory FAISS vector store and Llama 3.2, this system eliminates the minutes of waiting required by traditional disk-based databases, providing a "Ready!" status in seconds.

🚀 Key Features
Sub-Minute Ingestion: Optimized chunking and in-memory indexing via FAISS.

Ice Blue UI: Modern sidebar-style interface with high-contrast font visibility.

100% Privacy: All data stays on your machine. No cloud APIs, no data leaks.

Zero-Ghosting Logic: The "Brain" is completely wiped and rebuilt for every new upload to ensure clean contexts.

🛠️ System Setup Guide
1. Hardware & Environment
OS: Windows 10/11, macOS, or Linux.

Python: Version 3.10 or higher.

Power: For laptops, ensure you are plugged into a power source to allow maximum CPU performance during vector calculations.

2. Core Dependencies (Ollama)
You must have Ollama installed to run the Llama 3.2 engine.

Download: Ollama.com

Pull the Model: Open your terminal and run:

Bash
ollama pull llama3.2
3. Project Installation
Navigate to your project folder and install the 2026-optimized requirements:

Bash
pip install -r requirements.txt
Note: This will install faiss-cpu, gradio, langchain-classic, and the necessary document loaders.

📂 Project Architecture
processor.py (Ingestion): Handles file loading and splits text into 1,500-character semantic chunks.

brain.py (RAG Engine): Manages the FAISS vector store and orchestrates the Llama 3.2 retrieval chain.

app.py (Interface): The Ice Blue Gradio UI with sidebar controls and custom CSS.

📝 How to Use
Start the App: Run python app.py in your terminal.

Upload: Drag a document into the sidebar.

Wait for Status: Look for the 🟢 Ready! signal in the system dashboard.

Chat: Ask questions. The AI will strictly use the uploaded document to answer.
