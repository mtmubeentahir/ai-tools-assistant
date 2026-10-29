from openai import OpenAI

from config import API_KEY, BASE_URL, MODEL
from tools import TOOLS, run_tool

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

question = input("Ask something: ")

messages = [
    {"role": "system", "content": "You are a helpful assistant. Use the tools when they help."},
    {"role": "user", "content": question},
]

# ---- Request 1: send the question AND the list of tools ----
response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
message = response.choices[0].message

if not message.tool_calls:
    print("(No tool needed)")
    print("Bot:", message.content)
else:
    # ---- The AI asked us to run tools ----
    messages.append(message.model_dump(exclude_none=True))


    for call in message.tool_calls:
        print(f"[AI wants to call] {call.function.name}({call.function.arguments})")
        result = run_tool(call.function.name, call.function.arguments)
        print(f"[Tool result] {result}")
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})


    # ---- Request 2: send everything back, including the tool results ----
    final = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
    print("Bot:", final.choices[0].message.content)
