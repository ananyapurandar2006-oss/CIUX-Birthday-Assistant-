
const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const question = document.getElementById('question');
const trace = document.getElementById('trace');
const resetButton = document.getElementById('reset-chat');

const speakButton = document.getElementById('speak-button');
const voiceOutput = document.getElementById('voice-output');

// Browser speech recognition support.
const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;
let isListening = false;


// Display a chat message.
function addMessage(text, role = 'bot') {
  const row = document.createElement('div');
  row.className = `message ${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;

  row.appendChild(bubble);
  chat.appendChild(row);

  chat.scrollTop = chat.scrollHeight;
}


// Read the assistant's response aloud.
function speakResponse(text) {
  if (!voiceOutput.checked || !('speechSynthesis' in window)) {
    return;
  }

  window.speechSynthesis.cancel();

  const speech = new SpeechSynthesisUtterance(text);
  speech.lang = 'en-IN';
  speech.rate = 1;
  speech.pitch = 1;

  window.speechSynthesis.speak(speech);
}


// Send a question to the existing Flask backend.
async function ask(text) {
  text = text.trim();

  if (!text) return;

  addMessage(text, 'user');

  question.value = '';
  question.disabled = true;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: text })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    const answer = data.answer || 'No answer returned.';

    addMessage(answer, 'bot');

    // Show the recognized question and dialogue trace.
    trace.textContent =
      'Question: ' + text + '\n\n' +
      'Assistant trace:\n' +
      JSON.stringify(data.debug || {}, null, 2);

    // Read the answer aloud when voice output is enabled.
    speakResponse(answer);

  } catch (error) {
    addMessage(`Error: ${error.message}`, 'bot');

  } finally {
    question.disabled = false;
    question.focus();
  }
}


// Send a typed question using the Send button.
form.addEventListener('submit', event => {
  event.preventDefault();
  ask(question.value);
});


// Example question buttons.
document.querySelectorAll('[data-q]').forEach(button => {
  button.addEventListener('click', () => {
    ask(button.dataset.q);
  });
});


// Start voice recognition.
if (SpeechRecognition) {

  recognition = new SpeechRecognition();

  recognition.lang = 'en-IN';
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    isListening = true;
    speakButton.textContent = '🎤 Listening...';
  };

  recognition.onresult = event => {
    const transcript = event.results[0][0].transcript;

    // Show recognized speech in the same question input.
    question.value = transcript;

    trace.textContent =
      'Recognized speech:\n' + transcript +
      '\n\nSending recognized question to the assistant...';

    // Use the same ask function as typed questions.
    ask(transcript);
  };

  recognition.onerror = event => {
    addMessage(
      'Voice recognition error: ' + event.error,
      'bot'
    );
  };

  recognition.onend = () => {
    isListening = false;
    speakButton.textContent = '🎤 Speak';
  };

  speakButton.addEventListener('click', () => {

    if (isListening) {
      recognition.stop();
      return;
    }

    try {
      recognition.start();
    } catch (error) {
      addMessage(
        'Could not start the microphone. Please try again.',
        'bot'
      );
    }

  });

} else {

  speakButton.disabled = true;

  speakButton.textContent = 'Voice not supported';

  addMessage(
    'Your browser does not support speech recognition. You can still type questions.',
    'bot'
  );
}


// Stop any ongoing speech when voice output is switched off.
voiceOutput.addEventListener('change', () => {
  if (!voiceOutput.checked && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
});


// Reset conversation and dialogue trace.
resetButton.addEventListener('click', async () => {

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }

  if (isListening && recognition) {
    recognition.stop();
  }

  try {
    const response = await fetch('/api/reset', {
      method: 'POST'
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    chat.innerHTML = '';
    trace.textContent = 'No query yet.';

    addMessage(
      data.message || 'Conversation reset successfully.',
      'bot'
    );

  } catch (error) {
    addMessage(`Reset error: ${error.message}`, 'bot');
  }
});


// V5 welcome message.
addMessage(
  'Hello! I am Birthday Assistant Version 5. You can type or speak your birthday questions. I can also read my answers aloud.',
  'bot'
);
