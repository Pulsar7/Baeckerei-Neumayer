function NavbarFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}

function CloseCookieQuestionContainer() {
    var cookie_question_container = document.getElementById("cookie_question_container");
    cookie_question_container.style.display = "none";
}

function OpenModal(number) {
    var modal = document.getElementById("Modal" + number);
    modal.style.display = "block";
}

function CloseModal(number) {
    var modal = document.getElementById("Modal" + number);
    modal.style.display = "none";
    console.log(modal);
}