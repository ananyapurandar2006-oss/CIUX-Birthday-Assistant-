
import os

from flask import Flask, jsonify, render_template, request, session

from data_service import load_people
from nlu import parse
from llm_nlu import parse_with_llm
from service import execute
from dialogue import enrich_with_context, update_state

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv(
    "FLASK_SECRET",
    "birthday-assistant-v4-dev-key"
)

PEOPLE = load_people()

# Keep False to avoid paid API calls.
# Change to True only when API access and credits are available.
USE_LLM = os.getenv("USE_LLM", "false").lower() == "true"


def prepare_entities(parsed):
    """
    Validate LLM-extracted entities against the dataset.
    The spreadsheet remains the source of factual information.
    """

    entities = parsed.get("entities", {})

    # Ground person names against the dataset.
    if entities.get("person_name"):
        wanted = str(entities["person_name"]).strip().lower()

        matches = PEOPLE[
            PEOPLE["Name"].astype(str).str.strip().str.lower()
            == wanted
        ]

        if matches.empty and "Nickname" in PEOPLE.columns:
            matches = PEOPLE[
                PEOPLE["Nickname"].astype(str).str.strip().str.lower()
                == wanted
            ]

        if len(matches) == 1:
            person = matches.iloc[0]
            entities["person_id"] = person["Person_ID"]
            entities["person_name"] = person["Name"]

    # Convert month names into month numbers.
    import calendar

    if isinstance(entities.get("month"), str):
        month_name = entities["month"].strip().lower()

        for number in range(1, 13):
            if calendar.month_name[number].lower() == month_name:
                entities["month"] = number
                break

    # Validate relationship against the spreadsheet.
    if entities.get("relationship"):
        valid_relationships = PEOPLE["Relationship"].dropna().unique()

        wanted = str(entities["relationship"]).strip().lower()

        matched_relationship = next(
            (
                item for item in valid_relationships
                if str(item).strip().lower() == wanted
            ),
            None
        )

        if matched_relationship is not None:
            entities["relationship"] = matched_relationship
        else:
            entities.pop("relationship", None)

    parsed["entities"] = entities

    return parsed


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
        return jsonify({
            "answer": "Please enter a question."
        }), 400

    state = session.get("dialogue_state", {})

    # Use the LLM only when explicitly enabled.
    if USE_LLM:
        try:
            parsed = parse_with_llm(message)
            parsed = prepare_entities(parsed)

        except Exception as error:
            print("LLM fallback:", error)
            parsed = parse(message, PEOPLE)

    else:
        parsed = parse(message, PEOPLE)

    # Carry forward previous conversation context.
    parsed = enrich_with_context(parsed, state)

    entities = parsed.get("entities", {})

    # Ask for clarification when multiple people match.
    if (
        "relationship" in entities
        and "person_id" not in entities
        and "when is my" in message.lower()
    ):

        matches = PEOPLE[
            PEOPLE["Relationship"].astype(str).str.lower()
            == str(entities["relationship"]).lower()
        ]

        if len(matches) > 1:

            session["dialogue_state"] = update_state(
                parsed,
                state,
                list(matches["Person_ID"])
            )

            names = ", ".join(
                matches["Name"].head(8).tolist()
            )

            return jsonify({
                "answer": (
                    f"I found {len(matches)} people with that relationship: "
                    f"{names}. Which one do you mean?"
                ),
                "debug": parsed
            })

    # Get factual answers from the spreadsheet service.
    answer = execute(parsed, PEOPLE)

    # Save conversation state.
    session["dialogue_state"] = update_state(
        parsed,
        state
    )

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
        version="V4",
        llm_enabled=USE_LLM
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
