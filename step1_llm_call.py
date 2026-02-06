# step1_llm_call.py

import json

from openai import OpenAI

with open('secrets.json') as jfile:
    json_data = json.load(jfile)

# print( f"Secret API key {json_data['ORa_11NOV2025']}" )


# help(OpenAI)

# import inspect

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # e.g., Ollama
    api_key=json_data['ORa_11NOV2025']  # Some local APIs don't need keys
)

# print( inspect.signature(client.chat.completions.create) )


# Available models change frequently on OpenRouter. Examine the list of models available:
# https://openrouter.ai/docs/guides/overview/models
# https://openrouter.ai/models
def sync_chat_completion(usr_query):
    response = client.chat.completions.create(
        # model='tngtech/deepseek-r1t2-chimera:free',
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
    
query = input("Enter your query: ")
res_output = sync_chat_completion(query)
print( res_output )

# Tell me something interesting about Dubai.