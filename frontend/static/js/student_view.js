// Fetch all submissions for the logged-in student using session-based authentication
fetch('/get_student_submissions', {
    method: 'GET',
})
    .then((res) => res.json())
    .then((data) => {
        const submissionsContainer = document.getElementById('submissions-container');
        submissionsContainer.innerHTML = ''; // Clear previous content

        if (data.length > 0) {
            data.forEach((submission) => {
                const submissionElement = document.createElement('div');
                submissionElement.classList.add('submission-item');
                submissionElement.textContent = `Submission ID: ${submission.submission_id}, Status: ${submission.status}`;
                submissionElement.addEventListener('click', () => viewFeedback(submission));
                submissionsContainer.appendChild(submissionElement);
            });
        } else {
            submissionsContainer.innerHTML = '<p>No submissions found.</p>';
        }
    })
    .catch((error) => {
        console.error('Error fetching submissions:', error);
        alert('Error fetching submissions.');
    });

// Display feedback for a selected submission
function viewFeedback(submission) {
    const feedbackContainer = document.getElementById('feedback-container');
    const feedbackList = document.getElementById('feedback-list');

    feedbackList.innerHTML = ''; // Clear previous feedback

    if (submission.feedback && submission.grades) {
        submission.feedback.forEach((feedbackItem, index) => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <strong>Component ${index + 1}:</strong> ${feedbackItem.feedback || 'No feedback provided'}<br>
                <strong>Grade:</strong> ${submission.grades[index]?.marks || 'N/A'}
            `;
            feedbackList.appendChild(listItem);
        });

        feedbackContainer.style.display = 'block';
    } else {
        feedbackContainer.style.display = 'none';
        alert('No feedback available for this submission.');
    }
}
