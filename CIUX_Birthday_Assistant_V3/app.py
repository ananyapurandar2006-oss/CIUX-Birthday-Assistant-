
from flask import Flask, jsonify, render_template, request, session

from data_service import load_people
from nlu import parse
from service import execute
from dialogue import enrich_with_context, update_state

app = Flask(__name__)
app.secret_key = "birthday-assistant-v3-dev-key"

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
    message = payload.get("message", "").strip()

    if not message:
        return jsonify({"answer": "Please enter a question."}), 400

    state = session.get("dialogue_state", {})

    parsed = parse(message, PEOPLE)
    parsed = enrich_with_context(parsed, state)

    e = parsed["entities"]

    # Detect an ambiguous relationship question.
    if (
        "relationship" in e
        and "person_id" not in e
        and "when is my" in message.lower()
    ):
        matches = PEOPLE[
            PEOPLE["Relationship"].str.lower()
            == str(e["relationship"]).lower()
        ]

        if len(matches) > 1:
            session["dialogue_state"] = update_state(
                parsed,
                state,
                list(matches["Person_ID"])
            )

            names = ", ".join(matches["Name"].head(8).tolist())

            return jsonify({
                "answer": (
                    f"I found {len(matches)} people with that relationship: "
                    f"{names}. Which one do you mean?"
                ),
                "debug": parsed
            })

    answer = execute(parsed, PEOPLE)

    session["dialogue_state"] = update_state(parsed, state)

    return jsonify({
        "answer": answer,
        "debug": parsed
    })


@app.post("/api/reset")
def reset():
    session.pop("dialogue_state", None)

    return jsonify({
        "message": "Conversation reset successfully."
    })


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        records=len(PEOPLE),
        version="V3"
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
