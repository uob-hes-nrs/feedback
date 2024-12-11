let questionCount = 0;
const questionList = document.getElementById('question-list');

// Add new question
document.getElementById('add-question-btn').addEventListener('click', function () {
    const questionContainer = document.createElement('div');
    questionContainer.classList.add('question-container');
    questionContainer.setAttribute('id', `question-${questionCount}`);

    questionContainer.innerHTML = `
        <label>Question Title:</label>
        <input type="text" id="title-${questionCount}" placeholder="Question title" required>

        <label>Description:</label>
        <textarea id="description-${questionCount}" placeholder="Description"></textarea>

        <label>Marks:</label>
        <input type="number" id="marks-${questionCount}" placeholder="Marks" required>

        <button class="remove-question-btn" onclick="removeQuestion(${questionCount})">Remove Question</button>
    `;

    questionList.appendChild(questionContainer);
    questionCount++;
});

// Remove question
function removeQuestion(questionId) {
    const questionContainer = document.getElementById(`question-${questionId}`);
    questionList.removeChild(questionContainer);
}

// Submit the form and save it in Firestore
document.getElementById('submit-form-btn').addEventListener('click', function () {
    const formTitle = document.getElementById('form-title').value;
    const components = [];

    // Collect all question data
    for (let i = 0; i < questionCount; i++) {
        const title = document.getElementById(`title-${i}`).value;
        const description = document.getElementById(`description-${i}`).value;
        const marks = document.getElementById(`marks-${i}`).value;

        if (title && description && marks) {
            components.push({
                field: title,
                description: description,
                max_marks: parseInt(marks),
            });
        }
    }

    // Submit to backend (Firestore)
    fetch('/create_feedback_form', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ form_title: formTitle, components: components }),
    })
        .then((res) => res.json())
        .then((data) => {
            alert(data.message);
            // Clear the form after submission
            document.getElementById('form-title').value = '';
            document.getElementById('question-list').innerHTML = '';
            questionCount = 0;
        })
        .catch((error) => {
            alert('Error submitting form: ' + error.message);
        });
});
