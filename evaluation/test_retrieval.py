import sys
import os

# --- 1. THE BULLETPROOF PATH FIX ---
# Get the absolute path of the directory where this script is located (evaluation/)
current_dir = os.path.dirname(os.path.abspath(__file__)) 
# Get the absolute path of the project root (MyCapstone-main/)
project_root = os.path.dirname(current_dir)             
# Path to your source files (src/)
src_path = os.path.join(project_root, "src")

# Add both to sys.path so Python can find 'processor' and 'brain'
if src_path not in sys.path:
    sys.path.insert(0, src_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- 2. THE IMPORTS ---
try:
    from processor import process_file
    from brain import build_vector_store
    print("System modules loaded successfully.")
except ImportError as e:
    print(f"Error: Could not find core modules. {e}")
    print(f"Looked in: {src_path}")
    sys.exit(1)

# --- 3. THE EVALUATION LOGIC ---

def run_retrieval_test(file_path, test_cases):
    # Construct the full path to the file in test_files
    full_path = os.path.join(project_root, file_path)
    
    if not os.path.exists(full_path):
        print(f"File not found at: {full_path}")
        return

    print(f"\nRUNNING: Testing Lecture Material: {os.path.basename(full_path)}")
    print("-" * 60)

    # Step A: Load and Split
    chunks = process_file(full_path)
    if not chunks:
        print("Error: No chunks returned from processor.")
        return
    
    print(f"DEBUG: Document split into {len(chunks)} chunks.")

    # Step B: Build Vector Store
    vectorstore = build_vector_store(chunks)
    
    # Step C: Test Queries
    hits = 0
    for case in test_cases:
        query = case["query"]
        # Normalize text to handle extra spaces or newlines in PDFs
        expected = " ".join(case["expected"].lower().split())
        
        results = vectorstore.similarity_search(query, k=3)
        
        found = False
        for i, doc in enumerate(results):
            chunk_content = " ".join(doc.page_content.lower().split())
            if expected in chunk_content:
                print(f"PASS: Query: '{query}' -> Found in Chunk {i+1}")
                found = True
                hits += 1
                break
        
        if not found:
            print(f"FAIL: Query: '{query}' -> NOT FOUND in top 3.")
            # Print first bit of context to see what it found instead
            preview = results[0].page_content[:150].replace('\n', ' ')
            print(f"      Context found: {preview}...")

    # --- 4. THE SUMMARY ---
    total = len(test_cases)
    accuracy = (hits / total) * 100 if total > 0 else 0
    print("-" * 60)
    print(f"SUMMARY: {hits}/{total} passed ({accuracy:.1f}%)")
    print("-" * 60)

if __name__ == "__main__":
    lecture_test_cases = [
        {
            "query": "What is the title of Lecture 4?", 
            "expected": "Computer Architecture models" 
        },
        {
            "query": "what is a Three- State Bus Buffers", 
            "expected": "constructed with three state gates instead of multiplexers"
        }
    ]

    # Target the lecture file in your test_files folder
    run_retrieval_test("test_files/lecture 4.pdf", lecture_test_cases)