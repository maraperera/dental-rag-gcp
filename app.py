from pathlib import Path
from dotenv import load_dotenv

# Load .env before any local imports run
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

import sys
from rag.pipeline import run_dental_rag

def main():
    print("=" * 60)
    print("Dental Clinic RAG Assistant (BigQuery + Gemini)")
    print("Type 'exit' to quit.")
    print("=" * 60)

    while True:
        query = input("\nEnter query: ")
        if query.strip().lower() in ["exit", "quit", "q"]:
            break

        print("\nProcessing query...")
        try:
            result = run_dental_rag(query)
            print("\n[Generated SQL]")
            print(result["metadata"]["sql"])
            print("\n[AI Response]")
            print(result["answer"])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()