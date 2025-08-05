function openChat() {
  document.getElementById('chat-widget').style.display = 'block';
  document.querySelector('.chat-toggle').style.display = 'none';
}

function closeChat() {
  document.getElementById('chat-widget').style.display = 'none';
  document.querySelector('.chat-toggle').style.display = 'block';
}

function sendMessage() {
  const input = document.getElementById('chat-input');
  const message = input.value.trim();

  if (message) {
    const chatMessages = document.getElementById('chat-messages');
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.innerHTML = '<p>' + message + '</p>';
    chatMessages.appendChild(userMessage);

    input.value = '';

    setTimeout(() => {
      const agentMessage = document.createElement('div');
      agentMessage.className = 'message agent';
      agentMessage.innerHTML = '<p>Merci pour votre message. Un de nos agents va vous répondre dans quelques instants.</p>';
      chatMessages.appendChild(agentMessage);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);

    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const chatInput = document.getElementById('chat-input');
  if (chatInput) {
    chatInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
  }
});
