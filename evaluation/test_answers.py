import sys
import os

# --- 1. PATH CONFIGURATION ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, "src")

sys.path.insert(0, src_path)
sys.path.insert(0, project_root)

try:
    from processor import process_file
    from brain import build_vector_store, get_rag_chain
    print("SUCCESS: Full RAG components loaded.")
except ImportError as e:
    print(f"ERROR: Could not load modules. {e}")
    sys.exit(1)

# --- 2. ANSWER EVALUATION LOGIC ---

def run_answer_test(file_path, test_data):
    full_path = os.path.join(project_root, file_path)
    
    if not os.path.exists(full_path):
        print(f"ERROR: File not found: {full_path}")
        return

    print(f"\nSTARTING: Full Answer Evaluation for: {os.path.basename(full_path)}")
    print("=" * 70)

    # Setup RAG
    chunks = process_file(full_path)
    vectorstore = build_vector_store(chunks)
    rag_chain = get_rag_chain(vectorstore)

    for case in test_data:
        question = case["q"]
        expected = case["expected"]

        print(f"QUESTION: {question}")
        
        # Invoke the full RAG chain
        response = rag_chain.invoke({"input": question})
        actual_answer = response["answer"]

        print(f"EXPECTED: {expected}")
        print(f"ACTUAL:   {actual_answer}")
        
        # Quick manual verification check
        # (Does the actual answer contain key parts of the expected answer?)
        check = "YES" if expected.lower()[:20] in actual_answer.lower() else "REVIEW NEEDED"
        print(f"MATCH CHECK: {check}")
        print("-" * 70)

if __name__ == "__main__":
    # Test Data for Lecture 4
    lecture_4_tests = [
        {
            "q": "What is the function of a Three-State Bus Buffer?",
            "expected": "It allows a bus system to be constructed with three-state gates instead of multiplexers."
        },
        {
            "q": "What models are discussed in Lecture 4?",
            "expected": "Computer Architecture & Organization models."
        }
    ]

    run_answer_test("test_files/lecture 4.pdf", lecture_4_tests)
