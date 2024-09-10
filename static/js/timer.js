let timeLeft = 60;
function startTimer() {
    const countdown = setInterval(() => {
        document.getElementById("timer").innerHTML = 'Complete your booking in 00 : ' + timeLeft;
        timeLeft--;
        if (timeLeft < 0) {
            clearInterval(countdown);
            document.getElementById("timer").innerHTML = "Time's up!";
            location.reload()
        }
    }, 1000);
}
startTimer();