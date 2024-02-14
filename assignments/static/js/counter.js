// Timer duration in milliseconds (3 hours)
const timerDuration = 3 * 60 * 60 * 1000;
        
// Variable to store the timer interval
let timerInterval;

// Function to start the timer
function startTimer() {
    // Check if the timer is already running
    if (!timerInterval) {
        const timerDisplay = document.getElementById('timer-display');
        const endTime = Date.now() + timerDuration;
        
        // Update the timer display every second
        timerInterval = setInterval(function () {
            const remainingTime = endTime - Date.now();
            if (remainingTime <= 0) {
                // Timer has expired, submit the assignment
                clearInterval(timerInterval);
                timerInterval = null;
                document.forms[0].submit(); // Submit the form
            } else {
                const hours = Math.floor(remainingTime / 3600000);
                const minutes = Math.floor((remainingTime % 3600000) / 60000);
                const seconds = Math.floor((remainingTime % 60000) / 1000);
                timerDisplay.textContent = `${hours}h ${minutes}m ${seconds}s`;
            }
        }, 1000);
    }
}

// Function to reset the timer
function resetTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
    startTimer(); // Start the timer again
}

// Initialize the timer when the page is loaded
window.addEventListener('load', startTimer);
