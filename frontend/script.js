document.addEventListener('DOMContentLoaded', () => {
    // 1. Get DOM elements
    const inputField = document.getElementById('chatbot-input');
    const messagesContainer = document.getElementById('chatbot-messages');
    const chatbotContainer = document.getElementById('chatbot-float');
    const closeButton = document.getElementById('close-btn');

    // Function to add a message
    function addMessage(text, sender) {
        const messageDiv = document.createElement('p');
        messageDiv.classList.add(`${sender}-message`); 
        messageDiv.innerHTML = text; 
        messagesContainer.appendChild(messageDiv);
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // 2. Handle User Input on 'Enter'
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && inputField.value.trim() !== '') {
            const userText = inputField.value.trim();
            addMessage(userText, 'user');
            
            sendQueryToPython(userText); 
            
            inputField.value = '';
        }
    });

    // 3. API Call to Flask Server
    function sendQueryToPython(query) {
        // CONFIRM: This must be the EXACT URL used in the main.py @app.route
        fetch('http://127.0.0.1:5000/api/chat', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
        })
        .then(response => {
            if (!response.ok) {
                // This catches 404 Not Found, 500 Server Error, etc.
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const botResponse = data.response; 
            addMessage(botResponse, 'bot');
        })
        .catch((error) => {
            console.error('Connection Error:', error);
            // Enhanced error message to help user debug the connection
            addMessage(`Critical Error! Cannot connect to the bot server (Flask). 
                        Please ensure **main.py** is running on **http://127.0.0.1:5000** and check the Network tab (F12) for the exact error code.`, 'bot');
        }); 
    }

    // 4. Close/Hide Button
    closeButton.addEventListener('click', () => {
        chatbotContainer.style.display = 'none'; 
    });
});