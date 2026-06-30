import os
from dotenv import load_dotenv

from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

review = "The product arrived late and the packaging was damaged, but the item itself works perfectly."

prompt = f"""Analyze the sentiment of this customer review: "{review}"
Tell me: 1) Overall sentiment (Positive/Negative/Neutral/Mixed)
2) The main reason for that sentiment"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

print(response.text)