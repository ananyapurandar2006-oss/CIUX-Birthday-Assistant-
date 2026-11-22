# CIUX Birthday Assistant

## Project Overview
The CIUX Birthday Assistant is a web-based conversational application that helps users find birthday and location information using natural-language text or voice questions.

The project is developed using Python, Flask, HTML, CSS, JavaScript, NLU, dialogue management and an Excel dataset containing 100 fictional people.

## Project Versions

| Version | Main Feature |
|---|---|
| V1 | Rule-based birthday assistant |
| V2 | Natural Language Understanding and entity extraction |
| V3 | Dialogue management and conversation context |
| V4 | LLM-based semantic parsing integration with rule-based fallback |
| V5 | Voice input and speech output |

## Technologies Used
- Python
- Flask
- HTML, CSS and JavaScript
- Pandas
- Excel
- Natural Language Understanding (NLU)
- Web Speech API
- Speech Synthesis API

## Dataset
The application uses a structured Excel dataset containing 100 fictional people. It includes names, dates of birth, relationships and places of stay.

No real personal or family information is used.

## How to Run the Project

1. Install Python.
2. Open the required version folder in Visual Studio Code.
3. Open the terminal.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Run the application:

   `python app.py`

6. Open the browser and visit:

   `http://127.0.0.1:5000`

## Testing
The project includes a testing document with test utterances, observations and voice-interface tests.

The V5 rule tests were executed successfully, with 6 tests passing.

## LLM Integration Note
Version 4 includes an LLM integration with a rule-based fallback. Live API execution was not demonstrated because API credits were unavailable. The fallback allows the application to continue processing supported questions.

## Privacy
Only fictional demonstration data is used. API keys and credentials should not be uploaded to a public repository.

## Conclusion
The project demonstrates the gradual development of a task-oriented conversational assistant from a basic rule-based system to a context-aware text and voice-based application.
