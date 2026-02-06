# step2_llm_call_loop.py

import json
from openai import OpenAI

with open('secrets.json') as jfile:
    json_data = json.load(jfile)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # e.g., Ollama
    api_key=json_data['ORa_11NOV2025']  # Some local APIs don't need keys
)

def sync_chat_completion(usr_query):
    response = client.chat.completions.create(
        model='deepseek/deepseek-r1-0528:free',
        # model='tngtech/deepseek-r1t-chimera:free',
        messages=[
            {
                'role': 'system',
                'content': 'You are a helpful general assistant, always ready to answer questions'
            },
            {
                'role': 'user',
                'content': usr_query
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content
    
while True:
    query = input("Enter your query: ")
    if query == 'quit': break
    res_output = sync_chat_completion(query)
    print( res_output )

print('Loop quit, ending')

# Tell me something interesting about Dubai.