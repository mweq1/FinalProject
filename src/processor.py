import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    try:
        if ext == ".pdf":
            # Using fast_parser if available, but PyPDFLoader is generally okay.
            loader = PyPDFLoader(file_path)
        elif ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(file_path)
        elif ext == ".txt":
            loader = TextLoader(file_path)
        else:
            return None
        
        docs = loader.load()
        
        # INCREASED chunk size = FEWER chunks = FASTER vectorization
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, 
            chunk_overlap=100,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_documents(docs)
    except Exception as e:
        print(f"Error: {e}")
        return None