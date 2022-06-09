function NavbarFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
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