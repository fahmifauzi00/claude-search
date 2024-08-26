import json
from langchain.tools import StructuredTool
from typing import Dict
from pydantic import BaseModel, Field
from serpapi import GoogleSearch

# Import the necessary environment variables
import os
from dotenv import load_dotenv

load_dotenv()

serp_api_key = os.getenv("SERP_API_KEY")
if not serp_api_key:
    raise ValueError("SERP_API_KEY not found in environment variables")

def execute_search(query: str) -> Dict:
    try:
        params = {
            "engine": "google",
            "q": query,
            "api_key": serp_api_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "answer_box" in results:
            answer = results["answer_box"].get("snippet") or results["answer_box"].get("answer")
            if answer:
                return {"type": "answer", "content": answer}
        
        if "organic_results" in results:
            processed_results = []
            for result in results["organic_results"][:3]:
                processed_results.append({
                    "title": result.get('title', 'N/A'),
                    "url": result.get('link', 'N/A'),
                    "snippet": result.get('snippet', 'N/A')
                })
            return {"type": "search_results", "content": processed_results}
        
        return {"type": "error", "content": "No relevant results found."}
    except Exception as e:
        return {"type": "error", "content": f"Error performing search: {str(e)}"}

class SearchInput(BaseModel):
    query: str = Field(..., description="The search query")

search_tool = StructuredTool.from_function(
    func=execute_search,
    name="search_internet",
    description="Search the internet for current information. Use this for queries about weather, news, or any time-sensitive information.",
    args_schema=SearchInput
)
