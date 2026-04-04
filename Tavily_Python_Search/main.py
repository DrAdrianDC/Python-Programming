# Tavily Python Search Script

import os
from dotenv import load_dotenv
from tavily import TavilyClient

# Load API key from .env file
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

# Check if API key exists
if not api_key:
    print("Error: TAVILY_API_KEY not found in .env file.")
    exit(1)

# Initialize client for Tavily
tavily = TavilyClient(api_key=api_key)

# Ask user for query
query = input("🔍 Enter your search query: ")

try:
    # Perform search
    response = tavily.search(query, include_answer=True)

    # Print AI-generated answer
    print("\n Answer:\n")
    print(response.get("answer", "No answer found"))

    # Print sources
    print("\n Sources:\n")
    for r in response.get("results", []):
        print(f"- {r.get('title')}")
        print(f"  {r.get('url')}\n")

except Exception as e:
    print(f"Error during search: {e}")