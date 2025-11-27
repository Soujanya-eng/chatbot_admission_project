document.addEventListener('DOMContentLoaded', function() {
    const chatToggle = document.getElementById('chatbot-toggle');
    const chatWindow = document.getElementById('chat-window');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // --- Core Function to Append and Format Messages ---
    function appendMessage(sender, text) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender + '-message');
        
        // Format bold (**text**) and newlines (\n)
        let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        formattedText = formattedText.replace(/\n/g, '<br>');
        
        // Basic link detection
        formattedText = formattedText.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" class="text-blue-600 underline">$1</a>');

        messageDiv.innerHTML = formattedText;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // --- Toggle Chat Window ---
    chatToggle.addEventListener('click', function() {
        const isHidden = chatWindow.classList.toggle('hidden');
        chatToggle.setAttribute('aria-expanded', !isHidden);

        if (!isHidden) {
            chatWindow.classList.add('open');
            userInput.focus();
            if (chatMessages.children.length === 0) {
                // Send 'hi' to initiate the first bot response
                simulateMessage('hi');
            }
        } else {
            chatWindow.classList.remove('open');
        }
    });

    // --- Server Communication ---
    async function sendMessage() {
        const message = userInput.value.trim();
        if (message === "") return;

        appendMessage('user', message);
        userInput.value = '';

        await simulateMessage(message);
    }

    async function simulateMessage(messageText) {
        try {
            // This fetches the response from your Python Flask app.py running at http://localhost:5000/chat
            const response = await fetch('http://localhost:5000/chat', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText }),
            });

            if (!response.ok) {
                throw new Error(`Server returned status: ${response.status}`);
            }

            const data = await response.json();
            appendMessage('bot', data.response);

        } catch (error) {
            console.error('Connection Error:', error);
            appendMessage('bot', '❌ Connection Failed: The chatbot server is unreachable. Please ensure your Python **app.py** is running in a separate terminal.');
        }
    }

    // Event listeners for Send button and Enter key
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});