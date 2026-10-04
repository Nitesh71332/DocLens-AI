import os
from dotenv import load_dotenv
load_dotenv()

from google import genai

key=os.getenv("GEMINI_API_KEY")
model=os.getenv("GEMINI_MODEL")

print("key set:",bool(key),"| model:",repr(model))

client=genai.Client(api_key=key)

try:
    r=client.models.generate_content(
        model=model,
        contents="Reply with the word OK"
    )
    print("SUCCESS:",r.text)
except Exception as e:
    print("FAILED:",type(e).__name__,"-",e)

print("\nModels your key can use:")
try:
    for m in client.models.list():
        print("  ",m.name)
except Exception as e:
    print("could not list models:",e)