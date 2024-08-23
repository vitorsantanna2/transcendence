  


//    document.getElementById('send-button').addEventListener('click', function()
document.getElementById('send-button').addEventListener('click', function() {
  var messageInput = document.getElementById('message-input');
  var chatInbox = document.getElementById('chat-inbox');
  var newMessage = document.createElement('p');
  newMessage.textContent = messageInput.value;
  chatInbox.appendChild(newMessage);
  messageInput.value = '';
  console.log(newMessage); // This will log the new message element to the console
});
