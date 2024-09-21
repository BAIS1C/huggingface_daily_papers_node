import os
import json
import requests
from datetime import datetime

class HuggingFaceDailyPapersNode:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "max_papers": ("INT", {"default": 5, "min": 1, "max": 50, "step": 1}),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("titles", "abstracts", "urls", "published_dates")
    FUNCTION = "fetch_papers"
    CATEGORY = "API"

    def fetch_papers(self, max_papers):
        url = "https://huggingface.co/api/daily_papers"
        try:
            response = requests.get(url)
            response.raise_for_status()
            papers = response.json()[:max_papers]
            
            titles = [paper["title"] for paper in papers]
            abstracts = [paper["abstract"] for paper in papers]
            urls = [paper["url"] for paper in papers]
            published_dates = [datetime.fromtimestamp(paper["publishedAt"]).strftime('%Y-%m-%d') for paper in papers]
            
            return (json.dumps(titles), json.dumps(abstracts), json.dumps(urls), json.dumps(published_dates))
        except requests.RequestException as e:
            error_msg = f"Error fetching data: {str(e)}"
            return (json.dumps([error_msg]), json.dumps([error_msg]), json.dumps([error_msg]), json.dumps([error_msg]))

# This dictionary is used to specify which custom nodes are available in your extension
NODE_CLASS_MAPPINGS = {
    "HuggingFaceDailyPapersNode": HuggingFaceDailyPapersNode
}

# This dictionary is used to give user-friendly names to your custom nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "HuggingFaceDailyPapersNode": "Hugging Face Daily Papers"
}