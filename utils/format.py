import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Configure the genai library with your API key
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def generate_summary_from_html(html_content: str, url: str) -> dict:
    system_prompt = """You are a summarization assistant, who summarize the content given to you from a webscrapper, which gives you a html format data and you will summarize the information in it to store the summary as vector in vectordatabase"""
    model = genai.GenerativeModel( model_name='gemini-2.5-flash-lite',
        system_instruction = system_prompt)

    # Generate content
    summary_response = model.generate_content(
        html_content,
    )

    # Example metadata and summary
    summary_data ={
            "url": url,
            "timestamp": datetime.now().isoformat(),
        "original_text_length": len(html_content),
        "summary": summary_response.text,
        "source": "USCIS website",
        }
    
    return summary_data

