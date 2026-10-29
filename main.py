from agent import Agent
from config import MODEL

agent = Agent()

print(f"==== AI Tools Assistant - {MODEL} ====")
print("Try: 'What time is it?', 'What is 15% of 2400?', 'Save a note: buy milk'")
print("Commands: /clear, /quit")

while True:
    text = input("You: ").strip()
    if not text:
        continue
    if text == "/quit":
        print("Goodbye!")
        break
    if text == "/clear":
        agent.clear()
        print("Conversation cleared.")
        continue
    if text.startswith("/"):
        print("Unknown command.")
        continue

    reply = agent.run(text)
    print(f"Bot: {reply}")