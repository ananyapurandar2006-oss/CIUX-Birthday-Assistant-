
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-6.2-astra")

ALLOWED_INTENTS = {
    "birthday_search",
    "count_birthdays",
    "upcoming_birthdays",
    "person_place",
    "unknown"
}

ALLOWED_ENTITIES = {
    "person_name",
    "relationship",
    "month",
    "relative_date",
    "relative_month",
    "place"
}

SYSTEM_PROMPT = """
You are the Natural Language Understanding component
of a Birthday Assistant.

Your task is ONLY to identify the user's intent and entities.

Return your result as a valid JSON object.
The output must be JSON and nothing else.

Do not answer the user's question.
Do not invent names, birthdays, dates or places.
Do not provide information that is not in the user's message.

Use this JSON format:

{
    "intent": "birthday_search",
    "entities": {
        "person_name": "",
        "relationship": "",
        "month": "",
        "relative_date": "",
        "relative_month": "",
        "place": ""
    }
}

Allowed intents:
- birthday_search
- count_birthdays
- upcoming_birthdays
- person_place
- unknown

Entity rules:
- person_name: a person's name mentioned by the user.
- relationship: nephew, niece, wife, husband, father,
  mother, friend, uncle or aunt.
- month: a month explicitly mentioned by the user.
- relative_date: today, tomorrow or this week.
- relative_month: next month or this month.
- place: a location mentioned by the user.

Use only allowed entity keys.
Use empty strings for missing entities.
Never guess missing information.
"""


def parse_with_llm(message):

    if not API_KEY:
        raise ValueError("OPENAI_API_KEY is missing.")

    if not message or not message.strip():
        return {
            "intent": "unknown",
            "entities": {}
        }

    client = OpenAI(api_key=API_KEY)

    response = client.responses.create(
        model=MODEL,
        instructions=SYSTEM_PROMPT,
        input="Return JSON for this user message: " + message.strip(),
        text={
            "format": {
                "type": "json_object"
            }
        }
    )

    output = response.output_text

    if not output:
        raise ValueError("The model returned an empty response.")

    parsed = json.loads(output)

    if not isinstance(parsed, dict):
        raise ValueError("Invalid JSON response.")

    intent = parsed.get("intent", "unknown")

    if intent not in ALLOWED_INTENTS:
        intent = "unknown"

    entities = parsed.get("entities", {})

    if not isinstance(entities, dict):
        entities = {}

    clean_entities = {}

    for key, value in entities.items():
        if key in ALLOWED_ENTITIES and value not in (None, ""):
            if isinstance(value, (str, int, float)):
                clean_entities[key] = value

    return {
        "intent": intent,
        "entities": clean_entities
    }
