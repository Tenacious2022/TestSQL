document.addEventListener('DOMContentLoaded', () => {
  const startBtn = document.querySelector('.options-button');
  const popupInfo = document.querySelector('.popup-info');
  const exitBtn = document.querySelector('.exit-btn');
  const main = document.querySelector('.main');
  const continueBtn = document.querySelector('.continue-btn');
  const quizSection = document.querySelector('.quiz-section');
  const quizBox = document.querySelector('.quiz-box');

  const tryAgainBtn = document.querySelector('.tryAgain-btn');
  const goHomeBtn = document.querySelector('.goHome-btn');
  const nextBtn = document.querySelector('.next-btn');
  const prevBtn = document.querySelector('.prev-btn');

  let questionsData = null; 
  let userSelections = null;
  let arrayNumb = []; 
  let arrayQuestions = [];
  let arrayAnswers = [];
  let marks = [];
  let levels = [];
  let usersAnswers = [];
  let questionCount = 0;
  let questionNumb = 1;
  let feedback_data = {
    arrayQuestions: [],
    arrayAnswers: [],
    usersAnswers: [],
    marks: [],
    levels: [],
  };

  // Function to fetch questions from the server
  async function fetchQuestions() {
    try {
      const response = await fetch('/displayQuestions/');
      if (!response.ok) {
        throw new Error('Failed to fetch questions');
      }
      questionsData = await response.json();
      createArrayQuestions(arrayNumb, questionsData);
    } catch (error) {
      console.error(error);
    }
  }

  // Function to create arrays of questions, answers, marks, usersAnswers, and levels
  function createArrayQuestions(arrayNumb, questionsData) {
    arrayQuestions = [];
    arrayAnswers = [];
    marks = [];
    usersAnswers = [];
    levels = [];
    let increment = 0;

    for (let i = 0; i < arrayNumb.length; i++) {
      const numQuestionsToPick = arrayNumb[i];

      for (let index = 0; index < numQuestionsToPick; index++) {
        if (i == 2) {
          arrayQuestions[increment] = questionsData.Advanced[index].question;
          arrayAnswers[increment] = questionsData.Advanced[index].answer;
          marks[increment] = questionsData.Advanced[index].marks;
          levels[increment] = questionsData.Advanced[index].level;
          increment++;
        }

        if (i == 0) {
          arrayQuestions[increment] = questionsData.Basic[index].question;
          arrayAnswers[increment] = questionsData.Basic[index].answer;
          marks[increment] = questionsData.Basic[index].marks;
          levels[increment] = questionsData.Basic[index].level;
          increment++;
        }

        if (i == 1) {
          arrayQuestions[increment] = questionsData.Intermediate[index].question;
          arrayAnswers[increment] = questionsData.Intermediate[index].answer;
          marks[increment] = questionsData.Intermediate[index].marks;
          levels[increment] = questionsData.Intermediate[index].level;

          increment++;
        }
      }
    }

    feedback_data.arrayQuestions = arrayQuestions;
    feedback_data.arrayAnswers = arrayAnswers;
    feedback_data.marks = marks;
    feedback_data.levels = levels;
  }

  // Event listeners
  startBtn.addEventListener('click', (event) => {
    event.preventDefault();

    const Basic = parseInt(document.getElementById('easy').value);
    const Intermediate = parseInt(document.getElementById('medium').value);
    const Advanced = parseInt(document.getElementById('hard').value);

    userSelections = {
      Basic: Basic,
      Intermediate: Intermediate,
      Advanced: Advanced,
    };

    arrayNumb = [Basic, Intermediate, Advanced];

    const allZero = arrayNumb.every(value => value === 0);

    if (allZero) {
      arrayNumb = [3, 3, 3];
      event.preventDefault();
      popupInfo.classList.add('active');
      main.classList.add('active');
      fetchQuestions();
      document.getElementById('empty-fields-notification').style.display = 'none';
      continueBtn.disabled = false;
      
    } else {
      event.preventDefault();
      popupInfo.classList.add('active');
      main.classList.add('active');
      fetchQuestions();
      document.getElementById('empty-fields-notification').style.display = 'none';
      continueBtn.disabled = false;
    }
  });

  exitBtn.addEventListener('click', () => {
    popupInfo.classList.remove('active');
    main.classList.remove('active');
  });

  continueBtn.addEventListener('click', () => {
    quizSection.classList.add('active');
    popupInfo.classList.remove('active');
    main.classList.remove('active');
    quizBox.classList.add('active');

    showQuestions(0);
    questionCounter(1);
    headerMarks();
  });

  tryAgainBtn.addEventListener('click', () => {
    quizBox.classList.add('active');
    nextBtn.classList.remove('active');

    questionCount = 0;
    questionNumb = 1;
    usersAnswers = [];
    showQuestions(questionCount);
    questionCounter(questionNumb);
    fetchQuestions();
    headerMarks();
  });

  goHomeBtn.addEventListener('click', () => {
    quizSection.classList.remove('active');
    nextBtn.classList.remove('active');

    questionCount = 0;
    questionNumb = 1;
    usersAnswers = [];
    showQuestions(questionCount);
    questionCounter(questionNumb);
    questionsData = null;
    headerMarks();
  });

  nextBtn.addEventListener('click', () => {
    const userAnswer = document.querySelector('.user-answer').value;
    usersAnswers[questionCount] = userAnswer;
    feedback_data.usersAnswers = usersAnswers;
    document.querySelector('.user-answer').value = "";

    if (questionCount < arrayQuestions.length - 1) {
      questionCount++;
      showQuestions(questionCount);
      questionNumb++;
      questionCounter(questionNumb);
      headerMarks();
    } else {
      sendFeedbackDataToServer(feedback_data);
      showResultBox();
    }
  });

    prevBtn.addEventListener('click', () => {
      if (questionCount > 0) {
        questionCount--;
        const userAnswer = usersAnswers[questionCount];
        document.querySelector('.user-answer').value = userAnswer;
        questionNumb--;
        showQuestions(questionCount);
        questionCounter(questionNumb);
        headerMarks();
      }
    });

  // Display questions
  function showQuestions(index) {
    const questionText = document.querySelector('.question-text');
    questionText.textContent = `${index + 1}. ${arrayQuestions[index]}`;
    const answerInput = document.querySelector('.answer-input');
    answerInput.style.display = 'block';
  }

  // Update question counter
  function questionCounter(index) {
    const questionTotal = document.querySelector('.question-total');
    questionTotal.textContent = `${index} of ${arrayQuestions.length} Questions`;
  }

  // Update header marks
  function headerMarks() {
    const headerMarksText = document.querySelector('.header-score');
    headerMarksText.textContent = `Marks: ${marks[questionCount]}`;
  }

  // Show result box
  function showResultBox() {
    quizBox.classList.remove('active');
   
  }


  // Function to send feedback_data to the server
function sendFeedbackDataToServer(feedbackData) {
  fetch('/submitFeedback/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(feedbackData),
  })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to submit feedback data');
      }
      return response.json();
    })

    .then(data => {
      const feedbackData = data.feedback_data;
      const totalMarksObtained = data.total_marks_obtained;
      const feedbackTableBody = document.getElementById('feedback-table-body');
      const totalMarksElement = document.querySelector('.totalMarks');

      totalMarksElement.textContent = `Total Marks Obtained: ${totalMarksObtained}`;
      feedbackTableBody.innerHTML = ''; 

      for (const key in feedbackData) {
        if (feedbackData.hasOwnProperty(key)) {
          const feedback_item = feedbackData[key];
          
          const row = document.createElement('tr');
          row.innerHTML = `
              <td>${feedback_item.question}</td>
              <td>${feedback_item.level}</td>
              <td>${feedback_item.expected_answer}</td>
              <td>${feedback_item.user_answer}</td>
              <td>${feedback_item.marks_obtained}</td>
          `;
          feedbackTableBody.appendChild(row);
        }
      }

      const feedbackContainer = document.querySelector('.feedback');
      feedbackContainer.classList.add('active');
    })
    .catch(error => {
      console.error('Error submitting feedback data:', error);
    });
}
});
