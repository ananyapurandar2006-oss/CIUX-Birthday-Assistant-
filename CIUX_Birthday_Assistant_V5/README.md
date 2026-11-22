
# CIUX Birthday Assistant – Version 5

## Project Overview
Version 5 is a conversational birthday assistant that supports both text and voice interaction. Users can ask questions about birthdays, relationships and places of stay using natural language.

## Main Features
- Rule-based birthday search
- Natural Language Understanding (NLU)
- Intent recognition and entity extraction
- Dialogue management and conversation context
- LLM semantic parsing integration with rule-based fallback
- Voice input using browser speech recognition
- Spoken responses using speech synthesis
- Text-based interaction

## Technologies Used
- Python
- Flask
- HTML, CSS and JavaScript
- Pandas
- Excel
- Web Speech API
- Speech Synthesis API

## Dataset
The application uses an Excel dataset containing 100 fictional people. It includes names, dates of birth, relationships and places of stay.

## How to Run
1. Open the V5 folder in Visual Studio Code.
2. Open the terminal.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run:
   `python app.py`
5. Open `http://127.0.0.1:5000` in your browser.
6. Allow microphone access to test voice input.

## Testing
The V5 automated tests were executed successfully: 6 tests passed.

Voice input, spoken responses and text-only interaction were also tested manually.

## LLM Integration Note
V4 includes LLM integration code with a rule-based fallback. Live API execution was not demonstrated because API credits were unavailable.

## Privacy
The project uses fictional demonstration data. No real personal or family information is included.

## Conclusion
Version 5 completes the development of the CIUX Birthday Assistant by adding voice interaction to the context-aware conversational application.
