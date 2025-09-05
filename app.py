from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
memory_file = "memory.json"

# Load memory
if os.path.exists(memory_file):
    with open(memory_file, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "").strip().lower()

    # Format ajar: ajarin ngoding <topik> = <kode>
    if msg.startswith("ajarin ngoding"):
        try:
            _, rest = msg.split("ajarin ngoding", 1)
            topic, code = rest.split("=", 1)
            topic = "ngoding " + topic.strip()
            code = code.strip()
            memory[topic] = code
            with open(memory_file, "w", encoding="utf-8") as f:
                json.dump(memory, f, ensure_ascii=False, indent=2)
            return jsonify({"reply": f"Oke, aku ingat '{topic}' = '{code}'"})
        except:
            return jsonify({"reply": "Format salah. Gunakan: ajarin ngoding <topik> = <kode>"})

    if msg in memory:
        return jsonify({"reply": memory[msg]})
    
    return jsonify({"reply": "Maaf, aku belum tahu itu. Ajarin aku pakai: ajarin ngoding <topik> = <kode>"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
