import sys
import json
import os
from datetime import datetime
from groq import Groq

MEMORY_FILE = "memory/knowledge.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                pass
    return {"history": []}

def save_memory(data):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    user_prompt = sys.argv[1] if len(sys.argv) > 1 else "Olá!"
    api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        print("Erro: A variável GROQ_API_KEY não foi encontrada.")
        sys.exit(1)

    client = Groq(api_key=api_key)
    memory = load_memory()

    print(f"\nVocê: {user_prompt}")
    
    # Busca a lista de modelos ativos disponíveis na API
    models_list = client.models.list()
    available_models = [m.id for m in models_list.data if "whisper" not in m.id and "guard" not in m.id]
    
    if not available_models:
        print("Erro: Nenhum modelo de texto foi encontrado na sua conta do Groq.")
        sys.exit(1)
        
    print(f"Modelos de texto disponíveis encontrados: {available_models}")

    ai_reply = None
    for model_name in available_models:
        try:
            print(f"Tentando executar com o modelo: {model_name}...")
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Você é uma IA autônoma chamada iaFLEX, prestativa e inteligente."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
            ai_reply = completion.choices[0].message.content
            print(f"Sucesso! Resposta obtida do modelo: {model_name}")
            break
        except Exception as e:
            print(f"Falha no modelo {model_name}: {e}")

    if not ai_reply:
        print("Erro crítico: Não foi possível obter resposta de nenhum modelo.")
        sys.exit(1)

    print(f"\nIA: {ai_reply}\n")

    memory["history"].append({
        "timestamp": datetime.now().isoformat(),
        "user": user_prompt,
        "ia": ai_reply
    })
    save_memory(memory)
    print("===> Resposta registrada na memória com sucesso!")

if __name__ == "__main__":
    main()
