# step3_agent_simple.py

import json
from datetime import datetime
import re
from openai import OpenAI

with open('secrets.json') as jfile:
    json_data = json.load(jfile)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # e.g., Ollama
    api_key=json_data['ORa_11NOV2025']  # Some local APIs don't need keys
)


# Tool functions

def calculate(expression):
    print(f"* I * Tool * calculate * {expression}")
    return eval(expression)

def get_weather(req_city):
    print(f"* I * Tool * get_weather * {req_city}")
    weather_db = [
        {
            'city': 'Warsaw',
            'weather': 'fair'
        },
        {
            'city': 'Moscow',
            'weather': 'cold'
        },
        {
            'city': 'London',
            'weather': 'shitty'
        },
        {
            'city': 'Milan',
            'weather': 'mild'
        }
    ]
    for location in weather_db:
        # print( f'* D * {req_city}, {location['city']}, {location['weather']}')
        if location['city'].upper() in req_city.upper():
            return location['weather']
    return f'Weather not available for {req_city}'

def get_date():
    print(f"* I * Tool * get_date")
    return datetime.now().strftime('%Y-%m-%d')

def get_time():
    print(f"* I * Tool * get_time")
    return datetime.now().strftime('%H:%M:%S')

def tool_switch_call(tool_name, query):
    match tool_name:
        case 'calculator':
            return calculate(query)
        case 'get_weather':
            return get_weather(query)
        case 'get_date':
            return get_date()
        case 'get_time':
            return get_time()
        case _:
            return f'* E * tool_switch_call * unknown tool {tool_name}, query {query}'

def sync_chat_completion(system_prompt, usr_query):
    response = client.chat.completions.create(
        # model='deepseek/deepseek-r1-0528:free',
        model='tngtech/deepseek-r1t-chimera:free',
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': usr_query
            }
        ],
        max_tokens=1024
    )
    return response.choices[0].message.content
    
def query_handling(query):
    # Define system prompt
    sys_prompt = ("You're a helpful personal assistant. Based on the user's message, "
        "decide if you need to use a tool or respond directly.\n\n"
        "If you need a tool, respond ONLY with a JSON object:\n"
        "{ \"tool\": \"calculator\", \"input\": \"5 * (4 + 3)\" }\n"
        "or\n"
        "{ \"tool\": \"get_weather\", \"input\": \"New York\" }\n"
        "or\n"
        "{ \"tool\": \"get_date\", \"input\": \"\" }\n"
        "or\n"
        "{ \"tool\": \"get_time\", \"input\": \"\" }\n\n"
        "If no tool is needed, respond naturally with a helpful message (NOT JSON)."
    )
    # Call LLM with the query
    llm_response = sync_chat_completion(sys_prompt, query)
    
    # Check if the response is a JSON or else
    response_tool = None
    response_query = None
    try:
        json_response = json.loads(llm_response)
    except:
        try:
            json_response = json.loads(re.search(r'\{[^}]+\}', llm_response).group())
        except:
    # If not JSON -> return the response
            print(f"* I * query_handling * no JSON returned")
            return llm_response

    # If JSON -> extract tool and query and pass to tool_switch_call, return the response
    response_tool = json_response.get('tool')
    response_query = json_response.get('input')
    print(f"* I * query_handling * JSON * hand over with {response_tool}, {response_query}")
    return tool_switch_call(response_tool, response_query)
        
    
# llm_response = "{ \"tool\": \"calculator\", \"input\": \"5 * (4 + 3)\" }\n"
# print(llm_response)
# json_response = json.loads(llm_response)
# print(json_response)
# test_response = 'There are some very interesting. { \"tul\": \"calculator\", \"input\": \"5 * (4 + 3)\" }\nLorem ipsum who knows what else.'
# parsed_test_response = re.search(r'\{[^}]+\}', test_response)
# print( parsed_test_response.group() )
# json_response = json.loads(parsed_test_response.group())
# print(json_response)
# print(json_response.get('tool'))

while True:
    query = input("Enter your query: ")
    if query == 'quit': break
    res_output = query_handling(query)
    print( res_output )

print('Loop quit, ending')

