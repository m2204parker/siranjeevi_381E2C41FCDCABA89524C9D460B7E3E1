const video = document.getElementById("video");
const startBtn = document.getElementById("start-btn");
const gestureDisplay = document.getElementById("gesture");

// Access webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing webcam: ", err);
    });

// Handle "Start Detection" button
startBtn.addEventListener("click", () => {
    fetch("/start-detection")  // Calls Flask backend
        .then(response => response.json())
        .then(data => {
            gestureDisplay.innerText = data.gesture || "No Gesture Detected";
        })
        .catch(error => console.error("Error:", error));
});
