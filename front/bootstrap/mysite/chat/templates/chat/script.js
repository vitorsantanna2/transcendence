  


    document.getElementById('send-button').addEventListener('click', function()
    {
      var messageInput = document.getElementById('message-input');
      var chatInbox = document.getElementById('chat-inbox');
      var newMessage = document.createElement('p');
      newMessage.textContent = messageInput.value;
      var br = document.createElement('br');
      chatInbox.appendChild(br);
      chatInbox.appendChild(newMessage);
      messageInput.value = '';
    });
