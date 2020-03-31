var piece_size_px = 50;
var field_size_px = 100;


var finished = false;
// click control:
var freezeClick = false;


document.addEventListener("click", freezeClickFn, true);

function freezeClickFn(e) {
    if (freezeClick) {
        e.stopPropagation();
        e.preventDefault();
    }
}


function freeArea(dom){
    dom.addEventListener("click", freezeClickFn, true);

    function freezeClickFn(e) {
            e.stopPropagation();
            e.preventDefault();
    }
}



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

var board_table = document.querySelectorAll('.board .field');

function getID(classname) {
    let result = classname.match(/.*r-([0-9]).*c-([A-D]).*/);
    let idrow = parseInt(result[1])-1;
    let idcolumn = "ABCD".indexOf(result[2]);
    return [idrow,idcolumn]
}

for (let spot of board_table){
    // get board_id
    var result =  getID(spot.className);
    var idrow = result[0];
    var idcolumn = result[1];

    if (board[idcolumn][idrow]){
        spot.classList.remove('field-no-piece')
    }else{
        spot.classList.add('field-no-piece')
        spot.onclick = function () {
            if (!next_wrap.innerHTML) return;
            let piecedom = next_wrap.querySelector("[piece]");
            if(!piecedom) return;
            let pieceid =piecedom.getAttribute("piece");
            this.onclick = null;
            let result =  getID(this.className);
            let idrow = result[0];
            let idcolumn = result[1];
            board[idcolumn][idrow] = pieceid;

            // clear the next_piece
            next_piece = "";

            // render the piece onto the board
            this.classList.remove('field-no-piece')
            var el = create_piece_element(pieceid);
            el.style.bottom = piece_size_px / 2 + field_size_px * idrow + 'px';
            el.style.left = piece_size_px / 2 + field_size_px * idcolumn + 'px';
            board_wrap.appendChild(el);

            // remove next piece
            next_wrap.innerHTML = "";

        }
    }
}

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
    el.setAttribute("piece",piece);

    return el;
}

function highlight_winning_row(board) {
    function is_winning_row(pieces) {
        if (pieces.some(function (p) {
            return p.length === 0;
        })) {
            return false;
        }
        for (var prop of [0, 1, 2, 3]) {
            if (pieces.every(function (p) {
                return pieces[0][prop] === p[prop];
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
            board[0][r],
            board[1][r],
            board[2][r],
            board[3][r]
        ];
        if (is_winning_row(pieces)) {
            add_winning_class('r-' + (r + 1));
        }
    }

    // Columns
    for (var c of [0, 1, 2, 3]) {
        pieces = board[c];
        if (is_winning_row(pieces)) {
            add_winning_class('c-' + "ABCD".charAt(c));
        }
    }

    // Diagonals
    pieces = [
        board[0][0],
        board[1][1],
        board[2][2],
        board[3][3]
    ];
    if (is_winning_row(pieces)) {
        add_winning_class('d-1');
    }
    pieces = [
        board[0][3],
        board[1][2],
        board[2][1],
        board[3][0]
    ];
    if (is_winning_row(pieces)) {
        add_winning_class('d-2');
    }
}

function render_board(board) {
    var cols = 'ABCD'.split('');

    board_wrap.innerHTML = '';

    for (var i = 0; i < 4; i++) {
        for (var j = 0; j < 4; j++) {
            var piece = board[j][i];
            if (piece) {
                // var repeateddom = board_wrap.querySelector("[piece='"+piece+"']");
                // if(repeateddom) repeateddom.remove();
                var el = create_piece_element(piece);
                el.style.bottom = piece_size_px / 2 + field_size_px * i + 'px';
                el.style.left = piece_size_px / 2 + field_size_px * j + 'px';
                board_wrap.appendChild(el);
            }
        }
    }
}

var selectnextpiece = function () {
    if (finished) return;
    if (next_wrap.innerHTML) return;
    this.onclick = null;
    next_wrap.innerHTML = '';
    var piece = this.getAttribute("piece");
    var el = create_piece_element(piece);
    next_wrap.appendChild(el);
    this.classList.add('hidetransition');
    var self = this;
    this.addEventListener("transitionend", function () {
        self.classList.remove("hidetransition");
        self.classList.add("hide");
        // el.onclick = cancelnextpiece;
        next_piece = piece;
        remaining_piece = remaining_piece.filter(item => item !== next_piece);

        // connect to the server
        $ajax({
            url:'getnextstep',
            method: 'POST',
            type:'JSON',
            data:{
                remaining_pieces:remaining_piece,
                board:board,
                next_piece:next_piece
            },
            success: function(rq){
                players[1].innerHTML = "AI";
                data = JSON.parse(rq.responseText);
                remaining_piece = data.remaining;
                board = data.board;
                next_piece = data.next_piece;
                state = data.state;
                render_state(data);
                freezeClick = false;
            },
            loading: function(rq){
                text = "AI is thinking ...";
                players[1].innerHTML += " <span class=\"spinner-border text-primary\" role=\"status\"></span>";
                freezeClick = true;
            }
        });

    });
    };

var cancelnextpiece = function(){
    this.onclick = null;
    var piece = this.getAttribute("piece");
    var el = remaining_wrap.querySelector("[piece='"+piece+"']");
    el.classList.remove("hide");
    el.onclick = selectnextpiece;
    next_piece = "";
    this.remove()
};


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
    render_board(state.board);

    // Highlight winning row
    if (state.winner) {
        highlight_winning_row(state.board);
        freezeClick = true;
        finished = true;
        freeArea(document)

        var banner =  $id("banner");
        banner.classList.add("alert");
        banner.classList.add("banner");

        if (state.winner > 0){
            banner.classList.add("alert-success");
            text = "Congratulation! You won the game.";
        }else if(state.winner <0){
            banner.classList.add("alert-danger");
            text = "What a pity! You lost the game.";
        }else{
            banner.classList.add("alert-warning");
            text = "The game is fair.";
        }
        banner.innerText = text + " Refresh to restart the game.";
        document.querySelector('.bg').style.zIndex = 100;
    }

    // Next
    remaining_wrap.innerHTML = '';
    for (var i = 0; i < state.remaining.length; i++) {
        var piece = state.remaining[i];
        var el = create_piece_element(piece);
        el.onclick = selectnextpiece;
        remaining_wrap.appendChild(el);
    }

    // Remaining
    next_wrap.innerHTML = '';
    if (state.next_piece) {
        var piece = state.next_piece;
        var el = create_piece_element(piece);
        next_wrap.appendChild(el);
    };
};

render_state({
    board: board,
    remaining:remaining_piece,
    winner:null,
    next_piece: next_piece
});


//$ajax({
//    url:'getnextstep',
//    method: 'POST',
//    type:'JSON',
//    data:{
//        remaining_pieces:"TEST",
//        board:"TEST",
//        next_piece:"TEST"
//    },
//    success: function(rq){
//        state = JSON.parse(rq.responseText);
//        // state.board
//        // state.winner
//        // state.next_piece
//        // state.remaining
//        render_state(state)
//    },
//    loading: function(rq){
//        text = "AI is thinking ..."
//    }
//});