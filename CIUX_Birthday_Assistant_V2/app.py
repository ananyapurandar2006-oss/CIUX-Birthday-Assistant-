
from flask import Flask, jsonify, render_template, request
from data_service import load_people
from nlu import parse
from service import execute

app = Flask(__name__)

PEOPLE = load_people()


@app.get("/")
def index():
    return render_template(
        "index.html",
        record_count=len(PEOPLE)
    )


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = payload.get("message", "")

    parsed = parse(message, PEOPLE)
    answer = execute(parsed, PEOPLE)

    return jsonify({
        "answer": answer,
        "debug": parsed
    })


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        records=len(PEOPLE),
        version="V2"
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
