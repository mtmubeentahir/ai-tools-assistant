import json
from datetime import datetime

def get_current_time() -> str:
    return datetime.now().strftime("%I:%M %p, %A %d %B %Y")

def calculate(a: float, b: float, operation: str) -> str:
    if operation == "add":
        return str(a + b)
    if operation == "subtract":
        return str(a - b)
    if operation == "multiply":
        return str(a * b)
    if operation == "divide":
        if b == 0:
            return "Error: cannot divide by zero."
        return str(a / b)
    return f"Error: unknown operation '{operation}'"


TOOLS =[
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local date and time.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Do exact arithmetic on two numbers. Use this for any math.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": { "type": "number", "description": "The first number" },
                    "b": { "type": "number", "description": "The second number" },
                    "operation": { 
                        "type": "string", 
                        "enum": ["add", "subtract", "multiply", "divide"],
                        "description": "The operation to perform" 
                    }
                },
                "required": ["a", "b", "operation"]
                
            }
        }
    }
]





FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate
}

def run_tool(name: str, arguments: str) -> str:
    if name not in FUNCTIONS:
        return f"Error: unknown tool '{name}'"
    try:
        args = json.loads(arguments or "{}")
        return FUNCTIONS[name](**args)
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error: bad arguments for {name}: {e}"
        