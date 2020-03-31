var piece_size_px = 50;
var field_size_px = 100;

var players = [
    document.querySelector('.player-1'),
    document.querySelector('.player-2')
]; // players


var board_wrap = document.querySelector('.board .pieces-wrap');
// 画布

var next_wrap = document.querySelector('.next');
// 下一个放置的棋子

var remaining_wrap = document.querySelector('.remaining');
// 剩下的棋子

var field_set_names = [
    'r-1', 'r-2', 'r-3', 'r-4',
    'c-A', 'c-B', 'c-C', 'c-D',
    'd-1', 'd-2'
];
var field_sets = {};
for (var name of field_set_names) {
    field_sets[name] = document.querySelectorAll('.' + name);
}

function create_piece_element(piece) {
    var el = document.createElement('div');
    el.classList.add('piece');
    if (piece[0] === "1") {
        el.classList.add('dark');
    }
    if (piece[1] === "1") {
        el.classList.add('round');
    }
    if (piece[2] === "1") {
        el.classList.add('tall');
    }
    if (piece[3] === "1") {
        el.classList.add('hole');
    }
    return el;
}

function highlight_winning_row(board) {
    function is_winning_row(pieces) {
        if (pieces.some(function (p) {
            return p == null;
        })) {
            return false;
        }
        for (var prop of [0, 1, 2, 3]) {
            if (pieces.every(function (p) {
                return pieces[0][prop] == p[prop];
            })) {
                return true;
            }
        }
        return false;
    }
    function add_winning_class(name) {
        for (var el of field_sets[name]) {
            el.classList.add('in-winning-row');
        }
    }

    var pieces;

    // Rows
    for (var r of [0, 1, 2, 3]) {
        pieces = [
            board['A'][r],
            board['B'][r],
            board['C'][r],
            board['D'][r]
        ];
        if (is_winning_row(pieces)) {
            add_winning_class('r-' + (r + 1));
        }
    }

    // Columns
    for (var c of 'ABCD') {
        pieces = board[c];
        if (is_winning_row(pieces)) {
            add_winning_class('c-' + c);
        }
    }

    // Diagonals
    pieces = [
        board['A'][0],
        board['B'][1],
        board['C'][2],
        board['D'][3]
    ];
    if (is_winning_row(pieces)) {
        add_winning_class('d-1');
    }
    pieces = [
        board['A'][3],
        board['B'][2],
        board['C'][1],
        board['D'][0]
    ];
    if (is_winning_row(pieces)) {
        add_winning_class('d-2');
    }
}

function render_state(state) {
    // Title
//    players[0].textContent = state.players[0];
//    players[1].textContent = state.players[1];
//    players[0].classList.remove('player-active');
//    players[1].classList.remove('player-active');
//    if (state.active_player != null) {
//        players[state.active_player].classList.add('player-active');
//    }

    // Board
    render_board(state.board)

    // Highlight winning row
    if (state.winner != null) {
        highlight_winning_row(state.board);
    }

    // Next
    remaining_wrap.innerHTML = '';
    for (var i = 0; i < state.remaining.length; i++) {
        var piece = state.remaining[i];
        var el = create_piece_element(piece);
        remaining_wrap.appendChild(el);
    }

    // Remaining
    next_wrap.innerHTML = '';
    if (state.next_piece != null) {
        var piece = state.next_piece;
        var el = create_piece_element(piece);
        next_wrap.appendChild(el);
    }
}

function render_board(board) {
    var cols = 'ABCD'.split('');

    board_wrap.innerHTML = '';

    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            var piece = board[cols[j]][i];
            if (piece != null) {
                var el = create_piece_element(piece);
                el.style.bottom = piece_size_px / 2 + field_size_px * i + 'px';
                el.style.left = piece_size_px / 2 + field_size_px * j + 'px';
                board_wrap.appendChild(el);
            }
        }
    }
}

var ws_url = (location.protocol === 'https:' ? 'wss:' : 'ws:') + '//' +
    location.host + '/api/v1/games/' + game_id + '/message-channel';

$ajax({
    url:'getnextstep',
    method: 'POST',
    type:'JSON',
    data:{
        remaining_pieces:,
        board:,
        next_piece
    },
    success: function(rq){
        render_board(JSON.parse(rq))
    },
    loading: function(rq){
        text = "AI is thinking ..."
    }
});