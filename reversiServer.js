var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

var randomstring = require("randomstring");

var Board = require('./board.js')

html_dir = '/views/'

http.listen(8080);//8100

app.get('/', function (req, res) {
    res.sendFile('public/index.html', {root: __dirname});
});

var pOneToken = randomstring.generate(8);
var pTwoToken = randomstring.generate(8);

console.log('Player one token: ' + pOneToken);
console.log('Player two token: ' + pTwoToken);

var pOne = false;
var pTwo = false;

board = new Board(8);

// Set authentication
io.use(function(socket, next) {
    var query = socket.handshake.query;

    if (pOne == false && query.token === pOneToken) {
        console.log('Player One authenticated');
        pOne = socket.id;
        next();
    }
    else if (pTwo == false && query.token === pTwoToken) {
        console.log('Player Two authenticated');
        pTwo = socket.id;
        next();
    }
    else {
        console.log('Authenticate Failed!');
        next(new Error('not authorized'));
    }

});

// Logic on connection
var turn = 1;
io.on('connection', function (socket) {
    var player, foe, receiveId;

    if (socket.id === pOne) {
        // Player one logic
        player = 1;
        foe = 2;

        result = board.count()

        if (pTwo) {
            var toId = (turn == 1) ? pOne : pTwo;
            io.to(toId).emit('yourturn', {player: turn, player1: result.p1, player2: result.p2, board: board.board, message: 'init'});
        }
    }
    if (socket.id === pTwo) {
        // Player two logic
        player = 2;
        foe = 1;

        result = board.count()

        if (pOne) {
            var toId = (turn == 1) ? pOne : pTwo;
            io.to(toId).emit('yourturn', {player: turn, player1: result.p2, player2: result.p2, board: board.board, message: 'init'});
        }
    }

    result = board.count()

    socket.emit('updated', {player: turn, player1: result.p1, player2: result.p2, board: board.board, message: 'update'});

    socket.on('mymove', function(data){
        if (!pOne || !pTwo) {
            socket.emit('errormessage', 'waiting for compponent!');
            return;
        }

        if (player != turn) {
            socket.emit('errormessage', 'not your turn!');
            return;
        }

        var y = parseInt(data.rowIdx);
        var x = parseInt(data.colIdx);

        var result = !isNaN(x) && !isNaN(y) && board.go(player, y, x);

        if (result) {
            // Check wether opponent can move
            var foe_can_move = board.have_move(foe);

            // Check wether player can move
            var player_can_move = board.have_move(player);

            if (foe_can_move) {
                // Change turn to other player
                turn = foe;

                var receiveId = (player == 1) ? pTwo : pOne;

                result = board.count()

                io.to(receiveId).emit('yourturn', {player: foe, player1: result.p1, player2: result.p2, board: board.board, message: ''});
                socket.emit('updated',{player: foe, player1: result.p1, player2: result.p2, board: board.board, message: 'valid'});
            }
            else if (player_can_move) {
                // Opponent can't move, player continue to play
                result = board.count()
                
                socket.emit('yourturn', {player: player, player1: result.p1, player2: result.p2, board: board.board, message: ''});

                // Send updated board to the rest
                var receiveId = (player == 1) ? pTwo : pOne;
                io.to(receiveId).emit('updated', {player: player, player1: result.p1, player2: result.p2, board: board.board, message: 'valid'});
            } else {
                turn = -1;
                result = board.count();

                var winner;
                if (result.p1 == result. p2)
                    winner = 0;
                else if (result.p1 > result.p2)
                    winner = 1;
                else
                    winner = 2;
                io.of('/').emit('end', {winner: winner, player1: result.p1, player2: result.p2});
                // TODO: start new match?
            }
        }
        else {
            // Invalid move
            socket.emit('yourturn', {player: player, board: board.board, message: 'invalid', status: -1});
        }
    });

    socket.on('disconnect', function(){
        if (socket.id === pOne) {
            pOne = false;
            console.log('Lost connection to Player 1!');
        }
        if (socket.id === pTwo) {
            pTwo = false;
            console.log('Lost connection to Player 2!');
        }
    });

});

var spectator = io.of('/spectator');

spectator.on('connection', function(socket) {
    socket.on('get', function() {
        var count = board.count();
        socket.emit('board', {board: board.board, player: turn, player1: count.p1, player2: count.p2});
    });
});
