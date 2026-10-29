import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:1.7b"

print("=" * 40)
print("       MY AI CHATBOT")
print("=" * 40)
print("Using local AI: Qwen3 4B")
print("Type 'exit' to stop the chatbot.\n")

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    }
]

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("Bot: Goodbye!")
        break

    if not user_input:
        continue

    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "think": False
            },
            timeout=300
        )

        response.raise_for_status()
        data = response.json()

        reply = data.get("message", {}).get("content", "").strip()

        if not reply:
            reply = "Sorry, I couldn't generate a response."

        print(f"\nBot: {reply}\n")

        messages.append({
            "role": "assistant",
            "content": reply
        })

        print(f"\nBot: {reply}\n")

        messages.append({
            "role": "assistant",
            "content": reply
        })

    except requests.RequestException as error:
        print(f"\nConnection error: {error}\n")
        messages.pop()

    except (KeyError, ValueError) as error:
        print(f"\nResponse error: {error}\n")
        messages.pop()