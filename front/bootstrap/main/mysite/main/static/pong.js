const socket = new WebSocket('ws://localhost:8000/ws/main/');
    
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
    
let player1_X = 40, player1_Y = 250;
let player2_X = 710, player2_Y = 250;
let ballX = 400, ballY = 300;

socket.onmessage = function(e) {
    let data = JSON.parse(e.data);
        
    if (data.type === 'player1_position') {
        player1_X = data.x;
        player1_Y = data.y;
    } else if (data.type === 'player2_position') {
        player2_X = data.x;
        player2_Y = data.y;
    } else if (data.type === 'ball_position') {
        ballX = data.x;
        ballY = data.y;
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