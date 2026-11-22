
# CIUX Birthday Assistant – System Architecture

## 1. Introduction

The CIUX Birthday Assistant is a web-based conversational system that allows users to ask birthday-related questions using text or voice.

The system is developed using Python Flask, HTML, CSS and JavaScript. It uses Natural Language Understanding (NLU), dialogue management and a structured Excel dataset containing 100 fictional people.

The main objective is to provide an easy way to search birthday dates, find upcoming birthdays and retrieve a person's location through natural-language questions.

## 2. V5 System Architecture

The following diagram represents the overall architecture of the CIUX Birthday Assistant Version 5.

```text
                    USER
                      |
             +--------+--------+
             |                 |
         Text Input        Voice Input
             |                 |
             |          Speech Recognition
             |                 |
             +--------+--------+
                      |
                Recognized Text
                      |
                Frontend (HTML,
                 CSS, JavaScript)
                      |
                Flask Backend
                      |
                 NLU Processing
                      |
             Intent and Entity Extraction
                      |
              Dialogue Management
                      |
              Context and Validation
                      |
                 Query Service
                      |
              Structured Dataset
              (100 Fictional People)
                      |
              Birthday / Place Result
                      |
              Response Generation
                      |
             +--------+--------+
             |                 |
         Text Display     Speech Output
             |                 |
             +--------+--------+
                      |
                    USER
```

## 3. Main System Components

### 3.1 User Interface

The frontend is developed using HTML, CSS and JavaScript. It provides a chat interface where users can enter questions, view responses, use the microphone and enable or disable speech output.

### 3.2 Speech Recognition

The browser SpeechRecognition API converts the user's spoken questions into text. The recognized text is sent to the backend for processing.

### 3.3 Flask Backend

Python Flask acts as the backend framework. It receives user questions through the `/api/chat` endpoint and coordinates the processing of requests.

### 3.4 Natural Language Understanding (NLU)

The NLU module understands the user's questions by identifying intents and extracting important entities.

Examples of entities include:
- Person names
- Months
- Dates
- Relationships
- Relative dates

### 3.5 Dialogue Management

The dialogue management module maintains conversation context. It allows users to ask follow-up questions without repeating all the previous information.

For example:

User: Any nephew birthdays in September?

User: What about October?

The system uses the previous conversation context to understand the follow-up question.

### 3.6 Data Service

The data service retrieves information from the structured Excel dataset using Python and Pandas.

The dataset contains 100 fictional people with details such as:
- Person ID
- Name
- Nickname
- Date of Birth
- Place of Stay
- Relationship

### 3.7 Response Generation

The response generation component creates readable answers using the information retrieved from the dataset.

### 3.8 Speech Synthesis

The browser SpeechSynthesisUtterance API converts the assistant's text response into speech when the voice-output option is enabled.

## 4. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Natural Language Understanding | Rule-based NLU and LLM integration with fallback |
| Dialogue Management | Python |
| Dataset | Excel and Pandas |
| Speech Recognition | Web Speech API |
| Speech Synthesis | SpeechSynthesis API |
| Development Environment | Visual Studio Code |
| Browser | Google Chrome |

## 5. Working and Data Flow

The system follows these steps:

1. The user enters a question using text or the microphone.
2. If voice input is used, speech recognition converts the spoken question into text.
3. The frontend sends the question to the Flask backend.
4. The NLU module identifies the user's intent and extracts relevant entities.
5. Dialogue management checks the conversation context.
6. The query service retrieves the required information from the Excel dataset.
7. The system generates a response based on the retrieved data.
8. The response is displayed in the chat interface.
9. If speech output is enabled, the browser reads the response aloud.

## 6. Privacy and Security

The project uses a synthetic dataset containing fictional people for demonstration purposes.

Important privacy practices include:

- Avoid using real personal information in the demonstration dataset.
- Do not expose API keys or secret credentials.
- Store API keys in environment variables.
- Do not share sensitive information publicly.
- Use only the information required to answer user questions.

## 7. Conclusion

The CIUX Birthday Assistant Version 5 combines text and voice interaction in a single conversational system.

It uses Python Flask, Natural Language Understanding, dialogue management and a structured Excel dataset to answer birthday-related questions.

The addition of speech recognition and speech synthesis makes the system easier to interact with. The final architecture demonstrates the development of a task-oriented conversational assistant with context-aware responses and voice support.
