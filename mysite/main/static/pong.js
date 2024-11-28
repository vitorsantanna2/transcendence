document.addEventListener('DOMContentLoaded', () => {
    console.log("Game ID from template:", game_id);

    const socket = new WebSocket(`ws://` + window.location.host + `/ws/main/${game_id}/`);

    socket.onmessage = function(event) {
        console.log(`[message] Data received from server: ${event.data}`);
    };

    socket.onclose = function(event) {
        if (event.wasClean) {
            console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
        } else {
            console.log('[close] Connection died');
        }
    };

    socket.onerror = function(error) {
        console.log(`[error] ${error.message}`);
    };

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
    let player1_score = 0, player2_score = 0;
    let playerId;

    socket.onopen = function() {
        console.log("WebSocket conectado com game_id:", game_id);
    };

    socket.onerror = function(error) {
        console.log("WebSocket error: " + error);
    };

    socket.onmessage = function(e) {
        let data = JSON.parse(e.data);
        
        if (data.type === 'player_position') {
            if (data.player === 1) {
                player1_X = data.x;
                player1_Y = data.y;
                player1_speed = data.speed;
                player1_score = data.score;
            } else if (data.player === 2) {
                player2_X = data.x;
                player2_Y = data.y;
                player2_speed = data.speed;
                player2_score = data.score;
            }
        }
        if (data.type === 'ball_position') {
            radius = data.radius;
            ballX = data.x;
            ballY = data.y;
            speed_x = data.speed_x;
            speed_y = data.speed_y;
            width = data.width;
            height = data.height;
        }
    };

    document.addEventListener('keydown', (event) => {
        let key = event.key;
        let movement = null;

        if (key === 'w') {
            player1_Y -= player1_speed;
            movement = { player: 1, direction: 'up' };
        } else if (key === 's') {
            player1_Y += player1_speed;
            movement = { player: 1, direction: 'down' };
        } else if (key === 'ArrowUp') {
            player2_Y -= player2_speed;
            movement = { player: 2, direction: 'up' };
        } else if (key === 'ArrowDown') {
            player2_Y += player2_speed;
            movement = { player: 2, direction: 'down' };
        }
        if (movement) {
            socket.send(JSON.stringify(movement));
        }
    });

    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(p1Image, player1_X, player1_Y, 50, 70);
        ctx.drawImage(p2Image, player2_X, player2_Y, 50, 70);
        ctx.drawImage(ballImage, ballX, ballY, 15, 15);
        ctx.font = "30px Arial";
        ctx.fillText(player1_score, 20, 30);
        ctx.fillText(player2_score, canvas.width - 150, 30);
        requestAnimationFrame(draw);
    }
    draw();
});