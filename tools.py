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

NOTES_FILE = "notes.json"
def _load_notes() -> list[str]:
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    
def save_notes(text: str) -> str:
    notes = _load_notes()
    notes.append(text)
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)
        
    return f"Note saved. Total notes: {len(notes)}"

def list_notes() -> str:
    notes = _load_notes()
    if not notes:
        return "No notes found."
    return "\n".join(f"{i+1}. {note}" for i, note in enumerate(notes, start=1))

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
    },
    {
        "type": "function",
        "function": {
            "name": "save_notes",
            "description": "Save a note to the notes file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": { "type": "string", "description": "The note text to save" }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_notes",
            "description": "List all saved notes.",
            "parameters": {"type": "object", "properties": {}}
        }
    }
]


FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "save_notes": save_notes,
    "list_notes": list_notes
}

def run_tool(name: str, arguments: str) -> str:
    if name not in FUNCTIONS:
        return f"Error: unknown tool '{name}'"
    try:
        args = json.loads(arguments or "{}")
        return FUNCTIONS[name](**args)
    except (json.JSONDecodeError, TypeError) as e:
        return f"Error: bad arguments for {name}: {e}"
        