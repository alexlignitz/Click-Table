document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.getElementsByClassName('vote-btn')
    const counter = document.querySelector('.voting-counter')
    let counterValue = 0


    for (let i = 0; i < buttons.length; i++) {
        const button = buttons[i]

        button.addEventListener('click', function () {
            counterValue = counterValue + (i+1)
            counter.innerText = counterValue
        })
    }

});