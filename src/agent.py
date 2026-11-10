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
    
    completion = client.chat.completions.create(
        model="llama-3-70b-8192",
        messages=[
            {"role": "system", "content": "Você é uma IA autônoma chamada iaFLEX, prestativa e inteligente."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )
    
    ai_reply = completion.choices[0].message.content
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
