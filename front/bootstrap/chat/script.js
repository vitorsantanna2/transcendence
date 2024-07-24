document.querySelector('.chat-input button').addEventListener('click', () => {
    const input = document.querySelector('.chat-input input');
    if (input.value.trim() !== '') {
        const chatMessages = document.querySelector('.chat-messages');
        const newMessage = document.createElement('div');
        newMessage.className = 'chat-message user-message';
        newMessage.innerHTML = `<span class="sender">Você:</span> ${input.value}`;
        chatMessages.appendChild(newMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        input.value = '';
    }
});
