import os
import shutil
import time
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# FAISS is much faster for local re-indexing than Chroma
DB_PATH = "./faiss_index"

def build_vector_store(chunks):
    # Faster Embeddings initialization
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'} # Force CPU to avoid GPU initialization lag
    )
    
    # FAISS builds in-memory instantly
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore

def get_rag_chain(vectorstore):
    llm = ChatOllama(model="llama3.2", temperature=0) # Low temp for faster, direct answers
    
    system_prompt = (
        "Use the following context to answer the question. Be brief and direct."
        "\n\nContext: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3}) # k=3 is faster than k=5
    return create_retrieval_chain(retriever, combine_docs_chain)