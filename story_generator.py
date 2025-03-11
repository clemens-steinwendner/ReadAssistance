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

#story_system_prompt = "Your task is to write a short story of around three sentences in simplified chinese. Use only HSK 1 vocabulary as much as possible. Make the story interesting."

def generate_story(hsk_level):

    story_system_prompt = "Your task is to write a short story of around five sentences in simplified chinese. Use only HSK " + hsk_level+ " vocabulary as much as possible. Make the story interesting."

    print("hello, really generating")

    stream = client.chat.completions.create(model = "gpt-4o-mini",
                                            messages = [{"role": "developer", "content": story_system_prompt}],
                                            stream = False)
    
    print(stream.choices[0].message.content)
    
    return stream.choices[0].message.content
    

stream = client.chat.completions.create(model = "gpt-4o-mini",
                                            messages=[{"role": "developer", "content": system_message }],
                                            stream = False)


result = stream.choices[0].message.content

print(result)

