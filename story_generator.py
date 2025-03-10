import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

system_message = "Write one sentence in simplified chinese using only HSK 1 vocabulary"

def generate_sentence():
    stream = client.chat.completions.create(model = "gpt-4o-mini",
                                            messages=[{"role": "developer", "content": system_message }],
                                            stream = False)
    
    result = stream.choices[0].message.content
    return result

stream = client.chat.completions.create(model = "gpt-4o-mini",
                                            messages=[{"role": "developer", "content": system_message }],
                                            stream = False)


result = stream.choices[0].message.content

print(result)

