import openai
import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

# Set your OpenAI API key
openai.api_key = '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'

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def generate_summary(text_content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Résumez le texte suivant:\n{text_content}"}
        ]
    )

    if response.choices:
        summary = response.choices[0].message["content"]
        return summary
    else:
        return None
