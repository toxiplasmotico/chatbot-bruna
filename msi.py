import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Importante!
import google.generativeai as genai

app = Flask(__name__)

# CONFIGURAÇÃO DE SEGURANÇA (Resolve o erro do Inspecionar)
CORS(app, resources={r"/*": {"origins": "*"}}) 

SYSTEM_PROMPT = (
    "Seu nome é Bruna, curadora do site Som Tão. "
    "Responda sobre música e arte com gírias e emojis. "
    "Seja breve e simpática."
)

def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

@app.route("/", methods=["GET"])
def home():
    return "Servidor da Bruna Online! ✅", 200

@app.route("/chat", methods=["POST", "OPTIONS"]) # OPTIONS é necessário para o CORS
def chat():
    if request.method == "OPTIONS":
        return "", 200
        
    try:
        model = get_model()
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()
        
        if not user_message:
            return jsonify({"response": "Manda um salve! ✨"}), 400
        
        resposta = model.generate_content(user_message)
        return jsonify({"response": resposta.text})
    except Exception as e:
        return jsonify({"response": "Tive um soluço técnico... tente de novo! 😅"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
