document.addEventListener('DOMContentLoaded', function () {
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const userMessage = messageInput.value.trim();
        if (userMessage === '') return;
        addMessage(userMessage, 'user-message');
        messageInput.value = '';
        fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const botResponse = data.response || 'Bot did not respond.';
            addMessage(botResponse, 'bot-message');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('Error connecting to the server. Please try again.', 'bot-message');
        });
    }

    function addMessage(text, className) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${className}`;
        messageElement.textContent = text;
        chatBox.appendChild(messageElement);
        setTimeout(() => {
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 100);
    }
});
