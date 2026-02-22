const addMessage = (message, sender) => {
  const messagesList = document.getElementById('messages');

  if (sender === 'client') {
    const messageItem = document.createElement('li');
    messageItem.innerHTML = `<span class="sent-text">${message}</span>`;
    messageItem.setAttribute('id', 'last-sent'); // Temporary ID to find it when echo arrives
    messagesList.appendChild(messageItem);

    messagesList.scrollTop = messagesList.scrollHeight;
  } else {
    const lastSent = document.getElementById('last-sent');

    if (lastSent) {
      const echoSpan = document.createElement('span');
      echoSpan.className = 'echo-text';
      echoSpan.innerText = `Received: ${message}`;

      lastSent.appendChild(echoSpan);
      lastSent.removeAttribute('id');
    } else {
      const messageItem = document.createElement('li');
      messageItem.innerText = message;
      messagesList.appendChild(messageItem);
    }

    messagesList.scrollTop = messagesList.scrollHeight;
  }
};

window.addEventListener('DOMContentLoaded', (event) => {
  // Update this URL to your actual server address
  const socket = new WebSocket('ws://localhost:8000/ws');

  socket.addEventListener('open', () => {
    console.log('Connected to Server');

    document.getElementById('form').addEventListener('submit', (event) => {
      event.preventDefault();
      const input = document.getElementById('message');
      const message = input.value;

      addMessage(message, 'client');
      socket.send(message);

      event.target.reset();
    });
  });

  socket.addEventListener('message', (event) => {
    addMessage(event.data, 'server');
  });

  socket.addEventListener('error', (error) => {
    console.error('WebSocket Error:', error);
  });
});