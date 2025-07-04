class FloatingChatbot {
  constructor() {
    this.isOpen = false;
    this.messages = [];
    this.messageIdCounter = 1;

    this.initializeElements();
    this.bindEvents();
    this.addInitialMessage();
  }

  initializeElements() {
    this.chatContainer = document.getElementById('chat-container');
    this.chatToggle = document.getElementById('chat-toggle');
    this.closeChat = document.getElementById('close-chat');
    this.chatForm = document.getElementById('chat-form');
    this.userInput = document.getElementById('user-input');
    this.chatMessages = document.getElementById('chat-messages');
    this.chatIcon = document.getElementById('chat-icon');
    this.closeIcon = document.getElementById('close-icon');
    this.notificationBadge = document.getElementById('notification-badge');
  }

  bindEvents() {
    this.chatToggle.addEventListener('click', () => this.toggleChat());
    this.closeChat.addEventListener('click', () => this.closeChatMethod());
    this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
  }

  addInitialMessage() {
    this.addMessage('¡Hola! ¿En qué puedo ayudarte hoy?', false);
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
    this.updateChatVisibility();
  }

  closeChatMethod() {
    this.isOpen = false;
    this.updateChatVisibility();
  }

  updateChatVisibility() {
    if (this.isOpen) {
      this.chatContainer.classList.remove('hidden');
      this.chatContainer.classList.add('block');
      this.chatToggle.classList.add('rotate-180');
      this.chatIcon.classList.add('hidden');
      this.closeIcon.classList.remove('hidden');
      this.notificationBadge.classList.add('hidden');
      this.userInput.focus();
    } else {
      this.chatContainer.classList.add('hidden');
      this.chatContainer.classList.remove('block');
      this.chatToggle.classList.remove('rotate-180');
      this.chatIcon.classList.remove('hidden');
      this.closeIcon.classList.add('hidden');
      this.notificationBadge.classList.remove('hidden');
    }
  }

  handleSubmit(e) {
    e.preventDefault();
    const message = this.userInput.value.trim();
    if (!message) return;

    this.addMessage(message, true);
    this.userInput.value = '';

    // Simular respuesta automática
    setTimeout(() => {
      const responses = [
        'Gracias por tu mensaje. ¿En qué más puedo ayudarte?',
        'Entiendo tu consulta. Te ayudo con eso.',
        'Perfecto, déjame ayudarte con esa información.',
        'Excelente pregunta. Aquí tienes la respuesta.',
        'Me alegra poder asistirte. ¿Algo más en lo que pueda ayudar?'
      ];
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      this.addMessage(randomResponse, false);
    }, 1000);
  }

  addMessage(text, isUser) {
    const messageId = this.messageIdCounter++;
    const message = {
      id: messageId,
      text,
      isUser,
      timestamp: new Date()
    };

    this.messages.push(message);
    this.renderMessage(message);
    this.scrollToBottom();
  }

  renderMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `flex ${message.isUser ? 'justify-end' : 'justify-start'}`;

    const messageContent = document.createElement('div');
    messageContent.className = `max-w-xs px-4 py-2 rounded-2xl text-sm ${
      message.isUser
        ? 'bg-blue-500 text-white rounded-br-md'
        : 'bg-white text-gray-800 border border-gray-200 rounded-bl-md'
    }`;
    messageContent.textContent = message.text;

    messageDiv.appendChild(messageContent);

    const messagesContainer = this.chatMessages.querySelector('.space-y-3');
    messagesContainer.appendChild(messageDiv);
  }

  scrollToBottom() {
    setTimeout(() => {
      this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }, 100);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new FloatingChatbot();
});
