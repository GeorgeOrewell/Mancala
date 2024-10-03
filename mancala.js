// Mancala initial game state
let pits = {
    p1: 4, p2: 4, p3: 4, p4: 4, p5: 4, p6: 4,
    p7: 4, p8: 4, p9: 4, p10: 4, p11: 4, p12: 4,
    player1Store: 0,
    player2Store: 0
};

let currentPlayer = 1;

// Function to render the current state of the board
function renderBoard() {
    for (let pit in pits) {
        document.getElementById(pit).innerText = pits[pit];
    }
}

// Function to handle pit clicks
function pitClicked(pitId) {
    if (currentPlayer === 1 && pitId.startsWith('p') && pitId <= 'p6') {
        moveStones(pitId);
    } else if (currentPlayer === 2 && pitId.startsWith('p') && pitId >= 'p7') {
        moveStones(pitId);
    }
}

function checkCapture(lastPit) {
    // Überprüfen, ob der letzte Stein in eine leere Mulde des aktuellen Spielers gefallen ist
    if (currentPlayer === 1 && lastPit.startsWith('p') && pits[lastPit] === 1 && lastPit <= 'p6') {
        // Gegenüberliegendes Feld finden (Player 2 Mulden sind p7-p12)
        let oppositePit = 'p' + (13 - parseInt(lastPit.slice(1)));
        let capturedStones = pits[oppositePit];
        pits[oppositePit] = 0;  // Steine im gegenüberliegenden Feld entfernen
        pits[lastPit] = 0;      // Den letzten Stein aus dem aktuellen Feld entfernen
        pits['player1Store'] += capturedStones + 1;  // Steine in den Speicher des Spielers legen
    }
    if (currentPlayer === 2 && lastPit.startsWith('p') && pits[lastPit] === 1 && lastPit >= 'p7') {
        // Gegenüberliegendes Feld finden (Player 1 Mulden sind p1-p6)
        let oppositePit = 'p' + (13 - parseInt(lastPit.slice(1)));
        let capturedStones = pits[oppositePit];
        pits[oppositePit] = 0;
        pits[lastPit] = 0;
        pits['player2Store'] += capturedStones + 1;
    }
}

// Function to move stones
function moveStones(startPit) {
    let stones = pits[startPit];
    pits[startPit] = 0;
    let currentPit = startPit;

    while (stones > 0) {
        currentPit = getNextPit(currentPit);
        pits[currentPit]++;
        stones--;
    }
    checkCapture (lastPit);
    // Switch player after move
    currentPlayer = (currentPlayer === 1) ? 2 : 1;
    renderBoard();
}

// Helper function to get the next pit in the sequence
function getNextPit(pit) {
    let pitOrder = [
        'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 
        'player1Store', 
        'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 
        'player2Store'
    ];
    let currentIndex = pitOrder.indexOf(pit);
    return pitOrder[(currentIndex + 1) % pitOrder.length];
}

// Set up event listeners for pits
document.querySelectorAll('.pit').forEach(pit => {
    pit.addEventListener('click', (event) => {
        pitClicked(event.target.id);
    });
});

// Initial render of the board
renderBoard();