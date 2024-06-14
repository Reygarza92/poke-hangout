// Global variables (assuming received from server via AJAX)
let attemptsLeft = 6;
let guessedWord = "";

// Function to update the displayed word, attempts, and draw hangman
function updateGameInfo(newAttemptsLeft, newGuessedWord) {
  attemptsLeft = newAttemptsLeft;
  guessedWord = newGuessedWord.split(''); // Convert back to array for easier manipulation

  // Update the UI elements
  document.getElementById('attempts-left').textContent = `Intentos restantes: ${attemptsLeft}`;
  document.getElementById('guessed-word').textContent = `Palabra: ${guessedWord.join(' ')}`;

  // Call the function to draw the hangman based on attempts
  drawHangman(attemptsLeft);
}

// Function to send a guess and update the UI
function sendGuess(letter) {
  fetch('/guess', {
    method: 'POST',
    body: JSON.stringify({ letter }),
  })
  .then(response => response.json())
  .then(data => {
    updateGameInfo(data.attempts, data.guessedWord);
  })
  .catch(error => {
    console.error('Error sending guess:', error);
    // Handle errors appropriately (e.g., display an error message)
  });
}

// Function to draw the hangman based on attempts
function drawHangman(attempts) {
  const canvas = document.getElementById('hangman-canvas');
  const ctx = canvas.getContext('2d');

  // Clear the canvas before redrawing
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Set line width and color
  ctx.lineWidth = 2;
  ctx.strokeStyle = "#000";

  // Draw the base structure (gallows)
  ctx.beginPath();
  ctx.moveTo(175, 350);
  ctx.lineTo(225, 350);
  ctx.lineTo(225, 50);
  ctx.lineTo(275, 50);
  ctx.stroke();
  ctx.closePath();

  // Draw additional elements based on attempts
  switch (attempts) {
    case 1:
      // Draw head (circle)
      ctx.beginPath();
      ctx.arc(275, 75, 25, 0, Math.PI * 2);
      ctx.stroke();
      ctx.closePath();
      break;
    case 2:
      // Draw body
      ctx.beginPath();
      ctx.moveTo(275, 100);
      ctx.lineTo(275, 200);
      ctx.stroke();
      ctx.closePath();
      break;
    case 3:
      // Draw left arm
      ctx.beginPath();
      ctx.moveTo(275, 125);
      ctx.lineTo(250, 175);
      ctx.stroke();
      ctx.closePath();
      break;
    case 4:
      // Draw right arm
      ctx.beginPath();
      ctx.moveTo(275, 125);
      ctx.lineTo(300, 175);
      ctx.stroke();
      ctx.closePath();
      break;
    case 5:
      // Draw left leg
      ctx.beginPath();
      ctx.moveTo(275, 200);
      ctx.lineTo(250, 250);
      ctx.stroke();
      ctx.closePath();
      break;
    case 6:
      // Draw right leg
      ctx.beginPath();
      ctx.moveTo(275, 200);
      ctx.lineTo(300, 250);
      ctx.stroke();
      ctx.closePath();
      break;
    case 7:
      // Draw eye (circle)
      ctx.beginPath();
      ctx.arc(275, 40, 10, 0, Math.PI * 2);
      ctx.stroke();
      ctx.closePath();
      break;
  }
}

// Event listeners for forms
document.getElementById('guess-form').addEventListener('submit', (event) => {
  event.preventDefault();
  const letter = event.target.elements['letter'].value.toLowerCase();
  
// ... dentro de la función updateGameInfo()

if (data.isWinner) {
    // Mostrar mensaje de victoria (por ejemplo, usando alert o actualizando la interfaz)
    alert("¡Felicidades! Has adivinado el Pokemon.");
    // Deshabilitar la interacción con el juego (opcional)
    document.getElementById('guess-form').disabled = true;
    document.getElementById('hint-form').disabled = true;
  } else if (attemptsLeft === 0) {
    // Mostrar mensaje de derrota revelando la palabra
    guessedWordElement.textContent = `Palabra: ${data.wordToGuess}`; // Reemplazar con la palabra del servidor
    alert("¡Lo siento! Te has quedado sin intentos. La palabra era: " + data.wordToGuess);
    // Deshabilitar la interacción con el juego (opcional)
    document.getElementById('guess-form').disabled = true;
    document.getElementById('hint-form').disabled = true;
  }
  