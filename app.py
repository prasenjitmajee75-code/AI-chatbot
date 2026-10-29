
from flask import Flask, request, jsonify, send_from_directory
import requests

app = Flask(__name__)

# Ollama Local AI configuration
MODEL = "qwen3:1.7b"
OLLAMA_URL = "http://localhost:11434/api/chat"


# Load HTML page
@app.route("/")
def home():
    return send_from_directory(app.root_path, "INDEX.html")


# Load CSS
@app.route("/stylesheet.css")
def stylesheet():
    return send_from_directory(app.root_path, "stylesheet.css")


# Load JavaScript
@app.route("/script.js")
def javascript():
    return send_from_directory(app.root_path, "script.js")


# Handle chatbot messages
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "error": "Please enter a message."
            }), 400

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful AI assistant. "
                            "Answer clearly and concisely."
                        )
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "stream": False,
                "think": False
            },
            timeout=300
        )

        response.raise_for_status()

        result = response.json()
        reply = result.get("message", {}).get("content", "").strip()

        if not reply:
            reply = "Sorry, I could not generate a response."

        return jsonify({"reply": reply})

    except requests.exceptions.ConnectionError:
        return jsonify({
            "error": "Ollama is not running. Please start Ollama."
        }), 503

    except requests.exceptions.Timeout:
        return jsonify({
            "error": "The AI took too long to respond. Please try again."
        }), 504

    except Exception:
        app.logger.exception("Chatbot API error")
        return jsonify({
            "error": "Something went wrong. Check the VS Code terminal."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
