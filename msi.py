import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = (
    "Seu nome é Bruna, curadora do site Som Tão. "
    "Responda sobre música e arte com gírias e emojis. "
    "Seja breve e simpática."
)

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada no Render.")
    return genai.Client(api_key=api_key)

@app.route("/", methods=["GET"])
def home():
    return "Servidor da Bruna Online! ✅", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Manda um salve! ✨"}), 400

        client = get_client()

        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=f"{SYSTEM_PROMPT}\nUsuário: {user_message}"
        )

        return jsonify({"response": response.text})

    except Exception as e:
        print("🔥 ERRO REAL:", str(e))
        return jsonify({
            "response": "Erro interno no servidor 😵‍💫. Tente novamente."
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
