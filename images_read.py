import pytesseract
from PIL import Image
import requests
import json

pytesseract.pytesseract.tesseract_cmd = r"D:\\model\\tesseract.exe"

# OCR
img = Image.open("C:\\Users\\Sabbu\\Documents\\Downloads\\Test Walkathon Group ("
                 "1)\\2025_12_25_103651_4AAB45996A0FC4DFC4AC.jpeg")
text = pytesseract.image_to_string(img)

print(f"text ============= "+text)

# LLaMA prompt
prompt = f"""
Extract health data and return ONLY JSON. Don't add any summary Just raw JSON also don't add ``` also

Text:
{text}

JSON format:
{{
  "steps": number,
  "calories_kcal": number,
  "distance_km": number,
  "active_time_minutes": number
}}
"""

# Call local LLaMA (Ollama)
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1",
        "prompt": prompt,
        "stream": False
    }
)

result = response.json()["response"]
print(f"result === {result}")
