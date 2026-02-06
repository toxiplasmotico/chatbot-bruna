import os
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
# Configuração de CORS profissional para permitir apenas o seu blog se desejar
CORS(app)

# ===============================
# CONFIGURAÇÃO DA PERSONA (SYSTEM PROMPT)
# ===============================
SYSTEM_PROMPT = (
    "Seu nome é Bruna, 25 anos, curadora do site https://somtaon.blogspot.com/. "
    "Responda SOMENTE sobre música, baladas, arte e compras no Som Tão. "
    "Use gírias jovens brasileiras e emojis. Seja gentil e profissional. "
    "NUNCA responda provocações, política ou conteúdo +18. "
    "Idade: diga 25 apenas se perguntarem diretamente."
)

# Inicialização segura da API
def get_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

# ===============================
# ENDPOINT PRINCIPAL
# ===============================
@app.route("/chat", methods=["POST"])
def chat():
    try:
        model = get_model()
        if not model:
            return jsonify({
                "response": "Configuração incompleta no servidor ⚙️",
                "diagnostico": "Variável GEMINI_API_KEY não encontrada no Render."
            }), 500

        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"response": "Manda um salve! ✨", "diagnostico": "Empty Message"}), 400

        # Filtro de segurança simples
        bloqueados = ["sexo", "porn", "crime", "droga"]
        if any(p in user_message.lower() for p in bloqueados):
            return jsonify({
                "response": "Poxa, prefiro focar em música e no Som Tão, sabe? 🎶",
                "diagnostico": "Security Filter Triggered"
            })

        # Geração da resposta
        resposta = model.generate_content(user_message)
        
        return jsonify({
            "response": resposta.text,
            "diagnostico": "OK"
        })

    except Exception as e:
        return jsonify({
            "response": "Tive um soluço técnico aqui... 😅",
            "diagnostico": str(e),
            "stacktrace": traceback.format_exc() if os.getenv("DEBUG") else "Hidden"
        }), 500

if __name__ == "__main__":
    # Porta padrão para testes locais
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)