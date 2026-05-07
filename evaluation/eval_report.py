import pandas as pd
from evaluation.test_answers import run_answer_test

def generate_report(file_path):
    print("🚀 Starting Full Evaluation Report...")
    
    # Define your test suite
    test_suite = [
        {"q": "What is the document's date?", "expected": "2024"},
        # Add more...
    ]
    
    results = run_answer_test(file_path, test_suite)
    
    # Create a DataFrame for a clean look
    df = pd.DataFrame(results)
    df.to_csv("eval_report_latest.csv", index=False)
    
    print("\n📊 Report Generated: eval_report_latest.csv")
    print(df[["question", "actual"]])

if __name__ == "__main__":
    generate_report("sample_data.pdf")