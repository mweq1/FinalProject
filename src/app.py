import os
import gradio as gr
from processor import process_file
from brain import build_vector_store, get_rag_chain

current_chain = None

# Custom CSS for a professional "Universal AI" feel
custom_css = """
/* User Message: Very Light Blue with White Text */
.message-wrap .message.user { 
    background-color: #ADD8E6 !important; /* Light Blue */
    color: white !important; 
    border-radius: 15px 15px 0px 15px !important;
}

/* Bot Message: Very Light Blue with White Text */
.message-wrap .message.bot { 
    background-color: #B0E0E6 !important; /* Powder Blue */
    color: white !important; 
    border-radius: 15px 15px 15px 0px !important;
}

/* UNIVERSAL WHITE TEXT: Targets all text elements inside bubbles */
.message.user p, .message.user span, .message.user li, 
.message.bot p, .message.bot span, .message.bot li,
.message.bot code, .message.bot strong {
    color: white !important;
}

/* Sidebar and Status Styling */
#status_box { 
    font-weight: bold; 
    border: 1px solid #ADD8E6;
}
"""

def handle_upload(file):
    global current_chain
    if file is None: return "Waiting for document..."
    
    clean_filename = os.path.basename(file.name)
    current_chain = None # Reset
    
    chunks = process_file(file.name)
    if not chunks: return "❌ Processing Error"
    
    vectorstore = build_vector_store(chunks)
    current_chain = get_rag_chain(vectorstore)
    
    return f"🟢 '{clean_filename}' Ready!"

def chat_response(message, history):
    if current_chain is None:
        return "Please upload a document on the left sidebar first."
    try:
        response = current_chain.invoke({"input": message})
        answer = response["answer"]
        
        # Check if 'context' exists and has documents
        sources = response.get("context", [])
        
        if sources:
            # Extract filenames and remove duplicates
            filenames = {os.path.basename(doc.metadata.get("source", "Unknown")) for doc in sources}
            citation_line = f"\n\n**Source:** {', '.join(filenames)}"
            return answer + citation_line
        
        return answer
    except Exception as e:
        return f"AI Error: {str(e)}"

# Building the Enhanced Interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="green", neutral_hue="slate"), css=custom_css) as demo:
    with gr.Row():
        # Sidebar for Uploads
        with gr.Column(scale=1, variant="panel"):
            gr.Markdown("## 📁 Data Source")
            file_input = gr.File(label="Upload PDF, DOCX, or TXT", file_types=[".pdf", ".docx", ".txt"])
            status_box = gr.Textbox(
                value="No document loaded.", 
                label="System Status", 
                elem_id="status_box",
                interactive=False
            )
            gr.Markdown("---")
            gr.Markdown("### 🛠️ AI Controls")
            gr.Markdown("- **Model**: Llama 3.2\n- **Engine**: FAISS + LangChain\n- **Privacy**: 100% Local")

        # Main Chat Area
        with gr.Column(scale=3):
            gr.Markdown("# ⚡ Universal Intelligence")
            gr.Markdown("Analyze documents instantly with local AI.")
            
            chatbot = gr.ChatInterface(
                fn=chat_response,
                examples=["Summarize this document", "What are the key points?"],
                # Removes the redundant 'type' error from previous versions
            )

    # Handlers
    file_input.change(handle_upload, inputs=file_input, outputs=status_box)

if __name__ == "__main__":
    demo.launch(share=False, debug=True)