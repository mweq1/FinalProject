from brain import build_vector_store, get_rag_chain
from processor import process_file

def get_accuracy_score(query, expected, actual):
    # Quick similarity check or you can use your LLM to grade this
    return 1 if expected.lower() in actual.lower() else 0

def run_answer_test(file_path, test_data):
    chunks = process_file(file_path)
    vectorstore = build_vector_store(chunks)
    rag_chain = get_rag_chain(vectorstore)
    
    results = []
    for item in test_data:
        response = rag_chain.invoke({"input": item["q"]})
        actual = response["answer"]
        
        results.append({
            "question": item["q"],
            "expected": item["expected"],
            "actual": actual
        })
    return results

if __name__ == "__main__":
    my_tests = [{"q": "Who is the CEO?", "expected": "John Doe"}]
    # Logic to run and print results