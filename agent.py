from typing import Any

import openai
from openai import OpenAI

from config import API_KEY, BASE_URL, MODEL
from tools import TOOLS, run_tool

SYSTEM_PROMPT = (
    "You are a helpful assistant with tools. "
    "Use the tools whenever they help, especially for time, math and notes. "
    "Keep answers short and clear."
)

MAX_STEPS = 5


class Agent:
    def __init__(self) -> None:
        self.client = OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=60)
        self.messages: list[dict[str, Any]] = [{"role": "system", "content": SYSTEM_PROMPT}]

    def clear(self) -> None:
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def run(self, user_text: str) -> str:
        self.messages.append({"role": "user", "content": user_text})

        for step in range(MAX_STEPS):
            try:
                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=self.messages,
                    tools=TOOLS,
                )
            except openai.RateLimitError:
                return "[Error] Rate limit reached. Wait a minute and try again."
            except openai.APIConnectionError:
                return "[Error] Could not connect. Check your internet connection."
            except openai.APIStatusError as e:
                return f"[Error] The API returned an error ({e.status_code}): {e.message}"

            message = response.choices[0].message
            self.messages.append(message.model_dump(exclude_none=True))

            if not message.tool_calls:
                return message.content or "[Error] The model returned an empty reply."

            for call in message.tool_calls:
                print(f"  [tool] {call.function.name}({call.function.arguments})")
                result = run_tool(call.function.name, call.function.arguments)
                print(f"  [result] {result}")
                self.messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

        return "[Error] Stopped: too many tool steps."
    