document.getElementById('fetch-submissions').addEventListener('click', function () {
    const assignmentId = document.getElementById('assignment-id').value;

    fetch(`/get_submissions/${assignmentId}`, {
        method: 'GET',
    })
        .then((res) => res.json())
        .then((data) => {
            const submissionListContainer = document.getElementById('submission-list-container');
            submissionListContainer.innerHTML = ''; // Clear previous list

            if (data.length > 0) {
                data.forEach((submission) => {
                    const submissionElement = document.createElement('div');
                    submissionElement.classList.add('submission-item');
                    submissionElement.textContent = `Student ID: ${submission.student_id}, Status: ${submission.status}`;
                    submissionElement.addEventListener('click', () =>
                        loadFeedbackForm(submission.submission_id, assignmentId)
                    );
                    submissionListContainer.appendChild(submissionElement);
                });
            } else {
                submissionListContainer.innerHTML = 'No submissions found.';
            }
        })
        .catch((error) => {
            console.error('Error fetching submissions:', error);
            alert('Error fetching submissions.');
        });
});

function loadFeedbackForm(submissionId, assignmentId) {
    fetch(`/get_feedback_form/${assignmentId}`, {
        method: 'GET',
    })
        .then((res) => res.json())
        .then((data) => {
            if (Array.isArray(data.components)) {
                const formContainer = document.getElementById('feedback-form-container');
                formContainer.innerHTML = ''; // Clear previous form

                data.components.forEach((component, index) => {
                    const questionContainer = document.createElement('div');
                    questionContainer.classList.add('question-container');

                    questionContainer.innerHTML = `
                        <label for="marks-${index}">${component.field}</label>
                        <p>${component.description}</p>
                        <input type="number" id="marks-${index}" max="${component.max_marks}" placeholder="Enter marks">
                        <label for="feedback-${index}">Feedback:</label>
                        <textarea id="feedback-${index}" placeholder="Enter your feedback"></textarea>
                    `;

                    formContainer.appendChild(questionContainer);
                });

                document.getElementById('grade-submission-form').onsubmit = function (e) {
                    e.preventDefault();

                    const grades = [];
                    const feedback = [];
                    const components = document.querySelectorAll('[id^="marks-"]');

                    components.forEach((component, index) => {
                        grades.push({
                            field: component.id,
                            marks: component.value,
                        });

                        const feedbackText = document.getElementById(`feedback-${index}`).value;
                        feedback.push({ feedback: feedbackText });
                    });

                    fetch('/grade_submission', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            submission_id: submissionId,
                            grades: grades,
                            feedback: feedback,
                        }),
                    })
                        .then((res) => res.json())
                        .then((data) => alert(data.message))
                        .catch((error) => alert('Error submitting feedback.'));
                };
            } else {
                alert('Error: Feedback form components not found or invalid.');
            }
        })
        .catch((error) => {
            console.error('Error fetching feedback form:', error);
            alert('Error fetching feedback form.');
        });
}
