import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

SYSTEM_PROMPT = (
    "Seu nome é Bruna, curadora do site Som Tão. "
    "Responda sobre música e arte com gírias e emojis. "
    "Seja breve e simpática."
)

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada no ambiente.")

    genai.configure(api_key=api_key)

    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

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

        model = get_model()
        response = model.generate_content(user_message)

        return jsonify({"response": response.text})

    except Exception as e:
        print("ERRO:", str(e))  # aparece no log do Render
        return jsonify({
            "response": "Erro interno no servidor 😵‍💫. O admin já foi avisado!"
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
