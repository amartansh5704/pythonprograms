// ============================================
//   QUIZ DATA - Questions, Options, Answers
// ============================================
const questions = [
    {
        question: "🌍 What is the capital city of Japan?",
        options: ["Beijing", "Tokyo", "Seoul", "Bangkok"],
        answer: 1  // Tokyo (index 1)
    },
    {
        question: "💻 What does HTML stand for?",
        options: [
            "Hyper Text Markup Language",
            "High Tech Modern Language",
            "Hyper Transfer Method Link",
            "Home Tool Markup Language"
        ],
        answer: 0  // First option
    },
    {
        question: "🔢 What is 15 × 8?",
        options: ["100", "110", "120", "130"],
        answer: 2  // 120
    },
    {
        question: "🎨 Which CSS property changes text color?",
        options: ["font-color", "text-color", "color", "background-color"],
        answer: 2  // color
    },
    {
        question: "🌊 What is the largest ocean on Earth?",
        options: [
            "Atlantic Ocean",
            "Indian Ocean",
            "Arctic Ocean",
            "Pacific Ocean"
        ],
        answer: 3  // Pacific Ocean
    }
];

// ============================================
//   VARIABLES - Track Game State
// ============================================
let currentQuestion = 0;   // Which question we're on
let score = 0;             // Current score
let timerCount = 15;       // Countdown seconds
let timerInterval;         // Store timer reference
let answered = false;      // Did user answer?

// ============================================
//   GET ALL HTML ELEMENTS
// ============================================
const questionText  = document.getElementById("question-text");
const optionBtns    = document.querySelectorAll(".option");
const feedback      = document.getElementById("feedback");
const nextBtn       = document.getElementById("next-btn");
const scoreDisplay  = document.getElementById("score");
const questionNum   = document.getElementById("question-num");
const timerDisplay  = document.getElementById("timer");
const progress      = document.getElementById("progress");
const quizBox       = document.getElementById("quiz-box");
const resultBox     = document.getElementById("result-box");
const resultEmoji   = document.getElementById("result-emoji");
const resultTitle   = document.getElementById("result-title");
const resultMessage = document.getElementById("result-message");
const finalScore    = document.getElementById("final-score-text");
const restartBtn    = document.getElementById("restart-btn");

// ============================================
//   LOAD QUESTION FUNCTION
// ============================================
function loadQuestion() {
    // Reset state
    answered = false;
    feedback.textContent = "";
    feedback.className = "feedback";
    nextBtn.style.display = "none";

    // Get current question data
    const q = questions[currentQuestion];

    // Update question text
    questionText.textContent = q.question;

    // Update each option button
    optionBtns.forEach((btn, index) => {
        btn.textContent = q.options[index];
        btn.disabled = false;
        btn.className = "option";
    });

    // Update question number display
    questionNum.textContent = currentQuestion + 1;

    // Update progress bar
    const progressPercent = ((currentQuestion + 1) / questions.length) * 100;
    progress.style.width = progressPercent + "%";

    // Start timer
    startTimer();
}

// ============================================
//   TIMER FUNCTION
// ============================================
function startTimer() {
    // Reset timer
    timerCount = 15;
    timerDisplay.textContent = timerCount;
    timerDisplay.className = "";

    // Clear any existing timer
    clearInterval(timerInterval);

    // Count down every second
    timerInterval = setInterval(() => {
        timerCount--;
        timerDisplay.textContent = timerCount;

        // Warning effect when time is low
        if (timerCount <= 5) {
            timerDisplay.classList.add("danger");
        }

        // Time's up!
        if (timerCount === 0) {
            clearInterval(timerInterval);
            if (!answered) {
                timeUp();
            }
        }
    }, 1000);
}

// ============================================
//   TIME UP FUNCTION
// ============================================
function timeUp() {
    answered = true;

    // Disable all options
    optionBtns.forEach(btn => btn.disabled = true);

    // Show correct answer
    optionBtns[questions[currentQuestion].answer]
        .classList.add("correct");

    // Show feedback
    feedback.textContent = "⏰ Time's Up! Better luck next time!";
    feedback.className = "feedback wrong-msg";

    // Show next button
    nextBtn.style.display = "block";
}

// ============================================
//   CHECK ANSWER FUNCTION
// ============================================
function checkAnswer(selectedIndex) {
    // Stop if already answered
    if (answered) return;
    answered = true;

    // Stop timer
    clearInterval(timerInterval);

    // Disable all buttons
    optionBtns.forEach(btn => btn.disabled = true);

    const correctIndex = questions[currentQuestion].answer;

    // Correct answer selected
    if (selectedIndex === correctIndex) {
        score++;
        scoreDisplay.textContent = score;
        optionBtns[selectedIndex].classList.add("correct");
        feedback.textContent = "✅ Correct! Well done!";
        feedback.className = "feedback correct-msg";
    }
    // Wrong answer selected
    else {
        optionBtns[selectedIndex].classList.add("wrong");
        optionBtns[correctIndex].classList.add("correct");
        feedback.textContent = `❌ Wrong! Correct answer was: ${questions[currentQuestion].options[correctIndex]}`;
        feedback.className = "feedback wrong-msg";
    }

    // Show next button
    nextBtn.style.display = "block";
}

// ============================================
//   SHOW RESULT FUNCTION
// ============================================
function showResult() {
    // Hide quiz, show result
    quizBox.style.display = "none";
    resultBox.style.display = "block";

    const total = questions.length;
    const percentage = (score / total) * 100;

    // Set result based on score
    if (percentage === 100) {
        resultEmoji.textContent = "🏆";
        resultTitle.textContent = "Perfect Score!";
        resultMessage.textContent = "Absolutely amazing! You got everything right!";
    } else if (percentage >= 80) {
        resultEmoji.textContent = "🎉";
        resultTitle.textContent = "Excellent!";
        resultMessage.textContent = "Great job! You really know your stuff!";
    } else if (percentage >= 60) {
        resultEmoji.textContent = "😊";
        resultTitle.textContent = "Good Job!";
        resultMessage.textContent = "Not bad! Keep practicing to improve!";
    } else if (percentage >= 40) {
        resultEmoji.textContent = "😐";
        resultTitle.textContent = "Keep Trying!";
        resultMessage.textContent = "You can do better! Try again!";
    } else {
        resultEmoji.textContent = "😢";
        resultTitle.textContent = "Better Luck Next Time!";
        resultMessage.textContent = "Don't give up! Practice makes perfect!";
    }

    finalScore.textContent = `Your Score: ${score} / ${total}`;
}

// ============================================
//   RESTART GAME FUNCTION
// ============================================
function restartGame() {
    // Reset all variables
    currentQuestion = 0;
    score = 0;
    answered = false;

    // Reset displays
    scoreDisplay.textContent = "0";
    questionNum.textContent = "1";

    // Show quiz, hide result
    quizBox.style.display = "block";
    resultBox.style.display = "none";

    // Load first question
    loadQuestion();
}

// ============================================
//   EVENT LISTENERS
// ============================================

// Each option button click
optionBtns.forEach((btn, index) => {
    btn.addEventListener("click", () => {
        checkAnswer(index);
    });
});

// Next button click
nextBtn.addEventListener("click", () => {
    currentQuestion++;

    if (currentQuestion < questions.length) {
        loadQuestion();
    } else {
        showResult();
    }
});

// Restart button click
restartBtn.addEventListener("click", restartGame);

// ============================================
//   START THE GAME
// ============================================
loadQuestion();