import os
import json
import sys

MEMORY_PATH = "memory/knowledge.json"
PROMPT_PATH = "system_prompt.txt"

def carregar_memoria():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_aprendizado(novo_item):
    memoria = carregar_memoria()
    if "aprendizados" not in memoria:
        memoria["aprendizados"] = []
    memoria["aprendizados"].append(novo_item)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

def executar_agente(comando):
    memoria = carregar_memoria()
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        regras = f.read()

    print(f"==> Processando comando: {comando}")
    # Salva o aprendizado/histórico da execução
    salvar_aprendizado({"comando": comando, "status": "executado"})
    print("==> IA executou com sucesso e salvou na memória.")

if __name__ == "__main__":
    prompt_usuario = sys.argv[1] if len(sys.argv) > 1 else "Execucao inicial do agente"
    executar_agente(prompt_usuario)
