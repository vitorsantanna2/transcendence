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

let player1_X = 0, player1_Y = 0;
let player2_X = 0, player2_Y = 0;
let ballX = 0, ballY = 0;
let speed_x = 0, speed_y = 0;
let radius = 0;
let width = 0, height = 0;
let playerId;

socket.onopen = function() {
    console.log("WebSocket connection opened");
};

socket.onerror = function(error) {
    console.log("WebSocket error: " + error);
};

socket.onmessage = function(e) {
    let data = JSON.parse(e.data);

    if (data.player === 1) {
        player1_X = data.x;
        player1_Y = data.y;
    } else if (data.player === 2) {
        player2_X = data.x;
        player2_Y = data.y;
    } else if (data.type === 'ball_position') {
        radius = data.radius;
        ballX = data.x;
        ballY = data.y;
        speed_x = data.speed_x;
        speed_y = data.speed_y;
        width = data.width;
        height = data.height;
    }
    draw();
};

// document.addEventListener('keydown', (event) => {
//     let key = event.key;
//     let movement = null;

//     if (key === 'w') {
//         movement = { type: 'player1_move', direction: 'up' };
//     } else if (key === 's') {
//         movement = { type: 'player1_move', direction: 'down' };
//     } else if (key === 'ArrowUp') {
//         movement = { type: 'player2_move', direction: 'up' };
//     } else if (key === 'ArrowDown') {
//         movement = { type: 'player2_move', direction: 'down' };
//     }

//     // Enviando o movimento para o backend via WebSocket
//     if (movement) {
//         socket.send(JSON.stringify(movement));
//     }
// });


function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(p1Image, player1_X, player1_Y, 50, 70);
    ctx.drawImage(p2Image, player2_X, player2_Y, 50, 70);
    ctx.drawImage(ballImage, ballX, ballY, 15, 15);
}
draw();