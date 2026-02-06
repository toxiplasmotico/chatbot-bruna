import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Permite que seu blog acesse o servidor

SYSTEM_PROMPT = (
    "Seu nome é Bruna, curadora do site Som Tão. "
    "Responda sobre música, arte e o blog. Use gírias jovens e emojis. "
    "Seja breve e gentil."
)

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

# ROTA PARA O RENDER NÃO DAR ERRO (Página Inicial)
@app.route("/", methods=["GET"])
def home():
    return "Servidor da Bruna está Online! ✅", 200

# ROTA DO CHAT
@app.route("/chat", methods=["POST"])
def chat():
    try:
        model = get_model()
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()
        if not user_message: return jsonify({"response": "Oi! Manda um salve! ✨"}), 400
        
        resposta = model.generate_content(user_message)
        return jsonify({"response": resposta.text})
    except Exception as e:
        return jsonify({"response": "Estou descansando um pouco... tente em instantes! 😅"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
