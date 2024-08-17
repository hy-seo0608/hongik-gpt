function addMessage(sender, message) {
var chatBox = document.getElementById('chat-box');
var messageDiv = document.createElement('div');
messageDiv.innerHTML = `<p><strong>${sender}:</strong> ${message}</p>`;
chatBox.appendChild(messageDiv);
chatBox.scrollTop = chatBox.scrollHeight;
}

function askQuestion() {
var question = document
    .getElementById('question')
    .value;
fetch('/dialog/', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-CSRFToken': '{{ csrf_token }}'
    },
    body: new URLSearchParams({'question': question})
})
    .then(response => response.json())
    .then(data => {
    var chatBox = document.getElementById('chat-box');

    addMessage('You', question);
    if (question === "총장님") {
        var buttonDiv = document.createElement('div');
        buttonDiv.innerHTML = `<button onclick="handleButtonClick('옵션1')">옵션1</button> <button onclick="handleButtonClick('옵션2')">옵션2</button>`;
        chatBox.appendChild(buttonDiv);
    } else {
        addMessage('Bot', data.answer);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
    document
        .getElementById('question')
        .value = '';
    })
    .catch(error => {
    console.error('Error:', error);
    });
}

function handleButtonClick(option) {
addMessage('You', option);
fetch('/dialog/', {
    method: 'POST',
    headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-CSRFToken': '{{ csrf_token }}'
    },
    body: new URLSearchParams({'question': option})
})
    .then(response => response.json())
    .then(data => {
    addMessage('Bot', data.answer);
    })
    .catch(error => {
    console.error('Error:', error);
    });
}