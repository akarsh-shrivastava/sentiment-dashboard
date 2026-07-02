import os
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

def get_sentiment(review):
    prompt = prompt_temp.replace("<user-review/>", review)

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
    res_dict = json.loads(res)

    return res_dict