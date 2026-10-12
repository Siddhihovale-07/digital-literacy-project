function toggleMenu(){
    const menu = document.getElementById("navMenu");
    if(menu) menu.classList.toggle("open");
}

function speakLesson(){
    const textElement = document.getElementById("speechText");
    if(!textElement || !("speechSynthesis" in window)){
        alert("Text-to-speech is not supported in this browser.");
        return;
    }
    window.speechSynthesis.cancel();
    const speech = new SpeechSynthesisUtterance(textElement.textContent);
    speech.rate = 0.85;
    speech.pitch = 1;
    window.speechSynthesis.speak(speech);
}
