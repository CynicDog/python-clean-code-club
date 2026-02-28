let currentUsername = "";

const addMessage = (message, senderName) => {
  const messagesList = document.getElementById('messages');
  const messageItem = document.createElement('li');

  if (senderName === currentUsername) {
    messageItem.className = 'message-client';
    messageItem.innerText = message;
  } else {
    messageItem.className = 'message-server';
    messageItem.innerHTML = `<span class="username-label">${senderName}</span>${message}`;
  }

  messagesList.appendChild(messageItem);
  messagesList.scrollTop = messagesList.scrollHeight;
};

window.addEventListener('DOMContentLoaded', () => {
  currentUsername = prompt("Enter your username:") || "Anonymous";

  const socket = new WebSocket(`ws://localhost:8000/ws?username=${currentUsername}`);

  socket.addEventListener('open', () => {
    console.log('Connected to Server');

    document.getElementById('form').addEventListener('submit', (event) => {
      event.preventDefault();
      const input = document.getElementById('message');
      const message = input.value;

      socket.send(message);

      event.target.reset();
    });
  });

  socket.addEventListener('message', (event) => {
    try {
      const data = JSON.parse(event.data);
      addMessage(data.message, data.username);
    } catch (e) {
      console.error("Error parsing message:", e);
    }
  });

  socket.addEventListener('error', (error) => {
    console.error('WebSocket Error:', error);
  });

  socket.addEventListener('close', () => {
    console.log('Disconnected from server');
  });
});