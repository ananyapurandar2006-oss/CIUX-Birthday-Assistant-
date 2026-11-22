
const chat = document.getElementById('chat');
const form = document.getElementById('chat-form');
const question = document.getElementById('question');
const trace = document.getElementById('trace');
const resetButton = document.getElementById('reset-chat');


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

    addMessage(data.answer || 'No answer returned.', 'bot');

    // Display the interpreted intent and extracted entities.
    trace.textContent = JSON.stringify(
      data.debug || {},
      null,
      2
    );

  } catch (error) {
    addMessage(`Error: ${error.message}`, 'bot');

  } finally {
    question.disabled = false;
    question.focus();
  }
}


// Send a question using the Send button.
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


// Reset the conversation and clear the dialogue trace.
resetButton.addEventListener('click', async () => {
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


// Welcome message.
addMessage(
  'Hello! I am Version 3. I can understand birthday questions, remember conversation context, and answer follow-up questions.',
  'bot'
);
