let sentence = [];

function updateWord() {
    fetch('/get-word')
        .then(response => response.json())
        .then(data => {
            if (data.word) {
                document.getElementById('detected-word').innerText = data.word;
                sentence.push(data.word);
                document.getElementById('sentence').innerText = sentence.join(' ');

                // Speak the word
                speakWord(data.word);
            }
        });
}

function speakWord(word) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(word);
    synth.speak(utterance);
}

setInterval(updateWord, 2000);

