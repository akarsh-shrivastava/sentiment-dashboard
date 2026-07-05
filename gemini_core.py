import os
import time
import json
from dotenv import load_dotenv

from google import genai

reviews = [
    "The product arrived late and the packaging was damaged, but the item itself works perfectly.",
    "Absolutely love this! Fast shipping, great quality, will buy again.",
    "It stopped working after two days. Very disappointed. Never buying from this brand again."
]

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

with open("prompt.txt") as f:
    prompt_temp = f.read()

def get_sentiment(review, retries=3, delay=10):
    prompt = prompt_temp.replace("<user-review/>", review)

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            res = response.text.strip()
            if res.startswith("```"):
                res = res.split("```")[1]
                if res.startswith("json"):
                    res = res[4:]
                res = res.strip()
            return json.loads(res)

        except Exception as e:
            if attempt < retries-1:
                time.sleep(delay)
            else:
                return {
                    "sentiment": "Error",
                    "confidence": 0.0,
                    "themes": [],
                    "positive_aspects": [],
                    "negative_aspects": [],
                    "summary": f"Analysis failed: {str(e)}"
                }
        

    return res_dict