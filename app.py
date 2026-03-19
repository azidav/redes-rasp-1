from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
import json
from datetime import datetime
import os
import logging

logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*")

ARQUIVO_TAREFAS = "tarefas.json"

# Criar ficheiro se não existir
if not os.path.exists(ARQUIVO_TAREFAS):
    with open(ARQUIVO_TAREFAS, "w") as f:
        json.dump([], f)

def carregar_tarefas():
    with open(ARQUIVO_TAREFAS, "r") as f:
        return json.load(f)

def guardar_tarefas(tarefas):
    with open(ARQUIVO_TAREFAS, "w") as f:
        json.dump(tarefas, f, indent=4)


# 🏠 Página principal
@app.route("/")
def home():
    return render_template("index.html")

# ➕ POST - adicionar tarefa
@app.route("/api/tarefas", methods=["POST"])
def adicionar_tarefa():
    dados = request.json
    tarefas = carregar_tarefas()

    nova_tarefa = {
        "id": len(tarefas) + 1,
        "texto": dados.get("texto"),
        "concluida": False,
        "criado_em": datetime.now().isoformat()
    }

    tarefas.append(nova_tarefa)
    guardar_tarefas(tarefas)

    logging.info(f"Tarefa criada: {nova_tarefa['texto']}")

    return jsonify(nova_tarefa), 201

# 📄 GET - listar tarefas
@app.route("/api/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(carregar_tarefas())

# ✅ Concluir tarefa
@app.route("/api/tarefas/<int:id>/concluir", methods=["PUT"])
def concluir_tarefa(id):
    tarefas = carregar_tarefas()

    for t in tarefas:
        if t["id"] == id:
            t["concluida"] = True
            logging.info(f"Tarefa concluída: {t['texto']}")
            break

    guardar_tarefas(tarefas)
    return jsonify({"status": "ok"})

# ❌ Apagar tarefa (extra opcional)
@app.route("/api/tarefas/<int:id>", methods=["DELETE"])
def apagar_tarefa(id):
    tarefas = carregar_tarefas()
    tarefas = [t for t in tarefas if t["id"] != id]

    guardar_tarefas(tarefas)
    logging.info(f"Tarefa apagada ID: {id}")

    return jsonify({"status": "apagada"})

@app.after_request
def add_headers(response):
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)