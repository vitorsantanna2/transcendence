const socket = new WebSocket('ws://' + window.location.host + '/ws/main/');

const canvas = document.getElementById('pongCanvas');
const ctx = canvas.getContext('2d');
canvas.width = 800;
canvas.height = 600;

const p1Image = new Image();
p1Image.src = p1ImageUrl;

const p2Image = new Image();
p2Image.src = p2ImageUrl;

const ballImage = new Image();
ballImage.src = ballImageUrl;

// Inicializando as variáveis no escopo global com valores padrão
let player1_X = 0, player1_Y = 0;
let player2_X = 0, player2_Y = 0;
let ballX = 0, ballY = 0;

// Adicionando logs para depuração
socket.onopen = function() {
    console.log("WebSocket connection opened");
};

socket.onerror = function(error) {
    console.log("WebSocket error: " + error);
};

socket.onclose = function() {
    console.log("WebSocket connection closed");
};

socket.onmessage = function(e) {
    console.log("Message received from server");
    let data = JSON.parse(e.data);
    console.log("Data received: ", data);
    
    if (data.type === 'player1_position') {
        player1_X = data.x;
        player1_Y = data.y;
    } else if (data.type === 'player2_position') {
        player2_X = data.x;
        player2_Y = data.y;
    } else if (data.type === 'ball_position') {
        console.log("Ball position received: ", data);
        ballX = data.x;
        ballY = data.y;
        speedX = data.speed_x;
        speedY = data.speed_y;
    }
    draw();
};

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(p1Image, player1_X, player1_Y, 50, 70);
    ctx.drawImage(p2Image, player2_X, player2_Y, 50, 70);
    ctx.drawImage(ballImage, ballX, ballY, 15, 15);
}
draw();