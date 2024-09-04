// Keyhook for enter button
document.getElementById('message-input').addEventListener('keyup', function(event) {
    if (event.key === 'Enter') {
        var message = this.value;
        this.value = ''; // Clear the input
        document.getElementById('chat-inbox').insertAdjacentHTML('beforeend', '<div><p>' + message + '</p></div>');
    }
});

// Click event for send button
document.getElementById('send-button').addEventListener('click', function() {
    var message = document.getElementById('message-input').value;
    document.getElementById('message-input').value = ''; // Clear the input
    document.getElementById('chat-inbox').insertAdjacentHTML('beforeend', '<div><p>' + message + '</p></div>');
});

