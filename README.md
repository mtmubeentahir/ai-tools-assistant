# AI Tools Assistant 🛠️🤖

A command-line **AI agent** built with Python and the **Google Gemini API**. Instead of only generating text, the AI can call real Python functions (tools) to tell the time, do exact math and save notes. It can also chain several tool calls together to answer multi-step questions.

This is part of my learning journey. See also:
- [PythonLearning](https://github.com/mtmubeentahir/PythonLearning): Python fundamentals
- [ai-chatbot-cli](https://github.com/mtmubeentahir/ai-chatbot-cli): my first AI chatbot with memory

## ✨ Features

- **Tool calling**: the AI decides when to use a tool and fills in the arguments itself
- **Agent loop**: the AI can call a tool, look at the result, and call another one, until the task is done
- **Multi-step reasoning**: e.g. "How many hours until midnight?" uses the clock, then the calculator
- **Conversation memory**: follow-up questions like "Now divide that by 5" work
- **Persistent notes**: saved to a file, so they survive a restart
- **Safety limits**: a maximum number of steps per question, and tool errors never crash the app

## 💬 Example

```
You: How many hours are left until midnight?
  [tool] get_current_time({})
  [result] 02:18 AM, Friday 30 October 2026
  [tool] calculate({"a":24,"operation":"subtract","b":2.3})
  [result] 21.7
Bot: There are 21.7 hours left until midnight (or 21 hours and 42 minutes).

You: What is 25 times 4?
  [tool] calculate({"b":4,"a":25,"operation":"multiply"})
  [result] 100
Bot: 25 times 4 is 100.
You: Now divide that by 5
  [tool] calculate({"a":100,"b":5,"operation":"divide"})
  [result] 20.0
Bot: That divided by 5 is 20.
```

The `[tool]` and `[result]` lines show every decision the agent makes.

## 🧰 Available tools

| Tool | What it does |
|---|---|
| `get_current_time` | returns the current local date and time |
| `calculate` | exact arithmetic on two numbers (add, subtract, multiply, divide) |
| `save_notes` | saves a note to `notes.json` |
| `list_notes` | lists all saved notes |

## ⌨️ Commands

| Command | What it does |
|---|---|
| `/clear` | start a fresh conversation |
| `/quit` | exit |

## 🚀 Setup

**Requirements:** Python 3.10 or newer, and a free Gemini API key (no credit card needed).

1. **Clone the repository**
   ```bash
   git clone https://github.com/mtmubeentahir/ai-tools-assistant.git
   cd ai-tools-assistant
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

3. **Install the packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**
   - Get a free key at [Google AI Studio](https://aistudio.google.com).
   - Copy the example settings file:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and paste your key:
     ```
     GEMINAI_API_KEY=your-gemini-key-here
     BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
     MODEL=gemini-3.5-flash-lite
     ```

5. **Run the assistant**
   ```bash
   python main.py
   ```
   Or try the simpler one-question version from Part 1:
   ```bash
   python tool_demo.py
   ```

> ⚠️ Never share your `.env` file or commit it to GitHub. It is listed in `.gitignore`.

## 📁 Project structure

```
ai-tools-assistant/
├── main.py         # chat interface and commands
├── agent.py        # Agent class: conversation history and the agent loop
├── tools.py        # tool functions, their descriptions, and run_tool()
├── tool_demo.py    # minimal single-question tool calling demo
├── config.py       # loads settings from .env
├── .env.example    # settings template (copy to .env)
└── requirements.txt
```

## ⚙️ How it works

Each tool has three parts in `tools.py`:
1. **A Python function** that does the real work
2. **A description** (JSON Schema) that tells the AI what the tool does and which arguments it needs
3. **An entry in a dictionary** that connects the tool's name to the function

The agent loop in `agent.py`:

```
send the conversation + tool descriptions to the AI
        │
does the reply ask for tools?
   ├── yes → run each tool, add the results to the conversation, ask the AI again
   └── no  → that's the final answer
```

**The AI never runs code itself.** It only *requests* a tool by name with JSON arguments. My code decides whether to run it, and only functions listed in the tools dictionary can be called. The loop stops after 5 steps to prevent endless tool calls.

## 👤 Author

**Mubeen Tahir** · [GitHub](https://github.com/mtmubeentahir)