async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();

    if (!message) return;

    input.value = '';

    // Add user message to chat
    addMessage(message, 'user');

    // Show typing indicator
    const typingId = addTyping();

    try {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Remove typing indicator
        removeTyping(typingId);

        // Add bot response
        addMessage(data.response, 'bot');

        // Update mood pill
        updateMood(data.sentiment);

        // Add mood tag to user message
        addMoodTag(data.sentiment);

    } catch (error) {
        removeTyping(typingId);
        addMessage('Sorry, something went wrong. Please try again.', 'bot');
    }
}

function addMessage(text, sender) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = `message ${sender}-message`;
    div.id = sender === 'user' ? `user-msg-${Date.now()}` : '';
    div.innerHTML = `<div class="message-bubble">${text.replace(/\n/g, '<br>')}</div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div;
}

function addMoodTag(sentiment) {
    const container = document.getElementById('chat-messages');
    const userMessages = container.querySelectorAll('.user-message');
    const lastUserMessage = userMessages[userMessages.length - 1];
    if (lastUserMessage) {
        const tag = document.createElement('div');
        tag.className = `mood-tag ${sentiment.toLowerCase()}`;
        tag.textContent = sentiment;
        lastUserMessage.appendChild(tag);
    }
}

function addTyping() {
    const container = document.getElementById('chat-messages');
    const id = `typing-${Date.now()}`;
    const div = document.createElement('div');
    div.className = 'message bot-message';
    div.id = id;
    div.innerHTML = `<div class="message-bubble" style="color: var(--muted);">Thinking...</div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return id;
}

function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function updateMood(sentiment) {
    const pill = document.getElementById('current-mood');
    if (!pill) return;
    pill.textContent = sentiment;
    pill.className = `mood-pill mood-tag ${sentiment.toLowerCase()}`;
}

// Send on Enter key
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('user-input');
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    // Scroll to bottom of chat
    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});